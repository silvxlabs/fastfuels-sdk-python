# FastFuels SDK documentation

This site is built with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
and versioned with [mike](https://github.com/jimporter/mike). The header
has a version dropdown with two entries, mirroring the FastFuels
platform docs: **v1** (the current default SDK, alias `latest`) and
**v2 (Beta)** (the `fastfuels_sdk.v2` subpackage).

## Layout

| Path | What it is |
|---|---|
| `docs/v1/` | v1 SDK docs — frozen alongside the v1 SDK (bugfix-level edits only) |
| `docs/v2/` | v2 SDK docs — new documentation lands here |
| `docs/v1/SUMMARY.md`, `docs/v2/SUMMARY.md` | Each version's nav (mkdocs-literate-nav) |
| `docs/v1/stylesheets/extra.css`, `docs/v2/stylesheets/extra.css` | Duplicates by construction — edit both |
| `mkdocs.yml` (repo root) | One config for both versions: `DOCS_DIR` picks the tree (default `docs/v1`) |
| `docs/deploy.sh` | The docs entry point: build, serve, deploy |

## Launch the docs server

The full site, version dropdown included, at <http://localhost:8000>:

```bash
./docs/deploy.sh
```

This builds both versions onto your **local** `gh-pages` branch and
serves it with mike (`git branch -D gh-pages` discards the preview).

For quick edits to one version, plain mkdocs gives live reload:

```bash
uv run mkdocs serve                     # v1
DOCS_DIR=docs/v2 uv run mkdocs serve    # v2
```

> [!NOTE]
> The version dropdown only exists under mike — plain `mkdocs serve`
> shows a single version and logs a `versions.json` 404. That's
> expected, not a bug.

## Deploy

```bash
./docs/deploy.sh deploy
```

Publishes both versions to `gh-pages` on origin. The docs workflow
(`.github/workflows/docs.yml`) runs the same command on each GitHub
release (or manually via workflow_dispatch).
