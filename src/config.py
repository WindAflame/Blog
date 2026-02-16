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
DEFAULT_AUTHOR = os.getenv("author", "unknown_writer")
CONTENT_OUTPUT_DIR = Path(os.getenv("output_dir", "output"))
