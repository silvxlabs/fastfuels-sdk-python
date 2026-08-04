# How to Work with Grids in FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

This guide covers what you do with a grid you already hold: wait on its job,
inspect its bands and georeference, resample it, export it, and list or
delete grids. To create grids in the first place, see
[Creating grids](creating-grids.md). For what grids *are*, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com).

You get a grid handle either from a creator (see
[Creating grids](creating-grids.md)) or by fetching one by id:

```python
import fastfuels_sdk.v2 as ff

grid = ff.get_grid(domain, "0eeed67e33df450f943a528fb1447dab")
```

Operations on a grid you hold are **methods** on it (`grid.wait()`,
`grid.resample(...)`, `grid.delete()`); listing and fetching are top-level
functions (`ff.list_grids`, `ff.get_grid`).

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- A grid — created per [Creating grids](creating-grids.md), or fetched by id

## Wait for a grid to finish

Because creators return a pending grid, block on the job before using its
data:

```python
grid.wait()
```

```python
>>> grid.status
<JobStatus.COMPLETED: 'completed'>
```

`wait` polls until the job reaches a terminal status and returns the grid,
so calls chain. It waits indefinitely by default; pass `timeout` (seconds)
to bound it, which raises `TimeoutError`. A failed job raises
`JobFailedError`, carrying the API's `code`, `message`, and `suggestion`.

Jobs run server-side in parallel, so create everything first and join with
`ff.wait_all`. With `verbose=True` it prints a line per poll for each grid
still running when it is reached:

```python
ff.wait_all([topography, surface_fuel, canopy_fuel], verbose=True)
```

```text
Grid 0eeed67e33df450f943a528fb1447dab: running (5s)
Grid 0eeed67e33df450f943a528fb1447dab: completed (10s)
```

(Small domains finish fast — grids already complete when `wait_all` reaches
them print nothing.)

## Inspect a grid's bands and georeference

A grid reports its bands as soon as it is created — their keys, names, and
units — so you know what data it holds:

```python
>>> [b.key for b in topography.bands]
['elevation', 'slope', 'aspect']
>>> topography.bands[1].name, topography.bands[1].unit
('Slope', 'deg')
```

Its georeference is populated once the job completes (it is `None` while
pending), reporting the CRS, affine transform, and pixel shape of the
output:

```python
>>> topography.georeference.crs
'EPSG:32611'
>>> topography.georeference.transform   # affine [a, b, c, d, e, f]
[30.0, 0.0, 720192.0, 0.0, -30.0, 5190856.0]
>>> topography.georeference.shape       # [rows, cols]
[47, 58]
```

Two grids built on the same domain at the same resolution share this
georeference, which is what lets them overlay cell-for-cell.

## Summarize a band without downloading it

