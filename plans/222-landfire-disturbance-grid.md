# Plan: LANDFIRE Limited Annual Disturbance grid creator (#222)

Branch: `222-landfire-disturbance-grid` (off `main`). One PR, `Closes #222`.

Project commands (run from the repo root):
- Load live credentials: `set -a; source .env; set +a` (never print or commit them).
- Tests: `uv run pytest tests/v2/test_grids.py -k disturbance -v -p no:cacheprovider`
- Lint: `uv run pre-commit run --files <files>`
- Do NOT run `generate_client.sh`; the generated client already has the endpoint.

## Checklist

- [ ] 1. SDK method — `fastfuels_sdk/v2/grids.py`
  Add `create_disturbance_grid_from_landfire` next to the other LANDFIRE creators, modelled on
  `create_canopy_fuel_grid_from_landfire` (same argument order, `_build_alignment`, `_opt`,
  `expect(response, HTTPStatus.CREATED)`, `Grid._from_model`). Import
  `create_landfire_disturbance` from the generated api package and
  `CreateLandfireDisturbanceRequest`, `LandfireDisturbanceVersion` from the generated models.
  Add the name to `__all__`. Docstring in the module's NumPy style: what it does, parameters,
  returns; mention the band is categorical and `resampling="nearest"` is the sensible choice.
  No editorial or issue references in the docstring.
  Acceptance: `python -c "import fastfuels_sdk.v2 as ff; ff.grids.create_disturbance_grid_from_landfire"` imports;
  pre-commit passes.

- [ ] 2. Tests — `tests/v2/test_grids.py`  (blocked by 1)
  Add `TestCreateDisturbanceGridFromLandfire` beside `TestCreateCanopyFuelGridFromLandfire`:
  (a) live `test_create` on the shared `test_domain` fixture with `output_resolution_m=30`,
  `resampling="nearest"`, asserting id/domain/pending-or-running, then `grid.delete()`;
  (b) live `test_completed_band` that waits and asserts the band keys are exactly
  `{"annual_disturbance"}`, then deletes; (c) a monkeypatch unit test (pattern: the existing
  `fake_create` tests in this file) asserting the serialized body for
  `version="2025", output_resolution_m=30, resampling="nearest", name="x"` and that `version`
  is absent when not passed.
  Acceptance: the `-k disturbance` run is green against prod with `.env` loaded.

- [ ] 3. Docs — `docs/v2/guides/creating-grids.md`  (blocked by 1)
  Add a short subsection under the LANDFIRE grids area (near the topography / canopy LANDFIRE
  sections) titled "Disturbance grids", with one code block calling the new function with
  `resampling="nearest"` and one sentence that the single `annual_disturbance` band holds
  categorical LDist codes fetched on demand from the LANDFIRE Product Service. How-to voice,
  no background explanation; follow the guide's existing conventions.
  Acceptance: the section renders in the guide and links nothing that does not exist.

- [ ] 4. Close out  (blocked by 2, 3)
  Self-review the whole diff against `main`; run the full `tests/v2/test_grids.py` module live
  once; delete `specs/` and `plans/` for this feature in the final commit; mark the PR ready
  with `Closes #222` in the body. No attribution lines in commits or the PR.
