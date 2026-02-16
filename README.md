# igdb-data-py

Fetch game data from the [IGDB API](https://api-docs.igdb.com/) and generate JSON files for a blog.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- An IGDB API client ID and access token ([Twitch developer portal](https://dev.twitch.tv/console))

## Installation

```bash
uv sync
```

## Configuration

Copy the `.env.template` file and fill in your credentials:

```bash
cp .env.template .env
```

| Variable     | Description                                |
| ------------ | ------------------------------------------ |
| `client`     | IGDB API Client ID (required)              |
| `token`      | IGDB API Bearer Token (required)           |
| `game`       | IGDB Game ID (optional)                    |
| `output_dir` | Output directory (optional, default `output`) |

## Usage

```bash
# Game ID from .env
uv run python -m src.main

# Game ID as argument (overrides .env)
uv run python -m src.main 1942

# Custom output directory
uv run python -m src.main 1942 -o static
```

The generated JSON file is saved in the `output/` directory by default.
