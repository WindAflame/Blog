#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

if [ ! -f ".env" ]; then
    echo "Error: .env file not found"
    echo "Please copy .env.example to .env and add your IGDB credentials"
    exit 1
fi

echo "Installing dependencies..."
uv pip install -e . -q

if [ ! -d ".venv/lib/python"*"/site-packages/playwright/driver" ]; then
    echo "Installing Playwright browsers..."
    uv run playwright install chromium
fi

echo "Running article generator..."
uv run generate-article "$@"
