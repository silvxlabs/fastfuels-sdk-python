# Migrating from v1 to v2

The FastFuels v1 and v2 APIs are separate live services. Resources created
in v1 are not visible to v2 (and vice versa) — migrating a workflow means
creating new resources through v2. The SDK ships both interfaces as
versioned subpackages, so you can keep v1 working while you migrate to v2
one workflow at a time:

```python
from fastfuels_sdk import Domain      # v1 (the default today)
from fastfuels_sdk.v1 import Domain   # v1, explicit
from fastfuels_sdk.v2 import Domain   # v2
```

Both subpackages read the same `FASTFUELS_API_KEY` environment variable.
v1 and v2 are separate deployments that issue **different keys**, though, so
a v1 key will not authenticate against v2 — set `FASTFUELS_API_KEY` to the
key for the version you are calling.

!!! warning "One key per process"
    Because both subpackages read the single `FASTFUELS_API_KEY` variable,
    using v1 and v2 at the same time *in one process* with different keys is
    not supported. Migrate one workflow at a time, pointing
    `FASTFUELS_API_KEY` at the appropriate key for each run.

## At a glance

| v1 | v2 | What changed |
|---|---|---|
| `Domain.from_geojson(..., horizontal_resolution=2.0, vertical_resolution=1.0)` | `Domain.from_geojson(..., pad_to_resolution=2.0)` | Resolution belongs to grids now; domains only pad their extent for grid alignment |
| `domain.export()` | grid exports | No domain-level export in v2; data exports hang off grids |
| — | `Domain.preview`, `Domain.get_lattice`, `reproject_geojson` | New domain capabilities |
| `Grids`, `SurfaceGrid`, `TreeGrid`, `TopographyGrid`, `FeatureGrid` + builders | unified `Grid` resource | One job-based resource per grid, distinguished by data source |
| `Features`, `RoadFeature`, `WaterFeature` | unified `Feature` resource | One job-based resource for OSM roads, OSM water, and custom layersets |
| `feature.get_data()`, `feature.get_all_data()` | `feature.get_data_metadata()`, `feature.get_data_partition()`, `feature.get_data()`, `feature.to_geodataframe()` | Page-based data retrieval becomes partition-based |
| `Inventories`, `TreeInventory` | unified `Inventory` resource | One job-based resource, created from a PIM grid, a canopy height model, or an upload |

## Domains

Available now — see the [Domains guide](domains.md) and the
[Reference](../reference.md).

### What changed from v1

- **Resolution moved to grids.** Domains no longer take
  `horizontal_resolution`/`vertical_resolution`. Use the optional
  `pad_to_resolution` argument to pad the domain bounding box outward so
  grids of that resolution align with it.
- **Responses carry the working extent.** A v2 domain contains one named
  GeoJSON feature, `"domain"`: the projected bounding box used by child
  resources. Keep the original input geometry separately if you need it.
- **GeoDataFrame CRS is honored.** `from_geodataframe` forwards the
  GeoDataFrame's CRS to the API, so projected inputs (e.g. EPSG:5070)
  are interpreted correctly. The v1 SDK assumed EPSG:4326.
- **No `Domain.export()`.** The v2 API has no domain export endpoint;
  data is exported through [grid and inventory exports](exports.md)
  instead.
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
- **Universal transforms are methods; type-specific ones are functions.**
  Transforms that apply to any grid you hold are methods —
  `grid.resample(...)`, `grid.export(...)`. Deriving a fuel-parameter grid
  from FBFM40 codes only applies to FBFM40 grids, so it is a function:
  `ff.grids.create_fuel_grid_from_fbfm40_lookup(fbfm_grid, ...)`.

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

Available now — see the [Inventories guide](inventories.md) and the
[Reference](../reference.md).

### What changed from v1

- **TreeMap generation is a two-resource workflow.** v1's
  `create_tree_inventory_from_treemap()` did the plot matching and the
  tree expansion in one call. v2 splits them: create a PIM grid
  (`ff.grids.create_pim_grid_from_treemap`), wait for it, then expand it
  with `ff.inventories.create_tree_inventory_from_pim_grid(domain, pim)`.
  The intermediate PIM grid is reusable — expand it several times with
  different seeds or modifications without re-matching plots.
