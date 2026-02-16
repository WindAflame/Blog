from ...models.game_config import GameConfig

# Mihoyo games configuration
MIHOYO_GAMES = {
    "genshin": GameConfig(
        igdb_id="119277",
        game_name="Genshin Impact",
    ),
    "starrail": GameConfig(
        igdb_id="178282",
        game_name="Honkai: Star Rail",
    ),
    "zzz": GameConfig(
        igdb_id="200551",
        game_name="Zenless Zone Zero",
    ),
}

# Ennead API URLs for each game
ENNEAD_API_URLS = {
    "genshin": "https://api.ennead.cc/mihoyo/genshin/news/notices",
    "starrail": "https://api.ennead.cc/mihoyo/starrail/news/notices",
    "zzz": "https://api.ennead.cc/mihoyo/zenless/news/notices",
}

# Game website URLs
GAME_WEBSITES = {
    "Genshin Impact": "https://genshin.hoyoverse.com/",
    "Honkai: Star Rail": "https://hsr.hoyoverse.com/",
    "Zenless Zone Zero": "https://zenless.hoyoverse.com/",
}

# Base game names to filter from alternative names
MIHOYO_BASE_NAMES = [
    "Genshin Impact", "Honkai: Star Rail", "Zenless Zone Zero",
    "Genshin", "Honkai", "Zenless",
]
