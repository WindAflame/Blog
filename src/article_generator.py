import os
import logging
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from .config import CONTENT_OUTPUT_DIR, DEFAULT_AUTHOR
from .igdb_client import IGDBClient
from .modules.base import BaseModule
from .models.game_config import GameConfig

logger = logging.getLogger(__name__)


class ArticleGenerator:
    """Generator for creating IGDB game articles with Jinja2 templates"""

    def __init__(self, module: BaseModule, output_dir: str | None = None):
        self.module = module
        self.igdb_client = IGDBClient()
        self.output_dir = Path(output_dir) if output_dir else CONTENT_OUTPUT_DIR

        # Set up Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), "template")
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))

    def generate_article(self, update_igdb_id: str, game_key: str | None = None):
        """
        Generate article for a game update.

        Args:
            update_igdb_id: IGDB ID of the specific game update/version
            game_key: Optional game key for module-based game resolution

        Raises:
            ValueError: If game_key not found, IGDB update doesn't exist, or article already exists
        """
        # Resolve game config via module or fallback to IGDB
        game_config = None
        if game_key:
            game_config = self.module.get_game_config(game_key)
            if not game_config:
                available = self.module.get_available_games()
                raise ValueError(
                    f"Game '{game_key}' not found. Available games: {list(available.keys())}"
                )

        # Check if article already exists
        article_dir = self.output_dir / f"igdb_{update_igdb_id}"
        if article_dir.exists():
            raise ValueError(
                f"Article already exists at {article_dir}. Skipping generation."
            )

        # Fetch update details from IGDB
        logger.info("Fetching update details from IGDB (ID: %s)...", update_igdb_id)
        update_game = self.igdb_client.get_game_by_id(update_igdb_id)

        logger.info("Found update: %s", update_game.name)
        if update_game.alternative_names:
            logger.info("Alternative names: %s", ", ".join(update_game.alternative_names))

        # If no game_config from module, derive from IGDB data
        if not game_config:
            # Use the part before ":" as game name, or the full name
            if ":" in update_game.name:
                game_name = update_game.name.split(":", 1)[0].strip()
            else:
                game_name = update_game.name
            game_config = GameConfig(igdb_id=update_igdb_id, game_name=game_name)

        # Extract version keywords from update name and alternative names
        version_keywords = self.igdb_client.extract_version_keywords(update_game)
        version_keywords = self.module.enrich_version_keywords(version_keywords, update_game.alternative_names)
        logger.info("Version keywords: %s", ", ".join(version_keywords))

        # Fetch news article in English (search by version keywords)
        logger.info("Searching for news article (en)...")
        en_article = self.module.fetch_news_article(game_config, version_keywords, lang="en")
        if en_article:
            logger.info("Found: %s", en_article.title)
        else:
            logger.warning("No news article found")

        # Fetch the same article in other languages by ID
        articles_by_lang = {"en": en_article}
        if en_article:
            for lang in ["fr"]:
                logger.info("Fetching news article in '%s' (id: %s)...", lang, en_article.id)
                localized = self.module.fetch_news_article_by_id(game_config, en_article.id, lang=lang)
                if localized:
                    logger.info("Found: %s", localized.title)
                else:
                    logger.warning("Article not found in '%s', using English version", lang)
                    localized = en_article
                articles_by_lang[lang] = localized
        else:
            articles_by_lang["fr"] = None

        # Generate articles per language
        base_context = self._prepare_context(game_config, update_game, update_igdb_id)
        article_dir = self.output_dir / f"igdb_{update_igdb_id}"
        article_dir.mkdir(parents=True, exist_ok=True)

        for lang, template_name, filename in [
            ("en", "article.md.jinja2", "index.md"),
            ("fr", "article.fr.md.jinja2", "index.fr.md"),
        ]:
            context = {**base_context}
            extra = self.module.prepare_extra_context(game_config, articles_by_lang[lang], lang=lang)
            context.update(extra)

            template = self.jinja_env.get_template(template_name)
            content = template.render(context)

            with open(article_dir / filename, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info("Generated %s", article_dir / filename)

        logger.info("Articles generated in %s", article_dir)

    def _prepare_context(self, game_config: GameConfig, update_game, update_igdb_id: str):
        """Prepare base Jinja2 template context (language-independent)"""
        today = datetime.now().strftime("%Y-%m-%d")

        # Generate game slug for IGDB URL (use update name)
        game_slug = update_game.name.lower().replace(" ", "-").replace(":", "")

        # Build IGDB artwork image URL
        if update_game.artwork_image_id:
            banner_url = f"https://images.igdb.com/igdb/image/upload/t_720p/{update_game.artwork_image_id}.webp"
        else:
            banner_url = ""

        return {
            "igdb_id": update_igdb_id,
            "game_name": game_config.game_name,
            "date": today,
            "author": DEFAULT_AUTHOR,
            "game_slug": game_slug,
            # Defaults that modules can override per language
            "update_title": update_game.name,
            "banner_url": banner_url,
            "update_url": "",
            "game_website": "",
        }
