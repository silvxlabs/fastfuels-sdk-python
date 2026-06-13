# Tutorial: Export QUIC-Fire Inputs with the v2 SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

In this tutorial we'll build a complete set of QUIC-Fire fuel inputs for a
small region in the Blue Mountain Recreation Area and package them into a
QUIC-Fire-loadable archive. Along the way we'll touch
every kind of v2 resource — a domain, OpenStreetMap features, raster grids, a
tree inventory, and a 3D voxel grid — and assemble them with a single
QUIC-Fire export.

We'll follow the v2 SDK's functional style throughout: we **create** a
resource by calling a `create_…` function on a domain, and everything we do
with a resource we already hold (waiting, looking up values, voxelizing,
exporting) is a **method** on it. Because every creation runs as a background
job, we'll create work in batches and join each batch with `ff.wait_all`,
letting the server do the jobs in parallel.

## What we'll build

A QUIC-Fire export reads five required fuel fields — plus optional
topography, which we'll include. We'll build each from a real data source:

| Field | Source we'll use | v2 resource |
| --- | --- | --- |
| Canopy bulk density | TreeMap → tree inventory → voxels | 3D voxel grid |
| Canopy fuel moisture | voxelization moisture model | 3D voxel grid |
| Surface fuel load | LANDFIRE FBFM40 lookup | 2D grid |
| Surface fuel depth | LANDFIRE FBFM40 lookup | 2D grid |
| Surface fuel moisture | a uniform value | 2D grid |
| Topography (elevation) | USGS 3DEP | 2D grid |

The exporter slices these into the QUIC-Fire `.dat` arrays we'll inspect in
[Step 9](#step-9-inspect-the-export).

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- Basic familiarity with Python and GeoPandas

For background on what each of these resources *is*, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com). Coming from
the v1 SDK? The [migration guide](../guides/migration.md) maps the v1 builder
classes to the v2 functions used here.

## Step 1: Authenticate

The v2 SDK reads your API key from the `FASTFUELS_API_KEY` environment
variable:

```bash
export FASTFUELS_API_KEY="your-api-key"
```

Then import the package under the conventional `ff` alias — everything in this
tutorial hangs off it:

```python
import fastfuels_sdk.v2 as ff
```

If you'd rather set the key in code, call `ff.set_api_key("your-api-key")`
before anything else.

## Step 2: Define a region of interest

We'll describe our area as a GeoDataFrame holding a single polygon in WGS 84
(EPSG:4326):

```python
import geopandas as gpd
from shapely.geometry import Polygon

coordinates = [
    [-114.09957018646286, 46.82933208815811],
    [-114.10141707482919, 46.828370407248826],
    [-114.10010954324228, 46.82690548814563],
    [-114.09560673134018, 46.8271123684554],
    [-114.09592544216444, 46.829058122675065],
    [-114.09957018646286, 46.82933208815811],
]

roi = gpd.GeoDataFrame(geometry=[Polygon(coordinates)], crs="EPSG:4326")
```

## Step 3: Create a domain

A domain is the spatial container every other resource lives in. We'll create
one from the GeoDataFrame, padding its bounding box out to a whole number of
2 m cells so the grids we build later tile it exactly:

```python
domain = ff.Domain.from_geodataframe(
    geodataframe=roi,
    name="Blue Mountain QUIC-Fire",
    description="Tutorial region in the Blue Mountain Recreation Area",
    pad_to_resolution=2.0,
)
```

```python
>>> domain.id
'0d77a5b1525b497c829fceeadba5f958'
```

The domain reprojects our lat/lon polygon into a local metric CRS. We can see
the 2 m pixel lattice every grid will share:

```python
>>> lattice = domain.get_lattice(resolution=2.0)
>>> lattice.crs
'EPSG:32611'
>>> lattice.shape   # [rows, cols]
[136, 225]
```

## Step 4: Add roads and water from OpenStreetMap

Roads and open water aren't fuel — we'll pull them from OpenStreetMap now so
we can carve them out of the fuels later. Both extractions are background
jobs, so we create them together and join with `ff.wait_all`:

```python
roads = ff.features.create_road_feature_from_osm(domain, name="Roads")
water = ff.features.create_water_feature_from_osm(domain, name="Water")

ff.wait_all([roads, water], verbose=True)
```

```text
Feature 07e6407aedd44d7e8a09fbc5e48c3f3e: pending (5s)
Feature 07e6407aedd44d7e8a09fbc5e48c3f3e: pending (15s)
Feature 07e6407aedd44d7e8a09fbc5e48c3f3e: completed (20s)
```

(Only one feature prints here — the other finished before `wait_all`
reached it. Small regions extract fast.)

