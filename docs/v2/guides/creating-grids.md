# How to Create Grids in FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

A grid is a raster data product within a domain — topography, surface fuel
models, canopy fuels, and more — generated from a data source. This guide
shows how to create grids and assemble them into an aligned dataset for fire
modeling. For waiting on, inspecting, exporting, and managing grids you
already hold, see [Working with grids](working-with-grids.md); for what grids
*are*, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com). Coming from
the v1 SDK? Start with the [migration guide](migration.md#grids).

Creation is functional: call a `create_<kind>_grid_from_<source>` function on
a domain. Each returns a [`Grid`](working-with-grids.md) whose generation runs
as a background job, so it starts `"pending"`.

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- An existing [domain](domains.md) — every creator's first argument is a
  `Domain` (or a bare domain id string)

## Build an aligned grid set

The typical goal is several grids covering one domain on the *same* lattice,
so they stack cell-for-cell. Because each creator can resample to the domain
lattice, giving them all the same `output_resolution_m` is enough — here, a
30 m terrain + surface fuel + canopy set:

```python
import fastfuels_sdk.v2 as ff

topography = ff.grids.create_topography_grid_from_3dep(
    domain, source_resolution_m=10, output_resolution_m=30,
    bands=["elevation", "slope", "aspect"],
)
surface_fuel = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    domain, output_resolution_m=30,
)
canopy_fuel = ff.grids.create_canopy_fuel_grid_from_landfire(
    domain, output_resolution_m=30,
)

# Jobs run server-side in parallel — create first, then join.
ff.wait_all([topography, surface_fuel, canopy_fuel])
```

Each grid reports the bands it carries and, once complete, its
georeference:

```python
>>> [b.key for b in topography.bands]
['elevation', 'slope', 'aspect']
>>> topography.georeference.crs
'EPSG:32611'
>>> topography.georeference.shape   # [rows, cols] on the domain lattice
[47, 58]
```

Because all three share `output_resolution_m=30` on the same domain, they
share a CRS, transform, and shape — they overlay exactly. The sections below
cover each source in detail; [Working with grids](working-with-grids.md)
covers inspecting, resampling, exporting, and managing the results.

## Topography grids

From the USGS 3D Elevation Program (3DEP), which carries `elevation` (m),
`slope` (deg), and `aspect` (deg):

```python
grid = ff.grids.create_topography_grid_from_3dep(
    domain,
    source_resolution_m=10,   # 3DEP native resolution: 1, 10, or 30
    output_resolution_m=30,
    bands=["elevation", "slope", "aspect"],
)
```

3DEP is the higher-resolution source where it has coverage. To check before
creating the grid:

```python
>>> coverage = ff.grids.check_3dep_coverage(domain, resolution_m=10)
>>> coverage.available
True
>>> coverage.tile_count
1
```

Where 3DEP lacks coverage, source topography from LANDFIRE (30 m, CONUS)
instead:

```python
grid = ff.grids.create_topography_grid_from_landfire(domain, output_resolution_m=30)
```

## Surface fuel model grids

LANDFIRE's 40 Scott & Burgan fire behavior fuel models (FBFM40) is the
standard surface fuels source. The grid carries a single categorical `fbfm`
band of fuel model *codes* (e.g. `GR1`, `TL3`, `SH5`):

```python
grid = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    domain, output_resolution_m=30
)
```

To replace non-burnable codes (urban, water, agriculture, …) with no-data,
pass them to `remove_non_burnable`:

```python
grid = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    domain, output_resolution_m=30, remove_non_burnable=["NB1", "NB2"]
)
```

To pin an annual LANDFIRE vintage, pass `version` (e.g. `"2024"`); it defaults
to the API's current version. The grid reports the calendar year its fuels
represent on `grid.represented_year`:

```python
grid = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    domain, version="2024", output_resolution_m=30
)
```

```python
>>> grid.represented_year
2024
```

### Seasonal fuels

LANDFIRE Seasonal Fuels adjusts FBFM40 for a time of year — early spring
(`"ES"`), spring (`"SP"`), summer (`"SU"`), or fall (`"FA"`). Pass `season`
together with a seasonal `version` (`"2025"`) to fetch it on demand from the
LANDFIRE Product Service instead of the staged annual release:

```python
grid = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    domain, version="2025", season="SP", output_resolution_m=30
)
```

`grid.represented_year` is the projected season year — version `"2025"` plus
`"SP"` is spring 2026:

```python
>>> grid.represented_year
2026
```

!!! warning "Seasonal coverage is limited"

    Seasonal Fuels covers a changing region rather than all of CONUS. A
    request for a domain outside the current coverage raises
    `UnprocessableEntityException`. See
    [LANDFIRE Seasonal Fuels](https://landfire.gov/fuel/seasonal_fuels) for
    current availability.

### Look up fuel parameters from FBFM40 codes

The `fbfm` band holds codes, not the quantities a fire model consumes. To
turn the codes into fuel parameters — loadings by size class, fuel-bed depth,
surface-area-to-volume ratios — pass the completed grid to
`ff.grids.create_fuel_grid_from_fbfm40_lookup`. It returns a new grid whose
bands are the requested parameters:

```python
grid.wait()

fuels = ff.grids.create_fuel_grid_from_fbfm40_lookup(
    grid, bands=["fuel_load.1hr", "fuel_load.10hr", "fuel_depth"]
)
fuels.wait()
```

```python
>>> [(b.key, b.unit) for b in fuels.bands]
[('fuel_load.1hr', 'kg/m**2'), ('fuel_load.10hr', 'kg/m**2'), ('fuel_depth', 'm')]
```

### Use Anderson 13 fuel models

To create the Anderson 13 model set instead, select a LANDFIRE version and
use the FBFM13 creator:

```python
grid = ff.grids.create_fuel_model_grid_from_landfire_fbfm13(
    domain,
    version="2024",
    remove_non_burnable=["NB1", "NB2"],
    output_resolution_m=30,
)
grid.wait()
```

Its categorical source band is `fbfm13`. Convert it to any of the nine
FBFM13 parameter bands with the matching lookup:

```python
fuels = ff.grids.create_fuel_grid_from_fbfm13_lookup(
    grid,
    bands=["fuel_load.1hr", "fuel_load.live_foliage", "fuel_depth"],
)
fuels.wait()
```

### From FCCS instead

To use Fuel Characteristic Classification System (FCCS) fuelbeds, create the
categorical source grid and wait for it to complete:

```python
fccs = ff.grids.create_fuel_model_grid_from_landfire_fccs(
    domain, remove_bare_ground=True, output_resolution_m=30
)
fccs.wait()
```

Then look up any of the 12 available FCCS fuel-parameter bands, including
duff and live components:

```python
fuels = ff.grids.create_fuel_grid_from_fccs_lookup(
    fccs,
    bands=[
        "fuel_load.litter",
        "fuel_load.duff",
        "duff_depth",
        "fuel_load.live_shrub",
    ],
)
fuels.wait()
```

FCCS takes the same alignment arguments as the other source grids
(`output_resolution_m`, `align_to`, `align`, `resampling`) — see
[Align grids to each other](#align-grids-to-each-other).

To select and calculate bands across one or more completed grids, see
[Compose grids](composing-grids.md).

## Canopy grids

For crown-fire inputs, `create_canopy_fuel_grid_from_landfire` produces the
full LANDFIRE canopy set (30 m, CONUS) — canopy height, bulk density, base
height, and cover:

```python
grid = ff.grids.create_canopy_fuel_grid_from_landfire(domain, output_resolution_m=30)
```

```python
>>> [(b.key, b.unit) for b in grid.bands]
[('chm', 'm'), ('cbd', 'kg/m**3'), ('cbh', 'm'), ('cc', '%')]
```

When you only need canopy *height* at higher resolution, use a dedicated
canopy height model — the Meta model (≈1 m, global) or NAIP-CHM (0.6 m,
CONUS) — each producing a single `chm` band:

```python
meta = ff.grids.create_canopy_height_grid_from_meta(domain, output_resolution_m=1)
naip = ff.grids.create_canopy_height_grid_from_naip_chm(domain, output_resolution_m=1)
```

To rasterize a completed airborne point cloud into the same `chm` band, pass
the point cloud directly. The output defaults to 1 m cells:

```python
chm = ff.grids.create_canopy_height_grid_from_point_cloud(point_cloud)
chm.wait()
```

Use `output_resolution_m` or `align_to` to choose a different lattice. See the
[Point clouds guide](point-clouds.md#create-a-point-cloud-from-usgs-3dep) to
create an airborne point cloud from USGS 3DEP.

To control how each cell reduces its above-ground returns to a height, set
`aggregation` to `"max"` (the default), `"mean"`, `"median"`, or
`"percentile"`; `"percentile"` requires a `percentile` (0-100). The
`spike_filter` argument removes lone spurious returns: leave it unset for the
API's default filter, pass `False` to keep every return, or pass a mapping of
thresholds to tune it:

```python
chm = ff.grids.create_canopy_height_grid_from_point_cloud(
    point_cloud,
    output_resolution_m=2,
    aggregation="percentile",
    percentile=95,
    spike_filter={"min_canopy_footprint_m": 5, "min_prominence_m": 30},
)
chm.wait()
```

!!! tip "NAIP-CHM is a surface model"
    NAIP-CHM is a digital surface model and retains buildings and other
    infrastructure. To keep only vegetation, mask out built-up areas — see
    [Mask out features](#mask-out-features).

### Derive canopy fuels from a tree inventory

To compute the crown-fire bands directly from a completed
[tree inventory](inventories.md) rather than from LANDFIRE, pass the inventory
to `create_canopy_fuel_grid_from_inventory`. It derives canopy bulk density
(`cbd`), canopy base height (`cbh`), canopy height (`chm`), canopy cover
(`cc`), and canopy fuel load (`cfl`) from the inventory's trees; only live
trees contribute. The bands share keys and units with the LANDFIRE canopy
source, and the output defaults to 30 m cells:

```python
canopy = ff.grids.create_canopy_fuel_grid_from_inventory(
    inventory,
    bands=["cbd", "cbh", "chm", "cc", "cfl"],
    output_resolution_m=30,
)
canopy.wait()
```

```python
>>> {band.key for band in canopy.bands}
{'cbd', 'cbh', 'chm', 'cc', 'cfl'}
```

The default four bands (`cbd`, `cbh`, `chm`, `cc`) drop `cfl`; pass `bands`
to choose. Method keyword arguments tune how each band is derived — the
biomass source (`biomass_equations` or `biomass_column`), and per-band
reduction methods (`cbd`, `cbh`, `chm`, `cc`), among others. See
`create_canopy_fuel_grid_from_inventory` in the [Reference](../reference.md)
for the full surface. Pass `align_to` to match another grid's lattice exactly.

## 3D tree fuel grids (voxelization)

The 3D canopy fuel grid — per-voxel bulk density, the input 3D fire models
consume — is built in three steps:

**1. Create a Plot Imputation Map (PIM) grid** that maps each cell to a
TreeMap forest inventory plot:

```python
pim = ff.grids.create_pim_grid_from_treemap(
    domain, output_resolution_m=30, resampling="nearest"
)
pim.wait()
```

By default the grid carries the TreeMap id band (`tm_id`); request the plot
control number as well with `bands=["tm_id", "plt_cn"]`.

**2. Generate a tree inventory** from the PIM grid — a table of individual
trees imputed from the matched plots (see the
[Inventories guide](inventories.md)):

```python
inventory = ff.inventories.create_tree_inventory_from_pim_grid(
    domain, pim, seed=42
)
inventory.wait()
```

**3. Voxelize the inventory**, discretizing each tree's crown onto a 3D
lattice and computing per-voxel fuel properties:

```python
voxels = inventory.voxelize(
    horizontal_resolution_m=2.0, vertical_resolution_m=1.0
)
voxels.wait()
```

```python
>>> voxels.georeference.shape   # [layers, rows, cols]
[37, 703, 863]
```

Because it is a 3D product, a voxel grid supports neither resampling nor
post-hoc modifications — apply any tree modifications on the inventory
before voxelizing (see
[Modify and treat tree inventories](modify-treat-inventories.md)).

For the concepts behind plot imputation and voxelization, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com).

### Derive surface fuels with DUET

To create a two-dimensional DUET surface-fuel grid, include the three DUET
input bands when voxelizing the inventory:

```python
voxels = inventory.voxelize(
    horizontal_resolution_m=2,
    vertical_resolution_m=1,
    bands=[
        "bulk_density.foliage.live",
        "spcd",
        "fuel_moisture.live",
    ],
)
voxels.wait()
```

Build calibration targets from ordinary mappings, then pass them with the
output bands and time since fire:

```python
calibration = ff.duet_calibration(
    fuel_load={
        "grass": {"mean": 0.5, "sd": 0.25},
        "litter": {"max": 5, "min": 0},
    },
    fuel_depth={
        "grass": {"value": 0.3},
        "litter": {"value": 0.06},
    },
)

surface = ff.grids.create_surface_fuel_grid_from_duet(
    voxels,
    years_since_burn=25,
    bands=[
        "fuel_load.grass",
        "fuel_load.litter",
        "fuel_depth.grass",
        "fuel_depth.litter",
    ],
    calibration=calibration,
)
surface.wait()
```

Use a `value` target to set every occupied cell to a constant, `max` with an
optional `min` to scale by extrema, or `mean` and `sd` to scale by moments.
Omit `calibration` only when you want the raw DUET values.

## Solar irradiance grids

!!! warning "Beta"
    LeafLux irradiance grids are a new v2 grid family and still stabilizing.

To compute solar irradiance through the canopy at a single instant, pass a
completed 3D grid carrying a `leaf_area_density` band — a voxel grid from
[voxelization](#3d-tree-fuel-grids-voxelization) — to
`create_irradiance_grid_from_leaflux` with a UTC `date_time`. Light is
attenuated through the leaf area density with a Beer-Lambert
`extinction_coefficient` (default 0.5). For what solar irradiance means, see
the [FastFuels documentation](https://docs.fastfuels.silvxlabs.com).

The `irradiance.canopy.relative` band needs no terrain:

```python
import datetime

irradiance = ff.grids.create_irradiance_grid_from_leaflux(
    voxels,
    date_time=datetime.datetime(2024, 7, 1, 18, 0, tzinfo=datetime.timezone.utc),
    bands=["irradiance.canopy.relative"],
)
irradiance.wait()
```

The `irradiance.surface.relative` band (the default) drapes light onto the
ground, so it needs a terrain grid sharing the source grid's **exact
horizontal lattice** and carrying an `elevation` band. Build that terrain grid
with `align_to=<source grid>` and pass it as `source_terrain_grid`; without a
lattice-matched terrain grid the API returns a 422:

```python
topo = ff.grids.create_topography_grid_from_3dep(
    domain, align_to=voxels, bands=["elevation"]
)
topo.wait()

irradiance = ff.grids.create_irradiance_grid_from_leaflux(
    voxels,
    date_time=datetime.datetime(2024, 7, 1, 18, 0, tzinfo=datetime.timezone.utc),
    source_terrain_grid=topo,
    bands=["irradiance.surface.relative"],
)
irradiance.wait()
```

See [Align grids to each other](#align-grids-to-each-other) for how `align_to`
matches a lattice exactly.

## Fuel moisture grids

!!! warning "Beta"
    Fosberg dead fuel moisture grids are a new v2 grid family and still
    stabilizing.

To estimate 1-hour dead fuel moisture with the Fosberg model, pass a
topography grid and a surface-irradiance grid to
`create_dead_fuel_moisture_grid_from_fosberg` along with the weather inputs.
The result carries a single `fuel_moisture.dead.1hr` band (percent). For the
Fosberg 1-hr dead fuel moisture model itself, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com).

The topography, leaf-area-density, and surface-irradiance grids all feed the
same Fosberg cells, so they must land on **one shared lattice** — build the
topography and irradiance grids against the voxel grid with `align_to=`. The
topography grid supplies `slope` and `aspect` to Fosberg and `elevation` to
the irradiance surface draping:

```python
import datetime
import fastfuels_sdk.v2 as ff

# A voxel grid carrying leaf area density (see 3D tree fuel grids, above).
voxels = inventory.voxelize(
    horizontal_resolution_m=2, vertical_resolution_m=1, bands=["leaf_area_density"]
)
voxels.wait()

topo = ff.grids.create_topography_grid_from_3dep(
    domain, align_to=voxels, bands=["elevation", "slope", "aspect"]
)
topo.wait()

irradiance = ff.grids.create_irradiance_grid_from_leaflux(
    voxels,
    date_time=datetime.datetime(2020, 7, 1, 18, 0, tzinfo=datetime.timezone.utc),
    source_terrain_grid=topo,
    bands=["irradiance.surface.relative"],
)
irradiance.wait()

moisture = ff.grids.create_dead_fuel_moisture_grid_from_fosberg(
    topo, irradiance,
    dry_bulb_temp=75.0,       # degrees Fahrenheit, >= 10
    relative_humidity=20.0,   # percent, 0-100
    time=1200,                # local HHMM, 0800-1959
    month="July",
    elevation="near",         # Fosberg correction category: below/near/above
)
moisture.wait()
```

```python
>>> [band.key for band in moisture.bands]
['fuel_moisture.dead.1hr']
```

!!! warning "Grids must share one lattice"
    Passing topography, leaf-area-density, and irradiance grids that sit on
    different lattices is the most common failure. Build the topography and
    irradiance grids against the voxel grid with `align_to=` — see
    [Align grids to each other](#align-grids-to-each-other).

## Uniform grids

To fill the whole domain with constant band values at a chosen resolution —
useful for testing or for holding a fuel parameter constant:

```python
grid = ff.grids.create_uniform_grid(
    domain,
    resolution_m=2.0,
    bands={"fuel_load": 0.5, "fuel_moisture": 15.0},
)
```

## Grids from your own raster files

To upload a local NetCDF whose CRS matches the domain CRS:

```python
grid = ff.grids.create_grid_from_netcdf(domain, "fuels.nc")
grid.wait()
```

GeoTIFF uploads work the same way but additionally take a `bands` list of
`UploadBandDefinition`s mapping 1:1 to the raster's bands in order:

```python
from fastfuels_sdk.v2.client_library.models import UploadBandDefinition

grid = ff.grids.create_grid_from_geotiff(
    domain,
    "elevation.tif",
    bands=[UploadBandDefinition(key="elevation", interpolation="bilinear")],
)
```

The SDK creates the grid, uploads the file to the returned signed URL, and
hands back a pending grid.

## Align grids to each other

The worked example above gave every grid the same `output_resolution_m` to
land them on the domain lattice. Most creators (everything except FCCS and
uploads) accept four arguments that control the output lattice; they are
mutually exclusive — passing more than one raises `ValueError`:

- **`output_resolution_m`** — resample to this cell size on the **domain**
  lattice. The common case, and what makes grids of equal resolution stack.
- **`align="native"`** — keep the source's native resolution and lattice.
- **`align_to=<grid>`** — match another grid's lattice exactly (pass a
  `Grid` or its id), so the two stack even at the source's native
  resolution.
- **`resampling`** — the method used when changing resolution: `nearest`,
  `bilinear`, `cubic`, `average`, `mode`, `min`, `max`, `median`, and more.
  An unrecognized value raises `ValueError`.

```python
# Stack a canopy grid onto an existing topography grid's lattice exactly
canopy = ff.grids.create_canopy_fuel_grid_from_landfire(
    domain, align_to=topography, resampling="nearest"
)
```

## Mask out features

To overwrite grid cells that fall within a feature — the v2 replacement for
v1's `feature_masks` — build a mask with `ff.mask` and pass it in a creator's
`modifications` list. For example, to set the cells under roads to a
non-burnable fuel model code (FBFM 91):

```python
roads = ff.features.create_road_feature_from_osm(domain)
roads.wait()

grid = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    domain,
    output_resolution_m=30,
    modifications=[ff.mask(roads, "fbfm", 91, buffer_m=5)],
)
```

The feature must be `completed` and in the same domain as the grid. Roads
and other linestrings usually need a `buffer_m` (or `target="cell"`) so the
thin geometry covers whole cells. See `ff.mask` in the
[Reference](../reference.md) for masking multiple bands and the `operator`
and `target` options.

The same masks apply to a grid you already hold via
[`grid.apply_modifications`](working-with-grids.md#apply-modifications-to-a-grid),
which re-derives the grid in place.

## Error handling

Creators raise typed exceptions from `fastfuels_sdk.v2.exceptions` on invalid
input:

```python
from fastfuels_sdk.v2.exceptions import UnprocessableEntityException

try:
    grid = ff.grids.create_uniform_grid(domain, resolution_m=2.0, bands={"bad": 1})
except UnprocessableEntityException as exc:
    print(exc.detail)
```

See [Working with grids](working-with-grids.md#error-handling) for the full
exception model.

## Next steps

A freshly created grid is still a running job. [Working with
grids](working-with-grids.md) covers waiting on it, inspecting its bands and
georeference, resampling, exporting, and managing it.
