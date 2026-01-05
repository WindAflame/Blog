#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

build_zola() {
    local base_url=$1
    local extra_flags=$2

    validate_config

    echo "Updating submodules..."
    git submodule update --init --recursive

    echo "Building with Zola..."
    cd "$ACTIVE_PROJECT_PATH"

    if [ -n "$extra_flags" ]; then
        zola build --base-url "$base_url" $extra_flags
    else
        zola build --base-url "$base_url"
    fi

    echo "Build completed successfully"
}

main() {
    local environment=$1
    local base_url=$2
    local extra_flags=$3

    case "$BUILDER_TYPE" in
        zola)
            build_zola "$base_url" "$extra_flags"
            ;;
        *)
            echo "Error: Unknown builder type '$BUILDER_TYPE'"
            exit 1
            ;;
    esac
}

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <environment> <base_url> [extra_flags]"
    echo "Example: $0 production https://example.com"
    echo "Example: $0 develop https://deploy-preview.netlify.app --drafts"
    exit 1
fi

main "$@"
