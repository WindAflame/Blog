from ..models.game_config import GameConfig
from ..models.news_article import NewsArticle
from typing import Optional


class BaseModule:
    """Base module defining the pipeline extension points.

    The default implementation provides generic behavior for any IGDB game.
    Subclass and override methods to customize behavior for specific games.
    """

    def get_available_games(self) -> dict[str, GameConfig]:
        """Return preconfigured games (empty by default)."""
        return {}

    def get_game_config(self, game_key: str) -> Optional[GameConfig]:
        """Resolve a game_key to a GameConfig. Returns None by default."""
        return None

    def fetch_news_article(self, game_config: GameConfig, version_keywords: list, lang: str = "en") -> Optional[NewsArticle]:
        """Fetch a news article for the given game and version. Returns None by default."""
        return None

    def fetch_news_article_by_id(self, game_config: GameConfig, article_id: str, lang: str = "en") -> Optional[NewsArticle]:
        """Fetch a news article by its ID in a specific language. Returns None by default."""
        return None

    def enrich_version_keywords(self, keywords: list, alternative_names: list | None) -> list:
        """Enrich version keywords using alternative names. Pass-through by default."""
        return keywords

    def prepare_extra_context(self, game_config: GameConfig, news_article: Optional[NewsArticle], lang: str = "en") -> dict:
        """Return extra template context. Empty by default."""
        return {}
