#!/usr/bin/env bash
#
# Build the versioned docs — v1 and v2 mike snapshots — and serve or publish.
#
#   ./scripts/docs.sh          build both versions, then serve the full site
#                              (version selector included) at localhost:8000
#   ./scripts/docs.sh deploy   publish both versions to gh-pages on origin
#
# mike snapshots each version onto the gh-pages branch and maintains the
# versions.json that powers the header version selector; plain
# `mkdocs serve` can only ever show one version (and 404s versions.json).
# Without `deploy`, the snapshots are committed to your local gh-pages
# branch only — `git branch -D gh-pages` discards them.
#
# Version labels mirror the FastFuels-Web docs (docs.fastfuels.silvxlabs.com).

set -euo pipefail
cd "$(dirname "$0")/.."

push=""
case "${1:-serve}" in
  serve) ;;
  deploy) push="--push" ;;
  *)
    echo "usage: $0 [deploy]" >&2
    exit 1
    ;;
esac

uv run --group docs mike deploy $push --update-aliases v1 latest --title "v1"
DOCS_DIR=docs/v2 uv run --group docs mike deploy $push v2 --title "v2 (Beta)"
uv run --group docs mike set-default $push latest

if [[ -z "$push" ]]; then
  uv run --group docs mike serve
fi
