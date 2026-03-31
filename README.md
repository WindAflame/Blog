# EWA's Blog

[![Netlify Status](https://api.netlify.com/api/v1/badges/3121d731-fd3e-4d7e-8eaf-49f5a834613f/deploy-status)](https://app.netlify.com/projects/ewa-blog/deploys)

## Welcome to my blog's source project

Here you'll find my blogs in the form of branches.
Below is the list of blogs:

|Theme|Version|Status|
|---|---|---|
|[hugo-initio](https://github.com/WindAflame/hugo-initio)|?|Abandoned|
|[hugo-plate](https://github.com/zeon-studio/hugoplate)|?|Abandoned|
|[hugo-resume](https://github.com/eddiewebb/hugo-resume)|?|Abandoned|
|[hugo-stack](https://github.com/CaiJimmy/hugo-theme-stack)|?|Abandoned|
|[zola-linkita](https://github.com/salif/linkita)|[?]()|Deployed|

_I'm currently working on centralizing the articles so that they are compatible between each of my active blogs._

## Getting Started for Development

### Prerequisites

- **Git** with submodule support
- **Zola** v0.22.1 - [Installation guide](https://www.getzola.org/documentation/getting-started/installation/)

### Setup

1. Clone the repository with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/WindAflame/Blog.git
   cd Blog
   ```

2. If you already cloned without submodules, initialize them:
   ```bash
   git submodule update --init --recursive
   ```

3. Navigate to the active project and start the development server:
   ```bash
   cd sources/zola-linkita
   zola serve --drafts
   ```

The site will be available at `http://127.0.0.1:1111/` with live reload.

### Project Structure

```
Blog/
├── sources/           # Blog sources (submodules)
│   └── zola-linkita/  # Active blog (Zola)
├── scripts/
│   ├── ci/            # CI/CD scripts for Netlify
│   └── gen-igdb-article-py/  # IGDB article generator
└── docs/
```

## Extra Features / Scripts

This project includes Python scripts to work with [IGDB](https://www.igdb.com/) (Internet Game Database) API. Both require an IGDB API account to obtain `client_id` and `token` credentials.

### Generate Blog Articles from IGDB

Automatically generates Markdown blog posts for games using IGDB data and Jinja2 templates. Useful for creating consistent game review or showcase articles.

1. Install **Python 3.14+** and **[uv](https://docs.astral.sh/uv/)**
2. Setup the environment:
   ```bash
   cd scripts/gen-igdb-article-py
   cp .env.example .env
   # Edit .env with your IGDB API credentials
   uv sync
   ```

### Fetch IGDB Data for Offline Use

Downloads game metadata from IGDB and saves it as JSON files. This allows your blog to display game information without making API calls at runtime.

1. Install **Python 3.13+** and **[uv](https://docs.astral.sh/uv/)**
2. Setup and run:
   ```bash
   cd scripts/igdb-data-py
   cp .env.template .env
   # Edit .env:
   #   client=<your_client_id>
   #   token=<your_bearer_token>
   #   game=<igdb_game_id>
   uv sync
   uv run python main.py
   ```

The game data will be saved to `static/<game_id>.json`.
