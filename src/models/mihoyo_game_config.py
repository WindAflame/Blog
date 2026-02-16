from dataclasses import dataclass


@dataclass
class MihoyoGameConfig:
    igdb_id: str
    game_name: str
    api_news: str