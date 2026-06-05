# Migrating from v1 to v2

The FastFuels v1 and v2 APIs are separate live services. Resources created
in v1 are not visible to v2 (and vice versa) — migrating a workflow means
creating new resources through v2. The SDK ships both interfaces as
versioned subpackages, so you can run them side by side and migrate one
workflow at a time:

```python
from fastfuels_sdk import Domain      # v1 (the default today)
from fastfuels_sdk.v1 import Domain   # v1, explicit
from fastfuels_sdk.v2 import Domain   # v2
```

Both subpackages read the same `FASTFUELS_API_KEY` environment variable.

## At a glance

| v1 | v2 | What changed |
|---|---|---|
| `Domain.from_geojson(..., horizontal_resolution=2.0, vertical_resolution=1.0)` | `Domain.from_geojson(..., pad_to_resolution=2.0)` | Resolution belongs to grids now; domains only pad their extent for grid alignment |
| `domain.export()` | grid exports | No domain-level export in v2; data exports hang off grids |
| — | `Domain.preview`, `Domain.get_lattice`, `reproject_geojson` | New domain capabilities |
| `Grids`, `SurfaceGrid`, `TreeGrid`, `TopographyGrid`, `FeatureGrid` + builders | unified `Grid` resource *(SDK module in development)* | One job-based resource per grid, distinguished by data source |
| `Features`, `RoadFeature`, `WaterFeature` | unified `Feature` resource *(SDK module in development)* | One job-based resource for OSM road and water features |
| `Inventories`, `TreeInventory` | `Inventory` resource *(SDK module in development)* | Job-based; tree inventories are generated from PIM grids |

## Domains

Available now — see the [Domains guide](domains.md) and the
[Reference](../reference.md).

### What changed from v1

- **Resolution moved to grids.** Domains no longer take
  `horizontal_resolution`/`vertical_resolution`. Use the optional
  `pad_to_resolution` argument to pad the domain bounding box outward so
  grids of that resolution align with it.
- **Responses are richer.** A v2 domain carries two named GeoJSON
  features: `"domain"` (the projected working extent) and `"input"`
  (your original geometry).
- **GeoDataFrame CRS is honored.** `from_geodataframe` forwards the
  GeoDataFrame's CRS to the API, so projected inputs (e.g. EPSG:5070)
  are interpreted correctly. The v1 SDK assumed EPSG:4326.
- **No `Domain.export()`.** The v2 API has no domain export endpoint;
  domain data is exported through grid exports instead (coming with the
  v2 grids module).
- **New endpoints.** `Domain.preview` validates and projects a domain
  without creating it, `Domain.get_lattice` returns the pixel lattice
  for grid alignment, and `reproject_geojson` is a stateless
  reprojection utility.
- **Typed exceptions.** Errors raise `fastfuels_sdk.v2.exceptions`
  classes (`NotFoundException`, `UnprocessableEntityException`, ...)
  carrying the HTTP status code and API error detail.

### Before and after

v1:

```python
from fastfuels_sdk import Domain

domain = Domain.from_geojson(
    geojson,
    name="My Domain",
    horizontal_resolution=2.0,
    vertical_resolution=1.0,
)
```

v2:

```python
from fastfuels_sdk.v2 import Domain

domain = Domain.from_geojson(
    geojson,
    name="My Domain",
    pad_to_resolution=2.0,
)
```

## Grids

!!! note "In development"
    The v2 grids module is under development and will be documented here
    when it ships.

What to expect from the v2 API: the per-type grid resources
(surface/tree/topography/feature) collapse into a single job-based `Grid`
resource distinguished by its data source — LANDFIRE FBFM40 fuel models,
TreeMap (PIM), 3DEP topography, or custom GeoTIFF uploads. Every grid
shares the same `status`/`progress` lifecycle.

## Features

!!! note "In development"
    The v2 features module is under development and will be documented
    here when it ships.

What to expect from the v2 API: road and water features unify into a
single job-based `Feature` resource sourced from OSM, with the same
`status`/`progress` lifecycle as grids.

## Inventories

!!! note "In development"
    The v2 inventories module is under development and will be documented
    here when it ships.

What to expect from the v2 API: tree inventories are generated from a
PIM (TreeMap) grid, so the workflow becomes: create a TreeMap grid, wait
for it to complete, then create an inventory from it.
