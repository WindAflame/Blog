from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from .config import CONTENT_OUTPUT_DIR, DEFAULT_AUTHOR
from .igdb_client import IGDBClient
from .modules.base import BaseModule
from .models.game_config import GameConfig


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
        print(f"Fetching update details from IGDB (ID: {update_igdb_id})...")
        update_game = self.igdb_client.get_game_by_id(update_igdb_id)

        print(f"  Found update: {update_game.name}")
        if update_game.alternative_names:
            print(f"  Alternative names: {', '.join(update_game.alternative_names)}")

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
        version_keywords = self.module.filter_version_keywords(version_keywords)
        print(f"  Version keywords: {', '.join(version_keywords)}")

        # Fetch news article via module
        print(f"Searching for news article...")
        news_article = self.module.fetch_news_article(game_config, version_keywords)

        if news_article:
            print(f"  Found news article: {news_article.title}")
        else:
            print(f"  No news article found (continuing without)")

        # Prepare base template context
        context = self._prepare_context(game_config, update_game, news_article, update_igdb_id)

        # Merge extra context from module
        extra_context = self.module.prepare_extra_context(game_config, news_article)
        context.update(extra_context)

        # Generate articles
        self._generate_article_files(update_igdb_id, context)

        print(f"  Articles generated in {article_dir}")

    def _prepare_context(self, game_config: GameConfig, update_game, news_article, update_igdb_id: str):
        """Prepare base Jinja2 template context"""
        today = datetime.now().strftime("%Y-%m-%d")

        # Generate game slug for IGDB URL (use update name)
        game_slug = update_game.name.lower().replace(" ", "-").replace(":", "")

        context = {
            "igdb_id": update_igdb_id,
            "game_name": game_config.game_name,
            "date": today,
            "author": DEFAULT_AUTHOR,
            "game_slug": game_slug,
            # Defaults that modules can override
            "update_title": update_game.name,
            "banner_url": "",
            "update_url": "",
            "game_website": "",
        }

        return context

    def _generate_article_files(self, igdb_id: str, context: dict):
        """Generate article files for English and French"""
        # Create output directory
        article_dir = self.output_dir / f"igdb_{igdb_id}"
        article_dir.mkdir(parents=True, exist_ok=True)

        # Generate English article
        template_en = self.jinja_env.get_template("article.md.jinja2")
        content_en = template_en.render(context)

        with open(article_dir / "index.md", "w", encoding="utf-8") as f:
            f.write(content_en)

        print(f"  Generated English article: {article_dir / 'index.md'}")

        # Generate French article
        template_fr = self.jinja_env.get_template("article.fr.md.jinja2")
        content_fr = template_fr.render(context)

        with open(article_dir / "index.fr.md", "w", encoding="utf-8") as f:
            f.write(content_fr)

        print(f"  Generated French article: {article_dir / 'index.fr.md'}")