!!! note "No separate feature grid in v2"
    In the v1 SDK you created a standalone *feature grid* to mask trees and
    fuels. In v2 there's no such resource: you mask a feature directly into
    each grid by passing `ff.mask(feature, …)` in that creator's
    `modifications=` list, as we do for the surface fuels in
    [Step 6](#step-6-build-the-surface-fuel-grids). See
    [Mask out features](../guides/creating-grids.md#mask-out-features) for the
    full masking model.

## Step 5: Build the topography grid

Elevation comes from the USGS 3D Elevation Program (3DEP). We resample its
10 m source onto our 2 m domain lattice:

```python
topography = ff.grids.create_topography_grid_from_3dep(
    domain,
    source_resolution_m=10,
    output_resolution_m=2,
    bands=["elevation"],
)
```

We won't wait on it yet — it's a pending job we'll join with the other raster
grids in the next step.

## Step 6: Build the surface fuel grids

QUIC-Fire's surface needs fuel load, fuel depth, and fuel moisture. Load and
depth come from LANDFIRE's 40 Scott & Burgan fire behavior fuel models
(FBFM40). First we build the FBFM40 grid, masking the road network to a
non-burnable code (FBFM 91) as we go — this is the v2 replacement for v1's
`feature_masks`:

```python
fbfm = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    domain,
    output_resolution_m=2,
    modifications=[ff.mask(roads, "fbfm", 91, buffer_m=5)],
)
```

The FBFM40 grid holds categorical fuel-model *codes*. We also start the
PIM grid we'll need for trees in [Step 7](#step-7-build-the-canopy-fuel-grid),
then join all three pending raster jobs:

```python
pim = ff.grids.create_pim_grid_from_treemap(
    domain, output_resolution_m=2, resampling="nearest"
)

ff.wait_all([topography, fbfm, pim], verbose=True)
```

With the FBFM40 codes in hand, we look up the actual fuel quantities QUIC-Fire
consumes — 1-hour fuel load and fuel-bed depth — which produces a new grid:

```python
surface = ff.grids.create_fuel_grid_from_fbfm40_lookup(
    fbfm, bands=["fuel_load.1hr", "fuel_depth"]
)
```

```python
>>> [(b.key, b.unit) for b in surface.bands]
[('fuel_load.1hr', 'kg/m**2'), ('fuel_depth', 'm')]
```

LANDFIRE doesn't carry fuel moisture (it's a weather-driven scenario input),
so we set a uniform 15% surface moisture on a matching 2 m grid:

```python
moisture = ff.grids.create_uniform_grid(
    domain, resolution_m=2.0, bands={"fuel_moisture.1hr": 15.0}
)
```

## Step 7: Build the canopy fuel grid

Canopy fuel takes three moves: match each cell to a TreeMap forest plot (the
PIM grid we already started), expand those plots into individual trees, then
voxelize the trees into a 3D bulk-density grid. We expand the trees from the
completed PIM grid, using a fixed `seed` so the result is reproducible:

```python
inventory = ff.inventories.create_tree_inventory_from_pim_grid(
    domain, pim, seed=42
)

ff.wait_all([surface, moisture, inventory], verbose=True)
```

```python
>>> len(inventory.to_dataframe())
2068
```

Now we voxelize the inventory onto the same 2 m horizontal lattice, with 1 m
vertical layers, asking for both the live foliage bulk density and the live
fuel moisture QUIC-Fire needs:

```python
voxels = inventory.voxelize(
    horizontal_resolution_m=2.0,
    vertical_resolution_m=1.0,
    bands=["bulk_density.foliage.live", "fuel_moisture.live"],
)
voxels.wait(verbose=True)
```

```python
>>> [b.key for b in voxels.bands]
['bulk_density.foliage.live', 'fuel_moisture.live']
>>> voxels.georeference.shape   # [layers, rows, cols]
[27, 136, 225]
```

## Step 8: Export to QUIC-Fire

Everything is now on the same 2 m lattice. `create_quicfire_export` bundles
the fields into a QUIC-Fire archive — each role is a `(grid, band)` pair
naming the grid and the band to read from it:

```python
export = ff.exports.create_quicfire_export(
    domain,
    canopy_bulk_density=(voxels, "bulk_density.foliage.live"),
    canopy_moisture=(voxels, "fuel_moisture.live"),
    surface_fuel_load=(surface, "fuel_load.1hr"),
    surface_fuel_depth=(surface, "fuel_depth"),
    surface_moisture=(moisture, "fuel_moisture.1hr"),
    topography=(topography, "elevation"),
    name="Blue Mountain QUIC-Fire",
)

export.wait(verbose=True)
```

```text
Export 67af943ef13e49a1b71c97c90c3fa4d9: pending (5s)
Export 67af943ef13e49a1b71c97c90c3fa4d9: running (20s)
Export 67af943ef13e49a1b71c97c90c3fa4d9: completed (25s)
```

The export is its own background job; once it completes, a signed download URL
is filled in. We stream the archive to a local directory:

```python
path = export.to_file("quicfire_export/")
```

```python
>>> path
PosixPath('quicfire_export/Blue_Mountain_QUIC-Fire.zip')
```

## Step 9: Inspect the export

The archive is a zip that QUIC-Fire loads directly. Let's confirm the inputs
are all there:

```python
>>> import zipfile
>>> sorted(zipfile.ZipFile(path).namelist())
['domain.geojson', 'metadata.json', 'topo.dat', 'treesfueldepth.dat', 'treesmoist.dat', 'treesrhof.dat']
```

The `.dat` files are the QUIC-Fire fuel arrays:

- `treesrhof.dat` — canopy bulk density
- `treesmoist.dat` — canopy fuel moisture
- `treesfueldepth.dat` — surface fuel-bed depth
- `topo.dat` — elevation

alongside `metadata.json` (the grid geometry and band provenance) and
`domain.geojson` (the domain footprint).

## Recap

In one pass we created a domain, pulled road and water features, built
topography from 3DEP and surface fuels from LANDFIRE FBFM40, expanded a
TreeMap tree inventory into a 3D canopy fuel grid, and bundled it all into a
QUIC-Fire archive — masking roads out of the fuels along the way.

## Next steps

- Swap in your own region by changing the polygon in
  [Step 2](#step-2-define-a-region-of-interest).
- Mask water (and other features) into the fuels the same way we masked
  roads — see [Mask out features](../guides/creating-grids.md#mask-out-features).
- Tune the tree inventory before voxelizing — thinning, treatments, and
  modifications — see
  [Modify and treat tree inventories](../guides/modify-treat-inventories.md).
- Define the fire grid from an existing grid's lattice, or change its
  resolution, with the export's alignment options — see
  [Bundle grids for QUIC-Fire](../guides/exports.md#bundle-grids-for-quic-fire).
- Full signatures for every function used here are in the
  [Reference](../reference.md).
```
