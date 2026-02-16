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

| Variable | Description            |
| -------- | ---------------------- |
| `client` | IGDB API Client ID     |
| `token`  | IGDB API Bearer Token  |
| `game`   | IGDB Game ID to fetch  |

## Usage

```bash
uv run python -m src.main
```

Or via the entry point:

```bash
uv run igdb-data
```

The generated JSON file is saved in the `static/` directory.

## Project structure

```
igdb-data-py/
├── src/
│   ├── __init__.py        # Package marker
│   ├── main.py            # Entry point, orchestration
│   ├── config.py          # Configuration, constants, logging
│   └── igdb_client.py     # IGDB client: API requests + transformations
├── .env.template
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock
```
