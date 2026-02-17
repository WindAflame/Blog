from typing import Optional
from ..base import BaseModule
from ...models.game_config import GameConfig
from ...models.news_article import NewsArticle
from .ennead_client import EnneadAPIClient
from .config import MIHOYO_GAMES, ENNEAD_API_URLS, GAME_WEBSITES, MIHOYO_BASE_NAMES, HOYOLAB_LANG_CODES


class MihoyoModule(BaseModule):
    """Module for Mihoyo/HoYoverse games (Genshin Impact, Star Rail, ZZZ)."""

    def get_available_games(self) -> dict[str, GameConfig]:
        return MIHOYO_GAMES

    def get_game_config(self, game_key: str) -> Optional[GameConfig]:
        return MIHOYO_GAMES.get(game_key)

    def fetch_news_article(self, game_config: GameConfig, version_keywords: list, lang: str = "en") -> Optional[NewsArticle]:
        # Find the game key from config to get the API URL
        game_key = None
        for key, config in MIHOYO_GAMES.items():
            if config.game_name == game_config.game_name:
                game_key = key
                break

        if game_key is None or game_key not in ENNEAD_API_URLS:
            return None

        api_url = f"{ENNEAD_API_URLS[game_key]}?lang={lang}"
        ennead_client = EnneadAPIClient(api_url)
        return ennead_client.get_update_news_by_version(version_keywords)

    def fetch_news_article_by_id(self, game_config: GameConfig, article_id: str, lang: str = "en") -> Optional[NewsArticle]:
        game_key = None
        for key, config in MIHOYO_GAMES.items():
            if config.game_name == game_config.game_name:
                game_key = key
                break

        if game_key is None or game_key not in ENNEAD_API_URLS:
            return None

        api_url = f"{ENNEAD_API_URLS[game_key]}?lang={lang}"
        ennead_client = EnneadAPIClient(api_url)
        return ennead_client.get_article_by_id(article_id)

    def enrich_version_keywords(self, keywords: list, alternative_names: list | None) -> list:
        """Extract extra keywords by removing Mihoyo base game names from alt names."""
        if not alternative_names:
            return keywords

        extra = []
        for alt_name in alternative_names:
            cleaned = alt_name
            for base in MIHOYO_BASE_NAMES:
                cleaned = cleaned.replace(base, "").strip()
            cleaned = cleaned.strip(" -")
            if cleaned and len(cleaned) > 2 and cleaned.lower() not in [k.lower() for k in keywords]:
                extra.append(cleaned)

        return keywords + extra

    def prepare_extra_context(self, game_config: GameConfig, news_article: Optional[NewsArticle], lang: str = "en") -> dict:
        game_website = GAME_WEBSITES.get(game_config.game_name, "https://www.hoyoverse.com/")

        context = {
            "game_website": game_website,
        }

        if news_article:
            context["banner_url"] = news_article.banner_webp_url or ""
            context["update_title"] = news_article.title
            # Force HoYoLab language via query param
            hoyolab_lang = HOYOLAB_LANG_CODES.get(lang, "en-us")
            separator = "&" if "?" in news_article.url else "?"
            context["update_url"] = f"{news_article.url}{separator}lang={hoyolab_lang}"

        return context
