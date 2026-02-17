import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variable is loaded.")

# IGDB Configuration
IGDB_CLIENT_ID = os.getenv("client")
IGDB_ACCESS_TOKEN = os.getenv("token")

if not IGDB_CLIENT_ID or not IGDB_ACCESS_TOKEN:
    raise ValueError("IGDB credentials (client, token) not found in .env file")

# Default configuration
DEFAULT_AUTHOR = os.getenv("author", "unknown_writer")
CONTENT_OUTPUT_DIR = Path(os.getenv("output_dir", "output"))
