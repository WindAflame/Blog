import os
from pathlib import Path
from dotenv import load_dotenv

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
