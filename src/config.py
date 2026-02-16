import os
from pathlib import Path
from dotenv import load_dotenv
from .models.mihoyo_game_config import MihoyoGameConfig

# Load environment variables
load_dotenv()

# IGDB Configuration
IGDB_CLIENT_ID = os.getenv("client")
IGDB_ACCESS_TOKEN = os.getenv("token")

if not IGDB_CLIENT_ID or not IGDB_ACCESS_TOKEN:
    raise ValueError("IGDB credentials (client, token) not found in .env file")

# Default configuration
DEFAULT_AUTHOR = "endyw"
CONTENT_OUTPUT_DIR = Path("../../sources/zola-linkita/content")

# Mihoyo games configuration
MIHOYO_GAMES = {
    "genshin": MihoyoGameConfig(
        igdb_id="119277",
        game_name="Genshin Impact",
        api_news="https://api.ennead.cc/mihoyo/genshin/news/notices"
    ),
    "starrail": MihoyoGameConfig(
        igdb_id="178282",
        game_name="Honkai: Star Rail",
        api_news="https://api.ennead.cc/mihoyo/starrail/news/notices"
    ),
    "zzz": MihoyoGameConfig(
        igdb_id="200551",
        game_name="Zenless Zone Zero",
        api_news="https://api.ennead.cc/mihoyo/zenless/news/notices"
    ),
}
