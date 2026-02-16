from typing import Optional
from ..base import BaseModule
from ...models.game_config import GameConfig
from ...models.news_article import NewsArticle
from .ennead_client import EnneadAPIClient
from .config import MIHOYO_GAMES, ENNEAD_API_URLS, GAME_WEBSITES, MIHOYO_BASE_NAMES


class MihoyoModule(BaseModule):
    """Module for Mihoyo/HoYoverse games (Genshin Impact, Star Rail, ZZZ)."""

    def get_available_games(self) -> dict[str, GameConfig]:
        return MIHOYO_GAMES

    def get_game_config(self, game_key: str) -> Optional[GameConfig]:
        return MIHOYO_GAMES.get(game_key)

    def fetch_news_article(self, game_config: GameConfig, version_keywords: list) -> Optional[NewsArticle]:
        # Find the game key from config to get the API URL
        game_key = None
        for key, config in MIHOYO_GAMES.items():
            if config.game_name == game_config.game_name:
                game_key = key
                break

        if game_key is None or game_key not in ENNEAD_API_URLS:
            return None

        api_url = ENNEAD_API_URLS[game_key]
        ennead_client = EnneadAPIClient(api_url)
        return ennead_client.get_update_news_by_version(version_keywords)

    def filter_version_keywords(self, keywords: list) -> list:
        """Filter out Mihoyo base game names from alternative name keywords."""
        filtered = []
        for keyword in keywords:
            cleaned = keyword
            for base in MIHOYO_BASE_NAMES:
                cleaned = cleaned.replace(base, "").strip()
            # Remove leading/trailing dashes and spaces
            cleaned = cleaned.strip(" -")
            # Keep the keyword if it's still meaningful after cleaning
            if cleaned and len(cleaned) > 5:
                filtered.append(cleaned)
            elif keyword == cleaned:
                # Keyword wasn't affected by filtering, keep it
                filtered.append(keyword)
        return filtered if filtered else keywords

    def prepare_extra_context(self, game_config: GameConfig, news_article: Optional[NewsArticle]) -> dict:
        game_website = GAME_WEBSITES.get(game_config.game_name, "https://www.hoyoverse.com/")

        context = {
            "game_website": game_website,
        }

        if news_article:
            context["banner_url"] = news_article.banner_webp_url or ""
            context["update_url"] = news_article.url
            context["update_title"] = news_article.title

        return context
