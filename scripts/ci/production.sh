#!/bin/bash
ACTIVE_PROJECT=sources/zola-linkita

echo "Updating submodule $ACTIVE_PROJECT..."
git submodule update --init --recursive

echo "Building the project in production mode..."
cd $ACTIVE_PROJECT
zola build --base-url $URL