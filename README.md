# gen-igdb-article-py

Generates bilingual (EN/FR) game update articles from IGDB data.

Works generically with any IGDB game, or with a module (e.g. `mihoyo`) for game-specific features like news fetching and banners.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- An IGDB API client ID and access token ([Twitch developer portal](https://dev.twitch.tv/console))

## Setup

```bash
uv sync
```

## Configuration

Copy the `.env.template` file and fill in your credentials:

```bash
cp .env.template .env
```

client=YOUR_IGDB_CLIENT_ID
token=YOUR_IGDB_ACCESS_TOKEN
author=your_name          # optional, default: unknown_writer
output_dir=path/to/output # optional, default: output/

| Variable     | Description                                |
| ------------ | ------------------------------------------ |
| `client`     | IGDB API Client ID (required)              |
| `token`      | IGDB API Bearer Token (required)           |
| `author`     | Your name (optional, default `unknown_writer`) |
| `output_dir` | Output directory (optional, default `output`) |

## Usage

```bash
# Generic mode (any IGDB game)
uv run python -m src.main <update_igdb_id>

# With a module
uv run python -m src.main --module <module_name> <game_key> <update_igdb_id>

# Override output directory
uv run python -m src.main --output /path/to/dir <update_igdb_id>
```

The generated article is saved in the `output/` directory by default.

### Examples

```bash
# Generic
uv run python -m src.main 378320

# Mihoyo module
uv run python -m src.main --module mihoyo genshin 378320
uv run python -m src.main --module mihoyo starrail 123456
uv run python -m src.main --module mihoyo zzz 654321
```

### Options

| Option | Short | Description |
|---|---|---|
| `--module` | `-m` | Module to use (e.g. `mihoyo`) |
| `--output` | `-o` | Output directory (overrides `.env`) |
| `--help` | `-h` | Show help |

### Output priority for `output_dir`

1. `--output` CLI flag
2. `output_dir` in `.env`
3. `output/` (default)

## Available modules

### `mihoyo`

For HoYoverse games (Genshin Impact, Honkai: Star Rail, Zenless Zone Zero).

Fetches update news articles from the Ennead API, adds banners and game-specific links.

| Game key | Game |
|---|---|
| `genshin` | Genshin Impact |
| `starrail` | Honkai: Star Rail |
| `zzz` | Zenless Zone Zero |

## Creating a module

Create a new directory under `src/modules/` and subclass `BaseModule`:

```python
from ..base import BaseModule

class MyModule(BaseModule):
    def get_available_games(self):
        ...
    def get_game_config(self, game_key):
        ...
    def fetch_news_article(self, game_config, version_keywords):
        ...
    def filter_version_keywords(self, keywords):
        ...
    def prepare_extra_context(self, game_config, news_article):
        ...
```

Then register it in `src/modules/__init__.py`:

```python
MODULES = {
    "mihoyo": MihoyoModule,
    "mymodule": MyModule,
}
```