Once a grid completes, the server attaches summary statistics to each band, so
you can get a quick overview without fetching the cells (which is what
[`to_numpy`](#read-grid-data-into-python) does). Pass a band key to
`band_summary`:

```python
summary = topography.band_summary("elevation")
```

A continuous band reports `count`, `nodata_count`, `min_`, `max_`, `mean`, and
`std`; a categorical band reports `count`, `nodata_count`, and `unique_count`.
The `type_` field (`"continuous"` or `"categorical"`) tells you which.
`band_summary` returns `None` until the grid completes — call
[`wait`](#wait-for-a-grid-to-finish) first.

## Retrieve a grid by id

To fetch an existing grid using its domain and grid IDs:

```python
grid = ff.get_grid(domain, "0eeed67e33df450f943a528fb1447dab")
```

## Refresh and update

To reload a grid's latest state in place (for example, to check job progress
yourself):

```python
grid.refresh()
```

To change a grid's name, description, or tags:

```python
>>> grid.update(name="Topography (30 m)", tags=["terrain"])
>>> grid.name, grid.tags
('Topography (30 m)', ['terrain'])
```

`refresh` and `update` both change the grid in place and return it. `update`
sends only the fields you pass; passing none makes no API call.

## Resample a grid

To resample a completed grid onto a new lattice, producing a new grid:

```python
coarser = grid.resample(output_resolution_m=90, resampling="average")
```

`resample` takes the same alignment arguments as the creators (see
[Align grids to each other](creating-grids.md#align-grids-to-each-other)).
The source grid must be `completed`.

## Duplicate a grid

To branch from a completed grid, `duplicate` makes an independent copy under a
new ID. The finished data is byte-copied rather than re-derived, so the copy
carries the source's `checksum` verbatim — only its `id` and timestamps differ:

```python
copy = grid.duplicate(name="Scenario A")
copy.wait()
```

## Apply modifications to a grid

To modify a grid you already hold — rather than at creation — call
`apply_modifications` with the same `ff.mask(...)` rules a creator's
`modifications=` argument accepts. The rules are appended to the grid's
cumulative modifications and the data is re-derived **in place**: the grid
keeps its ID and returns to `"pending"` while it rebuilds.

```python
grid.apply_modifications([ff.mask(roads, "fbfm", 91, buffer_m=5)])
grid.wait()
```

The grid must be `completed` first. Re-deriving overwrites the grid's data, so
to keep the original, [`duplicate`](#duplicate-a-grid) it first and modify the
copy. See [Mask out features](creating-grids.md#mask-out-features) for the
masking model.

## Read grid data into Python

To pull a single band's values into a NumPy array, pass the band key to
`to_numpy`:

```python
elevation = topography.to_numpy("elevation")
```

```python
>>> elevation.shape       # matches grid.georeference.shape
(47, 58)
>>> elevation.dtype
dtype('float32')
```

The array is shaped like the grid — `(rows, cols)` for a 2D raster, or
`(z, rows, cols)` for a 3D voxel grid. Cells with no data hold the band's
`nodata` value, or `NaN` when the band defines none.

To read every band at once into an `xarray.Dataset` — one variable per band,
with `x`/`y` (and `z`) coordinates derived from the grid's affine transform
and the CRS on `.attrs` — call `to_xarray`:

```python
>>> topography.to_xarray()
<xarray.Dataset> Size: 34kB
Dimensions:    (y: 47, x: 58)
Coordinates:
  * y          (y) float64 376B 5.191e+06 5.191e+06 ... 5.189e+06 5.189e+06
  * x          (x) float64 464B 7.202e+05 7.202e+05 ... 7.219e+05 7.219e+05
Data variables:
    elevation  (y, x) float32 11kB 1.015e+03 1.013e+03 ... 1.02e+03 1.019e+03
    slope      (y, x) float32 11kB 7.587 8.345 8.092 7.41 ... 3.42 3.008 3.094
    aspect     (y, x) float32 11kB 25.29 28.79 40.35 51.47 ... 126.0 135.2 138.1
Attributes:
    crs:      EPSG:32611
```

Both methods download the grid's data and require a `completed` grid. To
write the data to a file on disk instead of loading it into memory, see
[Export a grid](#export-a-grid).

## Export a grid

To export a completed grid to a downloadable file and save it, chain the
export job's `wait` into `to_file`:

```python
export = grid.export(format="geotiff")  # or "netcdf", "zarr"
export.wait().to_file("elevation.tif")
```

The export runs as its own background job; the signed download URL fills
in once it completes and stays valid for seven days. To load a grid's
values into memory instead of a file, see
[Read grid data into Python](#read-grid-data-into-python). For exporting
band subsets, the multi-grid QUIC-Fire bundle, and managing exports, see the
[Exports guide](exports.md).

## List grids

To list grids in a domain, or across all your domains by omitting it:

```python
grids = ff.list_grids(domain)
all_grids = ff.list_grids()
```

Narrow the results by source, source product (requires `source`), or tag —
the source and product names are the ones a grid reports in `grid.source`:

```python
topo_grids = ff.list_grids(domain, source="3dep")
fbfm_grids = ff.list_grids(domain, source="landfire", product="fbfm40")
tagged = ff.list_grids(domain, tag="terrain")
```

## Delete a grid

To permanently delete a grid and its generated data:

```python
grid.delete()
```

Deleting a domain also deletes all of its grids.

## Error handling

Functions and methods raise typed exceptions from
`fastfuels_sdk.v2.exceptions`:

```python
import fastfuels_sdk.v2 as ff
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

try:
    grid = ff.get_grid(domain, "does-not-exist")
except NotFoundException:
    print("No such grid (or you don't have access to it)")

try:
    grid.resample(output_resolution_m=30)  # source not completed yet
except UnprocessableEntityException as exc:
    print(exc.detail)
```