- **Creation is a function per source.** The `Inventories.from_domain_id`
  container is gone; call `create_tree_inventory_from_pim_grid`,
  `create_tree_inventory_from_chm_grid` (new — stem isolation on a canopy
  height model), or `create_tree_inventory_from_file` on the domain.
- **Upload columns changed.** v1 uploads required `TREE_ID`, `SPCD`,
  `STATUSCD`, `DIA`, `HT` columns. v2 uses the roles `x`, `y`, `height`,
  `dbh`, `crown_ratio`, `fia_species_code`, `fia_status_code`, and a
  `columns={role: your_name}` mapping replaces renaming your file.
- **Modifications and treatments are typed models.** v1's dict syntax
  (`{"attribute": "HT", ...}`) becomes the generated
  `InventoryModification` / treatment models, passed to `modifications=` /
  `treatments=` at creation or to `inventory.apply_modifications(...)`
  in place. v1's `feature_masks=["road", "water"]` becomes a modification
  whose condition is a feature spatial condition
  (`InventoryFeatureSpatialCondition`) and whose action is `RemoveAction`.
- **Data access is direct.** v1 exposed tree records only through file
  exports (`create_export` → `to_file`). v2 streams them from the API:
  `get_data_metadata()` / `get_data_partition(index)` — plus
  `to_dataframe()` for the common case of loading every tree into pandas.
  File exports remain available via `inventory.export(...)`.
- **Scenario branching is first-class.** `inventory.duplicate()` clones a
  completed inventory, and `checksum` marks the data version, so derived
  resources can detect a stale source.
- **Voxelization is a method.** The v1 tree grid built from an inventory
  becomes `inventory.voxelize(horizontal_resolution_m=...,
  vertical_resolution_m=...)`, returning a 3D `Grid`.

## Exports

Available now — see the [Exports guide](exports.md) and the
[Reference](../reference.md).

### What changed from v1

- **Exports hang off grids and inventories.** v1's `domain.export()` and
  per-resource `create_export`/`get_export` pairs become
  `grid.export(format=...)` and `inventory.export(format=...)`, each
  returning a job-based `Export`; chain `export.wait().to_file(path)` to
  download. The lifecycle renames match the other resources
  (`wait_until_completed` → `wait`).
- **`export_roi` becomes explicit creation + the QUIC-Fire bundle.** The
  v1 convenience built every resource from an ROI and exported in one
  call. In v2 you create the domain, grids, and inventory explicitly
  (see the other guides), then bundle them with
  `ff.exports.create_quicfire_export(domain, ...)` — naming the exact
  grid and band filling each QUIC-Fire role (`canopy_bulk_density`,
  `surface_fuel_load`, ...). The API packages the `.dat` archive
  server-side, replacing v1's client-side zarr-to-QUIC-Fire conversion.
- **Exports are cross-domain resources.** `ff.get_export(export_id)` and
  `ff.list_exports(...)` address exports by ID alone, with domain,
  source, and tag filters.

### Before and after

=== "v1"

    ```python
    export = tree_inventory.create_export("csv")
    export = export.wait_until_completed()
    export.to_file("trees.csv")
    ```

=== "v2"

    ```python
    inventory.export(format="csv").wait().to_file("trees.csv")
    ```

### Before and after

=== "v1"

    ```python
    from fastfuels_sdk import Inventories

    inventories = Inventories.from_domain_id(domain.id)
    trees = inventories.create_tree_inventory_from_treemap(seed=42)
    trees.wait_until_completed()

    export = trees.create_export("csv")
    export.wait_until_completed().to_file("trees.csv")  # read the file back
    ```

=== "v2"

    ```python
    import fastfuels_sdk.v2 as ff

    pim = ff.grids.create_pim_grid_from_treemap(domain, output_resolution_m=30)
    pim.wait()

    trees = ff.inventories.create_tree_inventory_from_pim_grid(domain, pim, seed=42)
    trees.wait()

    data = trees.to_dataframe()
    ```
