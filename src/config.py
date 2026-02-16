import argparse
import os
import logging

from dotenv import load_dotenv

DESTINATION_DIRECTORY = "static"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch game data from IGDB API")
    parser.add_argument("game_id", nargs="?", default=None, help="IGDB Game ID (overrides .env)")
    return parser.parse_args()


def load_config(game_id_override: str | None = None) -> dict:
    load_dotenv()
    logger.info("Environment variable is loaded.")

    client_id = os.getenv("client")
    access_token = os.getenv("token")
    game_id = game_id_override or os.getenv("game")

    if not client_id or not access_token:
        raise Exception("The environment file does not contain the required fields (client, token)")

    if not game_id:
        raise Exception("Game ID is required: set 'game' in .env or pass it as argument")

    return {
        "client_id": client_id,
        "access_token": access_token,
        "game_id": game_id,
    }
