# v2 SDK — API Design (WORKING DRAFT)

> Scratch design notes for the v2 SDK refactor (umbrella #176; grids = #178).
> **Temporary** — delete or fold into real docs before merge.
> Captures the surface settled in the 2026-06 design discussion.

## Decision: hybrid — functional creation, method-based instances

Two separate decisions, each resolved differently:

1. **Creation lives in module-level functions.** Every class-home was rejected:
   classmethod on the resource (`Feature.create_osm_road(domain.id)`, the
   original complaint), method on `Domain` (God-class), method on a collection
   object (`domain.grids.topography.from_3dep()`, the object tree). Functions
   are what's left, and they read cold.
2. **Everything you do with a resource you already hold is a method** on the
   returned record — `grid.wait()`, `grid.to_xarray()`, `trees.voxelize(...)`,
   `grid.resample(...)`, `grid.delete()`. Methods read naturally, chain, answer
   "what can I do with this?" via `grid.<tab>`, and are mostly what the shipped
   class-based `domains.py`/`features.py` already have — so the migration is
   "move creation off the classes into functions," not a rewrite, and there's
   no split-brain.

The rule a user learns: **don't have the resource yet → function from the
domain; have it → method on it.**

Rejected wholesale: fully object-navigation (`domain.grids.topography.…`),
fully functional (free `ff.wait(grid)` / `ff.to_xarray(grid)` — loses chaining
and the shipped methods), typed spec objects, fluent builders, a "fuelscape"
façade.

## Access pattern (locked)

One import; reach everything through the package namespace (`np`/`pd`/`gpd`
idiom):

```python
import fastfuels_sdk as ff
```

- **Creators are module-qualified functions:**
  `ff.grids.create_topography_grid_from_3dep(domain, …)`,
  `ff.features.create_road_feature_from_osm(domain)`. Scoped tab-completion:
  `ff.grids.<tab>`.
- **Held-resource ops are methods:** `grid.wait()`, `grid.to_xarray()`,
  `trees.voxelize(…)`, `grid.resample(…)`, `grid.export(…)`, `grid.delete()`.
- **Cross-cutting helpers are top-level functions** (operate on many / build
  descriptors / start from nothing): `ff.wait_all([...])`, `ff.mask(...)`,
  `ff.list_grids(domain)`, `ff.list_all_grids()`, `ff.get_grid(domain, id)`,
  `ff.Domain`, `ff.set_api_key`. (Fuller modifications vocab — `modify`,
  `within`, `remove`, `thin_to_*` — lives in `ff.modifications`, least-settled.)
- `ff.<module>` is a **module, not an object** — no God-class. Not the rejected
  object tree.
- The resource noun stays **in the create-function name** (`…_grid_…`,
  `…_feature_…`) even though the module repeats it, so it reads cold under a
  bare import too.

## Guiding principles

1. **Read it cold** — one call, you know exactly what it does. No jargon, no
   magic values, units in names (`_m`), real domain nouns, named arguments.
2. **The shape encodes where the input comes from:** `create_<kind>_<resource>_from_<source>(domain, …)`
   = external dataset; `create_<resource>_from_<file>(domain, path)` = your
   file; `create_<resource>(domain, …)` = you supply values; `resource.<verb>()`
   = transform something you hold.
3. **Resource noun in every `create_*` name** (`grid`/`feature`/`inventory`).
4. **Concrete kind nouns**, grounded in the grid's bands — never vague
   umbrellas (`canopy` → `canopy_height` vs `canopy_fuel`).

## Wait / job model (decision: A — explicit)

API is async-job (create → poll → terminal). Surfaced explicitly:

- **Creation never blocks, never auto-waits** — returns a *pending* record.
  Lets you fan out and join (the v1 `export_roi` pattern).
- `grid.wait(timeout=None, verbose=False)` — method; blocks to terminal,
  updates & returns self (chains). `timeout=None` waits indefinitely; the job
  runs server-side regardless, so a bounded timeout is resumable.
- `ff.wait_all([...])` — function; join many, raises naming the first failure.
- **Deriving from a still-pending resource raises** a clear error. No hidden
  block.
- Failure → `JobFailedError(code, message, suggestion)`. Progress quiet by
  default; `verbose=True`.

## Resolution & alignment (verified against the models)

**v2 moved resolution off the domain and onto each grid** (v1 set it on the
domain). `Domain` has only `pad_to_resolution` (optional footprint snapping).
Per-creator:

- **2D source/derive grids** (`topography×2`, `canopy_height×2`, `canopy_fuel`,
  `fuel_model/fbfm40`, `resample`, `rasterize`) carry an **`alignment`** union.
  All three targets also hold `resolution: float` (horizontal) and an optional
  `method` (resampling). Friendly mapping:
  - `output_resolution_m=N` → `target="domain"` (anchor to domain origin at N m) — default.
  - `align_to=<grid>` → `target="grid"` (match that grid's lattice).
  - `align="native"` → `target="native"` (keep source pixels).
  - `resampling=<m>` → `method`; one of `average / bilinear / cubic /
    cubic_spline / lanczos / min / max / median / mode / first_quartile`.
- **`create_uniform_grid`**: direct `resolution: float` → `resolution_m=`.
- **`voxelize`** (3D): direct `resolution: Resolution3D = {horizontal, vertical}`
  (horizontal isotropic x/y, vertical independent), **no alignment** →
  `horizontal_resolution_m=` + `vertical_resolution_m=`.
- **`create_fuel_grid_from_fbfm40_lookup`, geotiff/netcdf upload**: no resolution/alignment — inherit
  the source grid's lattice (lookup) or the file (uploads).
- **`landfire_fccs`** reached alignment parity with the other LANDFIRE creators
  in FastFuels-API-v2 #358 (it now carries `alignment` + `extent_buffer_cells`),
  resolving the earlier asymmetry.

## Conventions

- Every creator also accepts `name=`, `description=`, `tags=`,
  `modifications=[...]` (applied server-side after build; `modifications` is a
  real field on grid creators *and* the FBFM40 lookup / `rasterize`).
- **Data out (methods, hide chunk/partition plumbing + signed-URL handshake):**
  `grid.to_xarray()`, `grid.to_numpy(band)`, `feature.to_geodataframe()`.
- **Generic methods on any record:** `.wait()`, `.refresh()`, `.update(...)`,
  `.delete()`.

## Module layout

```
fastfuels_sdk/
  __init__.py     set_api_key, Domain, wait_all, mask, basal_area_treatment, list_*, get_*, ...
  domains.py      Domain (record + from_* + methods), list_domains
  features.py     create_*_feature_from_* (fns); Feature record + methods
  grids.py        create_*_grid_from_* (fns; incl. create_fuel_grid_from_fbfm40_lookup);
                  Grid record + methods (wait/to_xarray/resample/duplicate/
                  apply_modifications/band_summary/export/...)
  inventories.py  create_tree_inventory_from_* (fns; pim/chm/file/gdam); Inventory + methods
                  (duplicate/apply_modifications/apply_treatments/voxelize/export/...)
  point_clouds.py create_point_cloud_from_file (fn); PointCloud record + methods (upload-only)
  exports.py      create_quicfire_export (fn); Export record + methods
  modifications.py mask() -> GridModification
  treatments.py   basal_area_treatment()/diameter_treatment() -> Inventory*Treatment
  _uploads.py     put_upload(spec, path) — shared signed-upload helper (grids/inventories/point_clouds)
  _jobs.py        wait()/wait_all()/JobFailedError
```

## Features — 10 endpoints (rewrite creation only; keep instance methods)

| API endpoint | SDK surface | Kind |
|---|---|---|
| `create_osm_road_feature` | `ff.features.create_road_feature_from_osm(domain)` | fn |
| `create_osm_water_feature` | `ff.features.create_water_feature_from_osm(domain)` | fn |
| `create_layerset` | `ff.features.create_layerset_feature_from_geojson(domain, geojson)` · `…_from_geodataframe(domain, gdf)` | fn |
| `get_feature` | `ff.get_feature(domain, feature_id)` · `feature.refresh()` | fn / method |
| `update_feature` | `feature.update(…)` | method |
| `delete_feature` | `feature.delete()` | method |
| `list_features` | `ff.list_features(domain)` | fn |
| `list_features_cross_domain` | `ff.list_all_features()` | fn |
| `get_feature_data_metadata` + `…_partition` | `feature.to_geodataframe()` | method (hides paging) |

## Grids — 26 endpoints (greenfield, #178)

All `create_*_grid_*` functions share an internal `_grid_request_base(...)` +
alignment-translation helper (plain function, not a base class).

**Create from external source (functions)**

| API endpoint | SDK surface |
|---|---|
| `create_3dep_topography` | `ff.grids.create_topography_grid_from_3dep(domain, source_resolution_m=10, output_resolution_m=…)` |
| `create_landfire_topography` | `ff.grids.create_topography_grid_from_landfire(domain, version=…)` |
| `create_landfire_canopy` | `ff.grids.create_canopy_fuel_grid_from_landfire(domain, version=…)` |
| `create_meta_chm` | `ff.grids.create_canopy_height_grid_from_meta(domain, version=…)` |
| `create_naip_chm` | `ff.grids.create_canopy_height_grid_from_naip_chm(domain)` |
| `create_landfire_fbfm40` | `ff.grids.create_fuel_model_grid_from_landfire_fbfm40(domain, version=…, remove_non_burnable=…)` |
| `create_landfire_fccs` | `ff.grids.create_fuel_model_grid_from_landfire_fccs(domain, version=…, remove_bare_ground=…, output_resolution_m=…)` |
| `create_treemap` | `ff.grids.create_pim_grid_from_treemap(domain, version=…, bands=[…])` (PIM = Plot Imputation Map; bands tm_id/plt_cn) |

**From your file / generated (functions)**

| `create_geotiff_upload` | `ff.grids.create_grid_from_geotiff(domain, path, bands=[…])` |
| `create_netcdf_upload` | `ff.grids.create_grid_from_netcdf(domain, path)` |
| `create_uniform_grid` | `ff.grids.create_uniform_grid(domain, resolution_m=…, bands={…})` |

**Transform a resource you hold**

A transform is a *method* when it applies to any instance of the resource
(every grid can resample/export; every inventory can voxelize). A transform
that only makes sense for a *particular kind* of grid is a **function** instead,
so it never appears on a grid that cannot perform it (the alternative — a method
that raises for the wrong grid type — is the wart this avoids). The FBFM40
lookup is the only such case today: it needs a grid carrying `fbfm` codes.

| `create_fbfm40_lookup` | `ff.grids.create_fuel_grid_from_fbfm40_lookup(fbfm_grid, bands=[…])` (fn — FBFM40-only) |
| `create_tree_inventory_grid` | `inventory.voxelize(horizontal_resolution_m=…, vertical_resolution_m=…, bands=…)` (method) |
| `create_resample` | `grid.resample(output_resolution_m=… / align_to=…, resampling=…)` (method) |
| `create_layerset_rasterize` | `layerset.rasterize(output_resolution_m=…, overlap_method=…)` (method) |

**Export**

| `create_grid_export` | `grid.export(format="geotiff")` → Export (method) |
| `create_quicfire_export` | `ff.exports.create_quicfire_export(domain, topography=…, surface=…, canopy=…)` (fn — assembled from many) |

**Lifecycle** · `get_grid` → `ff.get_grid(domain, grid_id)` + `grid.refresh()` · `update_grid` → `grid.update(…)` · `delete_grid` → `grid.delete()` · `list_grids` → `ff.list_grids(domain)` · `list_grids_cross_domain` → `ff.list_all_grids()`

**Data out** · `get_chunk_metadata` + `get_grid_data_json` + `get_grid_data_binary` → `grid.to_xarray()` / `grid.to_numpy(band)` (chunk reassembly + signed-URL hidden)

**Utility** · `check_3dep_coverage` → `ff.grids.check_3dep_coverage(domain)`

(`create_treemap` is a first-class grid source — see `create_pim_grid_from_treemap` in the "Create from external source" table above. It is distinct from `create_tree_inventory_grid` → `inventory.voxelize`, which produces a 3D voxel grid from an inventory.)

## v1 workflow findings (from mining `docs/v1`)

- **Masking simplifies.** v1's separate feature grid + `feature_masks=["road",
  "water"]` becomes `modifications=[ff.mask(feature)]` on the grids that need it
  (the API `GridModification` references a Feature by id). One fewer resource.
- **`to_geodataframe`/`to_xarray` erase the pagination ritual** — v1's
  `get_data` → `get_all_data` → `from_features` collapses to `feature.to_geodataframe()`.
- **Custom road/water is a model change to document:** v1 typed
  `create_road_feature_from_geodataframe`; v2 does road/water from OSM only, so
  bring-your-own geometry goes through `create_layerset_feature_from_*`.
- **`export_roi` wants a v2 home** — a plain function, not a façade.

## Open / flagged

- ~~`landfire_fccs` alignment/resolution asymmetry~~ — resolved (FastFuels-API-v2
  #358 added `alignment` + `extent_buffer_cells`; the SDK creator now exposes them).
- Single-grid export is a method (`grid.export`) but the QUIC-Fire bundle is a
  function (`ff.exports.create_quicfire_export`) — consistent with the rule
  (one held resource → method; assembled-from-many → function), but worth a look.
- Modifications/treatments vocab (`mask`/`modify`/`within`/`thin_to_*`) — now
  settled: builders ship for all three — `mask` (grids), `basal_area_treatment`/
  `diameter_treatment` (inventory treatments), and `tree_attribute`/`tree_within`/
  `remove_trees`/`modify_trees` (inventory modifications). `tree_within` builds an
  `InventoryFeatureSpatialCondition`, which treatments' `conditions=` also accept;
  geometry/expression conditions remain a raw pass-through.
- Returned-record implementation (wrap generated attrs model vs clean dataclass)
  — parked; shows up on every record.

## Post-regen additions (2026-06-12)

Wired after re-syncing the client to the live spec (FastFuels-API-v2 #358 +
later merges). Each new resource/endpoint kept to the settled rules above.

- **point_clouds** — new upload-only resource: `PointCloud` record (lifecycle
  only — no transforms/data-out), `create_point_cloud_from_file(domain, path,
  point_cloud_type=)`, `list_point_clouds`/`get_point_cloud`. Nothing else
  sources from a point cloud yet.
- **Inventory treatments** — `Inventory.apply_treatments([...])` (in-place
  re-derive; unlike `apply_modifications` it does *not* hit #333) + the
  `ff.basal_area_treatment`/`ff.diameter_treatment` builders (`treatments.py`).
- **GDAM** — `create_tree_inventory_from_gdam(domain, source_inventory,
  impute_columns=)`. A *create* (new inventory) → a function in the
  `create_tree_inventory_from_*` family, **not** a method — same call as the
  fbfm40-lookup precedent (derive-a-new-resource = function).
- **Grid** gained `duplicate` (byte-copy clone, mirrors `Inventory.duplicate`),
  `apply_modifications` (in-place re-derive; grid `modifications` list is *not*
  echoed in the pending response, unlike inventories), and `band_summary(band)`
  (cheap per-band stats from the new `Band.summary`; shares a `_band` helper
  with `to_numpy`).
- **FCCS** reached alignment parity (#358) — creator now takes the alignment kwargs.
- **Uploads** — one shared `_uploads.put_upload(spec, path)` echoes the
  server's signed `spec.headers` verbatim; replaced the two divergent
  `_put_upload` copies (grids had been missing the GCS content-length-range).

## Post-regen backlog (2026-08-04)

Client re-synced against the live spec: 94 operations, 236 schemas. 19
operations have no SDK surface. Ordered by what unblocks a user workflow.

### Breaking (landed with the regen)

- `get_inventory_data` split into `get_inventory_data_json` (adds
  `json_orientation`) and `get_inventory_data_csv`; `InventoryDataFormat` is
  gone. `Inventory.get_data_partition` now calls the JSON variant — behavior
  unchanged. The CSV variant is unused (see *data out* below).
- FastFuels-API-v2#489 resolved both schema-title collisions at the source.
  `generate_client.sh` now consumes the production spec without patching it.
  The generated domain request model is `GeoJsonFeatureCollection`, and the
  two 3DEP coverage models are `PointCloudThreeDepCoverageResponse` and
  `TopographyThreeDepCoverageResponse`.

### Quotas — cross-cutting, affects every creator

41 of 94 operations can now return **429** with a structured
`QuotaExceededDetail` (`quota`, `current`, `limit`, `window_reset_on`).
`exceptions.py` has no 429 mapping, so today it degrades to a bare
`ApiException`. Needs a `QuotaExceededException` carrying those fields —
`window_reset_on` is what a caller retries on.

- `ff.get_quotas()` / `ff.get_usage()` ← `users/me`, `users/me/usage`
  (`Quotas`, `Usage` per resource type: active/total counts, storage bytes,
  weekly dispatch windows, TTL policy). Top-level functions: owner-scoped,
  no held resource.

### New resource sources

- **3DEP point clouds** — `ff.point_clouds.create_point_cloud_from_3dep(
  domain, datasets=)` + `ff.point_clouds.check_3dep_coverage(domain)`
  (returns `available`, `coverage_fraction`, `estimated_point_count`,
  `point_budget`, `exceeds_point_budget`, per-acquisition `datasets`).
  Mirrors the existing `grids.check_3dep_coverage` pre-flight pattern; this
  is the first non-upload point cloud source.
- **Point cloud → CHM** — `ff.grids.create_canopy_height_grid_from_point_cloud(
  point_cloud, ...)`. First consumer of a point cloud, which closes the
  3DEP → CHM → tree inventory chain entirely inside the SDK.

### New grid creators

- **DUET** — `ff.grids.create_surface_fuel_grid_from_duet(source_grid,
  years_since_burn=, wind_direction=, wind_variability=, bands=,
  calibration=)`. Needs a `duet_calibration(...)` builder in the
  `modifications.py`/`treatments.py` family: `DuetCalibration` nests
  fuel_load/fuel_depth/fuel_moisture → per-fuel-type
  (grass/coniferous/deciduous/litter/all) targets in three shapes
  (constant / max-min / mean-sd).
- **FBFM13** — `create_fuel_model_grid_from_landfire_fbfm13` (version
  2023/2024, `remove_non_burnable=`) and
  `create_fuel_grid_from_fbfm13_lookup` (9 bands), matching the FBFM40 pair.
- **FCCS lookup** — `create_fuel_grid_from_fccs_lookup` (12 bands incl. duff
  and live components). The FCCS *source* creator exists; the lookup that
  turns it into fuel parameters does not.
- **Compose** — `create_grid_from_compose(inputs, select=, compute=)`: grid
  algebra over aliased input bands (`add`/`subtract`/`multiply`/`divide`/
  `min`/`max`/`average`, conditional `select` with `else_`). The largest
  design question in this batch — it is a small DSL, not a creator with
  kwargs, and it needs builders to be usable from Python.

### New export

- **Landscape (LCP)** — `ff.exports.create_landscape_export(...)`: 8-band
  FlamMap/IFTDSS/WFDSS GeoTIFF assembled from 8 named
  `LandscapeFieldSource` (grid_id + band) plus `fire_behavior_fuel_model`
  (fbfm13/fbfm40) and alignment. Assembled-from-many → function, same shape
  as `create_quicfire_export`.

### Records and data out

- `Inventory.forestry_metrics` — new `TreeForestryMetrics` on the inventory
  record (tree_count, basal area/acre, TPA, QMD, dominant FIA species
  groups). Read-only accessor; the parallel of `Grid.band_summary`.
- `Inventory.column_summary(column)` — `Column.summary` is new
  (categorical/continuous), exactly mirroring `Band.summary`; reuse the
  `band_summary` shape.
- `Inventory.to_dataframe` should fetch CSV partitions and `pd.read_csv`
  them instead of rebuilding frames from JSON row lists.
- `get_chunk_metadata` / `get_grid_data_json` stay unwrapped — the binary
  chunk path already covers `to_numpy`/`to_xarray`.

### Account management (deliberately generated-client only)

**Decision (2026-08-04): do not add high-level wrappers for `applications`
or `keys`.** The public SDK consumes an existing API key; application and key
provisioning remain account-console concerns.

The ten generated endpoints remain available in `client_library`, including
the new `Application.tier`/`quota_overrides` fields, but they are not exported
through `fastfuels_sdk.v2`. This keeps one-time key secrets, credential
rotation/revocation, and destructive account operations out of ordinary data
workflows. It also matches v1, where these endpoints exist only in the
generated client and never gained a high-level wrapper.

Revisit this boundary only if programmatic credential provisioning becomes a
supported SDK use case. That work should be designed as a dedicated account
module with explicit secret-handling requirements rather than added piecemeal
to the resource wrappers.
