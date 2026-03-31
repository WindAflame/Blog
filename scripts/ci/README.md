# CI Scripts

## Configuration

Edit `config.sh` to change active project:

```bash
ACTIVE_PROJECT_NAME="zola-linkita"
ACTIVE_PROJECT_PATH="sources/zola-linkita"
BUILDER_TYPE="zola"
BUILDER_VERSION="0.22.1"
```

## CI Behavior

- **Production** (master): Builds without drafts
- **Develop**: Builds with `--drafts` flag
- **Preview** (PRs): Builds without drafts

## Local Testing

```bash
export URL="http://localhost:1111"
bash scripts/ci/production.sh

export DEPLOY_PRIME_URL="http://localhost:1111"
bash scripts/ci/develop.sh
```
