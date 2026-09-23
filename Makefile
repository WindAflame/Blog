SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

OUTPUT_DIR ?= output

.PHONY: help check-uv install env run clean

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  install   uv sync (installs dependencies into .venv)"
	@echo "  env       Create .env from .env.example if missing"
	@echo "  run       Run the article generator (ARGS=\"...\")"
	@echo "            Generic:      make run ARGS=\"378320\""
	@echo "            With module:  make run ARGS=\"--module mihoyo genshin 378320\""
	@echo "  clean     Remove generated output/ and app.log"

check-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Error: 'uv' is not installed or not in PATH." >&2; \
		echo "Install it: https://docs.astral.sh/uv/getting-started/installation/" >&2; \
		exit 1; \
	}

install: check-uv
	uv sync

env:
	@if [ -f .env ]; then \
		echo ".env already exists, leaving it untouched."; \
	else \
		cp .env.example .env; \
		echo "Created .env from .env.example — fill in your IGDB credentials."; \
	fi

run: check-uv
	uv run python -m src.main $(ARGS)

clean:
	rm -rf "$(OUTPUT_DIR)" app.log
