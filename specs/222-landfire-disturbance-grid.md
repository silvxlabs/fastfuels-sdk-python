# Spec: LANDFIRE Limited Annual Disturbance grid creator (#222)

Issue: https://github.com/silvxlabs/fastfuels-sdk-python/issues/222
Go-ahead: approved by the maintainer on 2026-09-08. Ships in SDK v0.23.0 together with #221.

## Goal

Expose the LANDFIRE Limited Annual Disturbance (LDist) grid endpoint through the hand-written
v2 SDK layer, so users can call `ff.grids.create_disturbance_grid_from_landfire(domain, ...)`
instead of reaching into the generated client.

## API contract (live on prod, already in `fastfuels_sdk/v2/client_library/`)

- Endpoint: `POST /domains/{domain_id}/grids/disturbance/annual/landfire`
  (generated module `client_library/api/grids/create_landfire_disturbance.py`).
- Request model `CreateLandfireDisturbanceRequest`: the standard source-grid base
  (`name`, `description`, `tags`, `modifications`, `extent_buffer_cells`, `alignment`) plus
  `version: LandfireDisturbanceVersion` (enum; only `"2025"` today; server default when omitted).
  Always fetched on demand from LANDFIRE Product Service; there is no staged national release.
- Response: a normal `Grid` (201) with one categorical band, key `annual_disturbance`, no unit.

## Behaviour

- Signature mirrors `create_canopy_fuel_grid_from_landfire` minus `bands`:
  `create_disturbance_grid_from_landfire(domain, version=None, output_resolution_m=None, align_to=None, align=None, resampling=None, extent_buffer_cells=0, name="", description="", tags=None, modifications=None) -> Grid`.
- `version` is a string coerced through `LandfireDisturbanceVersion`; `None` leaves it UNSET.
- Alignment and resampling go through the existing `_build_alignment` helper unchanged.
  The band is categorical, so the docstring steers users to `resampling="nearest"` as the
  FBFM40 creator does; the SDK does not force it.
- Exported from `fastfuels_sdk.v2.grids.__all__`.

## Out of scope

- No coverage-check method (the API has no coverage endpoint for this product).
- No changes to the generated client library (never hand-edit it).
- No new docs page; one section in the existing creating-grids guide.

## Acceptance

- Live: creating the grid on the shared test domain returns a pending/running Grid in the
  domain, and the completed grid has exactly one band with key `annual_disturbance`.
- Unit: the request body sent to the endpoint carries `version`, `alignment`, and metadata
  exactly as passed, and omits `version` when not given.
- `uv run pre-commit run --files <changed files>` passes.
- No `Co-Authored-By` / generated-by lines anywhere (repo rule in CLAUDE.md).
