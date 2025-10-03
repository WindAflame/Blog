#!/bin/bash
ACTIVE_PROJECT=sources/zola-linkita
echo "Check if submodule has new content"
if git diff --quiet HEAD^ HEAD -- "$ACTIVE_PROJECT"; then
    echo "Submodule $ACTIVE_PROJECT has NOT been updated."
else
    echo "Submodule $ACTIVE_PROJECT has been updated."
    git submodule update --init --remote
    echo "Build the project in develop ..."
    zola build --base-url $DEPLOY_PRIME_URL --drafts
fi