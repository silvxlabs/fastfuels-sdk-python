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
| `Grids`, `SurfaceGrid`, `TreeGrid`, `TopographyGrid`, `FeatureGrid` + builders | unified `Grid` resource | One job-based resource per grid, distinguished by data source |
| `Features`, `RoadFeature`, `WaterFeature` | unified `Feature` resource | One job-based resource for OSM roads, OSM water, and custom layersets |
| `feature.get_data()`, `feature.get_all_data()` | `feature.get_data_metadata()`, `feature.get_data_partition()`, `feature.get_data()`, `feature.to_geodataframe()` | Page-based data retrieval becomes partition-based |
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

=== "v1"

    ```python
    from fastfuels_sdk import Domain

    domain = Domain.from_geojson(
        geojson,
        name="My Domain",
        horizontal_resolution=2.0,
        vertical_resolution=1.0,
    )
    ```

=== "v2"

    ```python
    from fastfuels_sdk.v2 import Domain

    domain = Domain.from_geojson(
        geojson,
        name="My Domain",
        pad_to_resolution=2.0,
    )
    ```

## Grids

Available now — see [Creating grids](creating-grids.md),
[Working with grids](working-with-grids.md), and the
[Reference](../reference.md).

### What changed from v1

- **One unified `Grid` resource.** v1's per-type resources
  (`SurfaceGrid`, `TreeGrid`, `TopographyGrid`, `FeatureGrid`) and their
  builders collapse into a single job-based `Grid` distinguished by its
  data source. The `Grids.from_domain_id(...)` container is replaced by
  the module-level `list_grids(domain)`.
- **Creation is a function per source.** Instead of a builder, call a
  `create_<kind>_grid_from_<source>` function on the domain — e.g.
  `ff.grids.create_topography_grid_from_3dep(...)` or
  `ff.grids.create_fuel_model_grid_from_landfire_fbfm40(...)`.
- **Alignment is explicit.** Resolution and lattice are set per grid with
  `output_resolution_m`, `align="native"`, `align_to=<grid>`, and
  `resampling` (see
  [Align grids to each other](creating-grids.md#align-grids-to-each-other)).
- **`feature_masks` becomes `modifications`.** v1's
  `feature_masks=["road", "water"]` becomes
  `modifications=[ff.mask(feature, band, value)]`, which overwrites the
  cells a feature covers.
- **Transforms are methods.** `grid.resample(...)`,
  `grid.lookup_fuel_model_values(...)`, and `grid.export(...)` act on a
  grid you already hold.

### Before and after

=== "v1"

    ```python
    from fastfuels_sdk import Grids

    grids = Grids.from_domain_id(domain.id)
    topo = grids.create_topography_grid(
        attributes=["elevation", "slope", "aspect"]
    )
    topo.wait_until_completed()
    ```

=== "v2"

    ```python
    import fastfuels_sdk.v2 as ff

    topo = ff.grids.create_topography_grid_from_3dep(
        domain, output_resolution_m=10, bands=["elevation", "slope", "aspect"]
    )
    topo.wait()
    ```

## Features

Available now — see the [Features guide](features.md) and the
[Reference](../reference.md).

### What changed from v1

- **Road and water unify into one resource.** v1's `Features` container
  with `.road`/`.water` sub-resources becomes a single job-based
  `Feature` distinguished by its type ("road", "water", or "layerset").
  The `Features.from_domain_id(...)` container is replaced by the
  module-level `list_features(domain_id)`.
- **Creation is a function per source.** The v1
  `features.create_road_feature_from_osm()` becomes the module-level
  `ff.features.create_road_feature_from_osm(domain)`, and likewise
  `create_water_feature_from_osm` for water. The new `extent_buffer_m`
  argument buffers the OSM query extent by up to 100 meters.
- **User-supplied geometry becomes layersets.** v1's road-from-GeoJSON
  path is gone. Instead, v2 accepts custom *layersets* — fuelbed
  polygons carrying rasterizer properties — via
  `ff.features.create_layerset_feature_from_geojson` and
  `create_layerset_feature_from_geodataframe`. Layersets require a
  projected CRS and upload synchronously, and a completed layerset can be
  burned onto a grid with `feature.rasterize(...)`.
- **Data access is partitioned.** v1's `get_data(page, size)` /
  `get_all_data()` become `get_data_metadata()` (partition layout),
  `get_data_partition(index)` (one partition), and `get_data()` (all
  partitions assembled) — plus `to_geodataframe()` for the common case
  of loading everything into GeoPandas.
- **Cross-domain listing.** `list_features()` without a domain ID lists
  features across all your domains, with `feature_type`, `product`, and
  `tag` filters.
- **Typed exceptions.** Errors raise `fastfuels_sdk.v2.exceptions`
  classes, the same as domains.

### Before and after

=== "v1"

    ```python
    from fastfuels_sdk import Features

    features = Features.from_domain_id(domain.id)
    road = features.create_road_feature_from_osm()
    road.wait_until_completed(verbose=True)

    data = road.get_all_data()
    ```

=== "v2"

    ```python
    import fastfuels_sdk.v2 as ff

    road = ff.features.create_road_feature_from_osm(domain)
    road.wait(verbose=True)

    roads = road.to_geodataframe()
    ```

## Inventories

!!! note "In development"
    The v2 inventories module is under development and will be documented
    here when it ships.

What to expect from the v2 API: tree inventories are generated from a
PIM (TreeMap) grid, so the workflow becomes: create a TreeMap grid, wait
for it to complete, then create an inventory from it.
