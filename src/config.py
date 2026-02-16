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


def load_config() -> dict:
    load_dotenv()
    logger.info("Environment variable is loaded.")

    client_id = os.getenv("client")
    access_token = os.getenv("token")
    game_id = os.getenv("game")

    if not client_id or not access_token or not game_id:
        raise Exception("The environment file does not contain the required fields")

    return {
        "client_id": client_id,
        "access_token": access_token,
        "game_id": game_id,
    }
