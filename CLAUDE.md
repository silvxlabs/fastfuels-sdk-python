# Claude Code Guidelines

## Attribution

Do NOT add "Co-Authored-By: Claude", "Generated with Claude Code", or any other
AI-attribution lines to commit messages, PR descriptions, or GitHub issues.

## Documentation

FastFuels has two documentation properties that must stay in concert:

- **This repo (`docs/`)** — the Python SDK docs (mkdocs-material + mike,
  published to silvxlabs.github.io/fastfuels-sdk-python). Scope: how to use
  FastFuels **from Python** — SDK how-to guides, SDK tutorials, migration
  guides, and the mkdocstrings API reference.
- **FastFuels-Web `documentation/`** (sibling repo) — the platform docs at
  docs.fastfuels.silvxlabs.com (Astro/Starlight). Scope: the web
  application, the HTTP API (language-agnostic: curl + raw requests), and
  **all concept explanations**.

Division of responsibility: platform concepts (what a domain is, how grids
work, why a design is the way it is) are explained once, in the platform
docs — the SDK docs link to docs.fastfuels.silvxlabs.com rather than
duplicating them. The SDK docs own Python idioms, signatures, and
SDK-specific behavior. Cross-link in both directions; never copy content
between the two.

### Diátaxis

Both properties follow the Diátaxis framework (reference copy:
`FastFuels-Web/documentation/diataxis.rst`). Every page is exactly ONE of
four kinds — decide which before writing; if a page wants to be two kinds,
split it:

- **Tutorial** — learning by doing. First-person plural ("we'll create…"),
  prerequisites up front, expected output shown at each step, reliable
  end-to-end. No explanation digressions — link instead.
- **How-to guide** — a goal, for a competent user. Conditional imperatives
  ("To create a domain from a file, …"). Action only: no teaching, no
  background. Opens with a short Prerequisites section.
- **Reference** — neutral facts. In this repo it is generated from
  docstrings via mkdocstrings; do not hand-write opinions into it.
- **Explanation** — the "why". Belongs in the platform docs unless it is
  SDK-specific (e.g. the v1→v2 migration guide's what-changed sections).

### Docstrings are user-facing reference documentation

mkdocstrings renders docstrings directly into the published Reference
pages. A docstring describes what the object does, parameters, returns,
raises, and examples — nothing else. No editorial or comparative
commentary (no v1-vs-v2 asides, no GitHub issue references, no design
rationale). Migration notes belong in `docs/v2/guides/migration.md`;
rationale and issue references belong in `#` code comments.

### Conventions

- Version labels mirror the platform docs: **"v1"** (alias `latest`) and
  **"v2 (Beta)"** — set as mike titles in `.github/workflows/docs.yml`.
- One `mkdocs.yml` builds both versions: `DOCS_DIR` selects `docs/v1`
  (default) or `docs/v2`; each tree owns its nav in a `SUMMARY.md`
  (literate-nav). Versions deploy as independent mike snapshots picked
  from the header version selector.
- `docs/v1/stylesheets/extra.css` and `docs/v2/stylesheets/extra.css` are
  duplicates by construction — edit both or the version snapshots diverge.
- Code examples must be real: verified against the live API (the live test
  suite in `tests/` is the verification path), with realistic output —
  never hand-written response shapes.
- Use admonitions (`!!! tip` / `warning` / `danger`) instead of bold
  "Note:" prose; use content tabs (`=== "v1"` / `=== "v2"`) for
  side-by-side variants; v2 pages open with the `!!! warning "Beta"`
  admonition.
- `docs/v1/` is frozen alongside the v1 SDK (bugfix-level edits only);
  new documentation lands in `docs/v2/`.
