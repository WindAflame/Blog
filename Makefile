SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

CI_DIR := scripts/ci
GEN_ARTICLE_DIR := scripts/gen-igdb-article-py
IGDB_DATA_DIR := scripts/igdb-data-py

# Override to force a base URL, e.g. `make build URL=https://example.com`
URL ?=

.PHONY: help install check-zola check-uv serve serve-draft build \
        gen-igdb-article-install gen-igdb-article \
        igdb-data-install igdb-data

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Blog (Zola):"
	@echo "  install                    Init submodules and check the Zola install"
	@echo "  serve                      Start the local dev server with live reload"
	@echo "  serve-draft                Start the local dev server, including draft pages"
	@echo "  build                      Build the site (reuses scripts/ci/builder.sh, override with URL=...)"
	@echo ""
	@echo "IGDB scripts:"
	@echo "  gen-igdb-article-install   uv sync for scripts/gen-igdb-article-py"
	@echo "  gen-igdb-article           Run the article generator (ARGS=\"<update_igdb_id>\")"
	@echo "  igdb-data-install          uv sync for scripts/igdb-data-py"
	@echo "  igdb-data                  Run the IGDB data fetcher (ARGS=\"<game_id>\")"

check-zola:
	@command -v zola >/dev/null 2>&1 || { \
		echo "Error: 'zola' is not installed or not in PATH." >&2; \
		echo "Install it: https://www.getzola.org/documentation/getting-started/installation/" >&2; \
		exit 1; \
	}
	@source $(CI_DIR)/config.sh; \
	version=$$(zola --version | awk '{print $$2}'); \
	if [ "$$version" != "$$BUILDER_VERSION" ]; then \
		echo "Warning: zola $$version detected, but this project targets $$BUILDER_VERSION (see $(CI_DIR)/config.sh)." >&2; \
	fi

check-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Error: 'uv' is not installed or not in PATH." >&2; \
		echo "Install it: https://docs.astral.sh/uv/getting-started/installation/" >&2; \
		exit 1; \
	}

install: check-zola
	@echo "==> Initializing submodules"
	git submodule update --init --recursive
	@source $(CI_DIR)/config.sh; validate_config
	@echo "Install complete."

serve: check-zola
	@source $(CI_DIR)/config.sh; validate_config; \
	echo "==> Starting dev server"; \
	cd "$$ACTIVE_PROJECT_PATH" && zola serve

serve-draft: check-zola
	@source $(CI_DIR)/config.sh; validate_config; \
	echo "==> Starting dev server (with drafts)"; \
	cd "$$ACTIVE_PROJECT_PATH" && zola serve --drafts

build: check-zola
	@echo "==> Building site (reusing $(CI_DIR)/builder.sh)"
	bash $(CI_DIR)/builder.sh production "$(URL)"

gen-igdb-article-install: check-uv
	cd $(GEN_ARTICLE_DIR) && uv sync

gen-igdb-article: check-uv
	cd $(GEN_ARTICLE_DIR) && uv run python -m src.main $(ARGS)

igdb-data-install: check-uv
	cd $(IGDB_DATA_DIR) && uv sync

igdb-data: check-uv
	cd $(IGDB_DATA_DIR) && uv run python -m src.main $(ARGS)
