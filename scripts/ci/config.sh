#!/bin/bash

ACTIVE_PROJECT_NAME="zola-linkita"
ACTIVE_PROJECT_PATH="sources/zola-linkita"
BUILDER_TYPE="zola"
BUILDER_VERSION="0.22.1"

validate_config() {
    if [ -z "$ACTIVE_PROJECT_PATH" ]; then
        echo "Error: ACTIVE_PROJECT_PATH is not set"
        exit 1
    fi

    if [ ! -d "$ACTIVE_PROJECT_PATH" ]; then
        echo "Error: Project directory $ACTIVE_PROJECT_PATH does not exist"
        exit 1
    fi

    echo "Active project: $ACTIVE_PROJECT_NAME ($BUILDER_TYPE)"
    echo "Project path: $ACTIVE_PROJECT_PATH"
}
