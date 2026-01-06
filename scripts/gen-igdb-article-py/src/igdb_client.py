from igdb.wrapper import IGDBWrapper
from .config import IGDB_CLIENT_ID, IGDB_ACCESS_TOKEN
from .models.igdb_game import IGDBGame
import json
import re


class IGDBClient:
    """Client for interacting with IGDB API"""

    def __init__(self):
        self.wrapper = IGDBWrapper(IGDB_CLIENT_ID, IGDB_ACCESS_TOKEN)

    def get_game_by_id(self, game_id: str) -> IGDBGame:
        """
        Fetch game data from IGDB by game ID

        Args:
            game_id: IGDB game ID

        Returns:
            IGDBGame instance

        Raises:
            ValueError: If game not found
        """
        query = f"fields name, alternative_names.name; where id = {game_id};"

        try:
            response = self.wrapper.api_request("games", query)

            if not response or len(response) == 0:
                raise ValueError(f"Game with ID {game_id} not found on IGDB")

            # Parse JSON response if needed
            if isinstance(response, bytes):
                response = json.loads(response.decode('utf-8'))

            game_data = response[0] if isinstance(response, list) else response
            return IGDBGame.from_api_response(game_data)

        except Exception as e:
            raise ValueError(f"Error fetching game {game_id} from IGDB: {str(e)}")

    def verify_game_exists(self, game_id: str) -> bool:
        """
        Verify if a game exists on IGDB

        Args:
            game_id: IGDB game ID

        Returns:
            True if game exists, False otherwise
        """
        try:
            self.get_game_by_id(game_id)
            return True
        except (ValueError, Exception):
            return False

    def extract_version_keywords(self, game: IGDBGame) -> list:
        """
        Extract version keywords from game name and alternative names

        Args:
            game: IGDBGame instance

        Returns:
            List of version keywords to search for
        """
        keywords = []

        # Generic words to avoid (too common in descriptions)
        avoid_generic = ["interlude", "segue", "reprise", "prelude", "sonata"]

        # Extract from main name
        if ":" in game.name:
            version = game.name.split(":", 1)[1].strip()
            if version.lower() not in avoid_generic and len(version) > 3:
                keywords.append(version)

        # Extract version numbers from main name (always include)
        version_match = re.search(r'\d+\.\d+', game.name)
        if version_match:
            keywords.append(version_match.group(0))

        # Extract from alternative names
        if game.alternative_names:
            for alt_name in game.alternative_names:
                # Extract after colon
                if ":" in alt_name:
                    version = alt_name.split(":", 1)[1].strip()
                    if version.lower() not in avoid_generic and len(version) > 3:
                        keywords.append(version)

                # Extract version numbers (always include)
                version_match = re.search(r'\d+\.\d+', alt_name)
                if version_match:
                    keywords.append(version_match.group(0))

                # Remove base game name and extract remaining part
                cleaned_name = alt_name
                for base in ["Genshin Impact", "Honkai: Star Rail", "Zenless Zone Zero",
                           "Genshin", "Honkai", "Zenless"]:
                    cleaned_name = cleaned_name.replace(base, "").strip()

                # Remove leading/trailing dashes and spaces
                cleaned_name = cleaned_name.strip(" -")

                # If something remains, not too generic, and not too short, add it
                if (cleaned_name and
                    len(cleaned_name) > 5 and
                    cleaned_name.lower() not in avoid_generic):
                    keywords.append(cleaned_name)

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword.lower() not in seen:
                seen.add(keyword.lower())
                unique_keywords.append(keyword)

        return unique_keywords if unique_keywords else [game.name]
