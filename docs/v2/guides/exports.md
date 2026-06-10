# How to Export Data from FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

An export packages a resource's data into a downloadable file: a
[grid](working-with-grids.md) as GeoTIFF/NetCDF/zarr, an
[inventory](inventories.md) as Parquet/CSV/GeoJSON/GeoPackage, or several
grids bundled into a QUIC-Fire-loadable archive. Exports run as background
jobs and expose a signed download URL on completion.

The pattern is the same everywhere: exporting a resource you **hold** is a
method on it (`grid.export(...)`, `inventory.export(...)`); the QUIC-Fire
bundle is **assembled from many** grids, so it is a module-level function
(`ff.exports.create_quicfire_export(...)`).

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- A completed resource to export — a [grid](creating-grids.md) or an
  [inventory](inventories.md)

## Export and download a grid

To export a completed grid and save the file, chain create → `wait` →
`to_file`:

```python
import fastfuels_sdk.v2 as ff

export = grid.export(format="geotiff")  # or "netcdf", "zarr"
export.wait().to_file("elevation.tif")
```

`grid.export` returns a pending [`Export`](#work-with-an-export-you-hold);
`wait()` blocks until the file is packaged, and `to_file` streams it to
disk. GeoTIFF applies to 2D grids; export 3D voxel grids as `"netcdf"` or
`"zarr"`. Pass `bands=` to export a subset of the grid's bands.

If `to_file` is given an existing directory, the file lands inside it
under the export's default filename:

```python
>>> export.wait().to_file("outputs/")
PosixPath('outputs/export.tif')
```

## Export and download an inventory

The same flow exports an inventory's tree records — `"parquet"` (zipped,
default), `"csv"`, `"geojson"`, or `"geopackage"`, with `columns=` for a
column subset:

```python
export = inventory.export(format="csv")
path = export.wait().to_file("trees.csv")
```

```python
>>> path.read_text().splitlines()[0]
'x,y,fia_species_code,fia_status_code,dbh,height,crown_ratio'
```

## Bundle grids for QUIC-Fire

`create_quicfire_export` packages surface fuel, canopy fuel, and
(optionally) topography grids into a zip archive that QUIC-Fire loads
directly. Each role is a `(grid, band)` pair; the five required roles
produce `treesrhof.dat`, `treesmoist.dat`, and `treesfueldepth.dat`:

```python
export = ff.exports.create_quicfire_export(
    domain,
    canopy_bulk_density=(voxels, "bulk_density.foliage.live"),
    canopy_moisture=(voxels, "fuel_moisture.live"),
    surface_fuel_load=(surface, "fuel_load.1hr"),
    surface_fuel_depth=(surface, "fuel_depth"),
    surface_moisture=(surface, "fuel_moisture.1hr"),
    name="QUIC-Fire bundle",
)
export.wait().to_file("outputs/")
```

```python
>>> import zipfile
>>> sorted(zipfile.ZipFile("outputs/QUIC-Fire_bundle.zip").namelist())
['domain.geojson', 'metadata.json', 'treesfueldepth.dat', 'treesmoist.dat', 'treesrhof.dat']
```

Here `voxels` is a [3D tree fuel grid](inventories.md#voxelize-into-a-3d-fuel-grid)
carrying bulk density and moisture bands, and `surface` is any 2D grid
carrying the surface roles (the example above pairs naturally with a
[uniform grid](creating-grids.md#uniform-grids) or an
[FBFM40 lookup grid](creating-grids.md#surface-fuel-model-grids)).

Two optional roles extend the bundle: `topography=(grid, "elevation")`
adds `topo.dat`, and the SAVR pair (`canopy_savr=` + `surface_savr=`,
both or neither) adds `treesss.dat`.

The fire grid — the lattice everything is sliced onto — defaults to the
domain bounding box at 2 m horizontal / 1 m vertical. Change it with
`horizontal_resolution_m=` / `vertical_resolution_m=`, or define it from
an existing grid's lattice with `align_to=<grid>`. Every role grid must be
lattice-aligned with the fire grid and cover its full extent — the
exporter crops oversized grids by integer slicing but never resamples, so
build the roles on the fire grid's lattice (see
[Align grids to each other](creating-grids.md#align-grids-to-each-other)).

## Work with an export you hold

An `Export` is a job resource like any other: `wait(timeout=, verbose=)`
polls it to a terminal status (raising `JobFailedError` on failure),
`refresh()` reloads it in place, `update(name=, description=, tags=)`
edits its metadata, and `delete()` removes it along with the packaged
file.

The signed download URL fills in on completion and expires after
`expiration_days` (max 7, the default):

```python
>>> export.signed_url[:50]
'https://storage.googleapis.com/silvx-fastfuels-exp'
>>> export.expires_on
datetime.datetime(2026, 6, 17, 15, 5, 46, 885537, tzinfo=datetime.timezone.utc)
```

Downloading before the job completes raises a `ValueError`:

```python
>>> pending_export.to_file("outputs/")
ValueError: Cannot download an export with status 'pending'. Call .wait() until it completes first.
```

Exports are addressed by their ID alone — no domain in the path:

```python
export = ff.get_export("4a56bae0cd5e481aa1617cb894a9a7f3")
```

## List exports

To list your exports, optionally narrowed to a domain, a source name
(the format, or `"quicfire"` for bundles), or a tag:

```python
exports = ff.list_exports(domain)
bundles = ff.list_exports(source="quicfire")
tagged = ff.list_exports(tag="run-42")
```

## Error handling

Wrapper functions and methods raise typed exceptions from
`fastfuels_sdk.v2.exceptions`:

```python
import fastfuels_sdk.v2 as ff
from fastfuels_sdk.v2.exceptions import NotFoundException

try:
    export = ff.get_export("does-not-exist")
except NotFoundException:
    print("No such export (or you don't have access to it)")
```

## Next steps

- Build the grids that feed an export — see
  [Creating grids](creating-grids.md) and
  [Inventories](inventories.md)
- Full signatures — see the [Reference](../reference.md)
