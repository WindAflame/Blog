#!/bin/bash
set -e

echo "=== Initializing Blog Development Environment ==="

# Initialize git submodules
echo "Updating git submodules..."
git submodule update --init --recursive

# Install UV for current user if not available
if ! command -v uv &> /dev/null; then
    echo "Installing UV package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install theme dependencies
echo "Installing Linkita theme dependencies..."
cd sources/zola-linkita/themes/linkita
if [ -f "pnpm-lock.yaml" ]; then
    pnpm install
fi
cd /workspaces/Blog

# Setup Python scripts if .env files exist
echo "Checking Python scripts setup..."

if [ -d "scripts/gen-igdb-article-py" ]; then
    cd scripts/gen-igdb-article-py
    if [ -f "pyproject.toml" ]; then
        echo "Syncing gen-igdb-article-py dependencies..."
        uv sync 2>/dev/null || echo "Note: Run 'uv sync' manually if needed"
    fi
    cd /workspaces/Blog
fi

if [ -d "scripts/igdb-data-py" ]; then
    cd scripts/igdb-data-py
    if [ -f "pyproject.toml" ]; then
        echo "Syncing igdb-data-py dependencies..."
        uv sync 2>/dev/null || echo "Note: Run 'uv sync' manually if needed"
    fi
    cd /workspaces/Blog
fi

echo ""
echo "=== Environment Ready ==="
echo ""
echo "Available commands:"
echo "  - Start Zola dev server:  cd sources/zola-linkita && zola serve --drafts"
echo "  - Build for production:   bash scripts/ci/production.sh"
echo "  - Build with drafts:      bash scripts/ci/develop.sh"
echo ""
echo "Python scripts (requires IGDB API credentials in .env):"
echo "  - Generate article:       cd scripts/gen-igdb-article-py && uv run python main.py"
echo "  - Fetch IGDB data:        cd scripts/igdb-data-py && uv run python main.py"
echo ""
