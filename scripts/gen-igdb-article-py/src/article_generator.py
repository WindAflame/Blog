import os
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from .config import CONTENT_OUTPUT_DIR, DEFAULT_AUTHOR, MIHOYO_GAMES
from .igdb_client import IGDBClient
from .ennead_client import EnneadAPIClient
from .models.mihoyo_game_config import MihoyoGameConfig


class ArticleGenerator:
    """Generator for creating IGDB game articles with Jinja2 templates"""

    def __init__(self):
        self.igdb_client = IGDBClient()
        self.output_dir = CONTENT_OUTPUT_DIR

        # Set up Jinja2 environment
        template_dir = Path(__file__).parent
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))

    def generate_article(self, game_key: str, update_igdb_id: str):
        """
        Generate article for a Mihoyo game update

        Args:
            game_key: Key for the game in MIHOYO_GAMES config (e.g., 'genshin', 'starrail')
            update_igdb_id: IGDB ID of the specific game update/version

        Raises:
            ValueError: If game_key not found, IGDB update doesn't exist, or article already exists
        """
        # Get game config
        if game_key not in MIHOYO_GAMES:
            raise ValueError(
                f"Game '{game_key}' not found. Available games: {list(MIHOYO_GAMES.keys())}"
            )

        game_config = MIHOYO_GAMES[game_key]

        # Check if article already exists
        article_dir = self.output_dir / f"igdb_{update_igdb_id}"
        if article_dir.exists():
            raise ValueError(
                f"Article already exists at {article_dir}. Skipping generation."
            )

        # Fetch update details from IGDB
        print(f"Fetching update details from IGDB (ID: {update_igdb_id})...")
        update_game = self.igdb_client.get_game_by_id(update_igdb_id)

        print(f"✓ Found update: {update_game.name}")
        if update_game.alternative_names:
            print(f"  Alternative names: {', '.join(update_game.alternative_names)}")

        # Extract version keywords from update name and alternative names
        version_keywords = self.igdb_client.extract_version_keywords(update_game)
        print(f"✓ Extracted version keywords: {', '.join(version_keywords)}")

        # Fetch news from Ennead API using version keywords
        print(f"Searching for news article with versions: {', '.join(version_keywords)}...")
        ennead_client = EnneadAPIClient(game_config.api_news)
        news_article = ennead_client.get_update_news_by_version(version_keywords)

        if not news_article:
            raise ValueError(
                f"Failed to find news article for versions: {', '.join(version_keywords)}"
            )

        print(f"✓ Found news article: {news_article.title}")

        # Prepare template context
        context = self._prepare_context(game_config, update_game, news_article, update_igdb_id)

        # Generate articles
        self._generate_article_files(update_igdb_id, context)

        print(f"✓ Articles generated successfully in {article_dir}")

    def _prepare_context(self, game_config: MihoyoGameConfig, update_game, news_article, update_igdb_id: str):
        """Prepare Jinja2 template context"""
        today = datetime.now().strftime("%Y-%m-%d")

        # Determine game website URL based on game
        game_websites = {
            "Genshin Impact": "https://genshin.hoyoverse.com/",
            "Honkai: Star Rail": "https://hsr.hoyoverse.com/",
            "Zenless Zone Zero": "https://zenless.hoyoverse.com/",
        }

        game_website = game_websites.get(game_config.game_name, "https://www.hoyoverse.com/")

        # Generate game slug for IGDB URL (use update name)
        game_slug = update_game.name.lower().replace(" ", "-").replace(":", "")

        return {
            "igdb_id": update_igdb_id,
            "game_name": game_config.game_name,
            "update_title": news_article.title,
            "date": today,
            "banner_url": news_article.banner_webp_url or "",
            "update_url": news_article.url,
            "author": DEFAULT_AUTHOR,
            "game_website": game_website,
            "game_slug": game_slug,
        }

    def _generate_article_files(self, igdb_id: str, context: dict):
        """Generate article files for English and French"""
        # Create output directory
        article_dir = self.output_dir / f"igdb_{igdb_id}"
        article_dir.mkdir(parents=True, exist_ok=True)

        # Generate English article
        template_en = self.jinja_env.get_template("template.md.jinja2")
        content_en = template_en.render(context)

        with open(article_dir / "index.md", "w", encoding="utf-8") as f:
            f.write(content_en)

        print(f"✓ Generated English article: {article_dir / 'index.md'}")

        # Generate French article
        template_fr = self.jinja_env.get_template("template.fr.md.jinja2")
        content_fr = template_fr.render(context)

        with open(article_dir / "index.fr.md", "w", encoding="utf-8") as f:
            f.write(content_fr)

        print(f"✓ Generated French article: {article_dir / 'index.fr.md'}")
