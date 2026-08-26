# How to Work with Point Clouds in FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

A point cloud is a 3D LiDAR dataset within a domain, fetched from USGS 3DEP or
uploaded from your own airborne (ALS) or terrestrial (TLS) scan. For what
point clouds *are* and how they fit the platform, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com); this guide
covers creating and managing them from Python.

The v2 surface is functional: you **create** a point cloud from a domain and
data source, and everything you do with one you already hold is a **method**
on it.

```python
import fastfuels_sdk.v2 as ff

pc = ff.point_clouds.create_point_cloud_from_file(
    domain, "scan.laz", point_cloud_type="als"
)
pc.wait()
```

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- An existing [domain](domains.md) — the first argument is a `Domain` (or a
  bare domain id string)
- A local LiDAR file (`.las`/`.laz`) when uploading your own scan

## Create a point cloud from USGS 3DEP

Check coverage and the per-fetch point budget before starting the background
job:

```python
coverage = ff.point_clouds.check_3dep_coverage(domain)

if not coverage.available:
    raise RuntimeError("No 3DEP LiDAR covers this domain")
if coverage.exceeds_point_budget:
    raise RuntimeError("Shrink the domain before fetching 3DEP LiDAR")
```

Create the point cloud with automatic acquisition selection:

```python
pc = ff.point_clouds.create_point_cloud_from_3dep(
    domain,
    name="USGS 3DEP",
)
pc.wait()
```

To pin specific acquisitions, pass names returned by the coverage check in
priority order:

```python
pc = ff.point_clouds.create_point_cloud_from_3dep(
    domain,
    datasets=[coverage.datasets[0].name],
)
```

The returned point cloud is always airborne (`type_ == "als"`).

## Upload a point cloud

`create_point_cloud_from_file` creates the resource, uploads the file to a
signed URL, and returns the (pending) point cloud. Set `point_cloud_type` to
`"als"` for an airborne scan or `"tls"` for a terrestrial one:

```python
pc = ff.point_clouds.create_point_cloud_from_file(
    domain,
    "scan.laz",
    point_cloud_type="als",
    name="North stand ALS",
)
```

Processing runs as a background job — the returned point cloud starts in
`"pending"` status and `wait()` blocks until it is ready:

```python
pc.wait(verbose=True)
```

Once completed, the point cloud's `georeference` (CRS and bounds) and
`summary` (point statistics) are populated.

## Work with a point cloud you hold

A point cloud is a job resource like any other: `wait(timeout=, verbose=)`
polls it to a terminal status (raising `JobFailedError` on failure),
`refresh()` reloads it in place, `update(name=, description=, tags=)` edits its
metadata, and `delete()` removes it along with its data.

```python
pc.update(name="North stand (2024)", tags=["als", "2024"])
pc.delete()
```

Point clouds are addressed by their domain and id:

```python
pc = ff.get_point_cloud(domain, "4a56bae0cd5e481aa1617cb894a9a7f3")
```

## Read point cloud data

To read a completed point cloud's points into memory, call `to_numpy()` or
`to_dataframe()`; both page over every occupied tile and stack them into one
array or frame. `to_numpy()` returns an `(N, k)` `float64` array of the
requested `columns`, defaulting to the `X`/`Y`/`Z` coordinates:

```python
pc = ff.get_point_cloud(domain, "4a56bae0cd5e481aa1617cb894a9a7f3").wait()

points = pc.to_numpy()
```

```python
>>> points.shape
(48213, 3)
```

`to_dataframe()` returns one row per point and one column per stored attribute
(`X`, `Y`, `Z`, `classification`, and any source columns such as `intensity`):

```python
df = pc.to_dataframe()
```

```python
>>> df.columns.tolist()
['X', 'Y', 'Z', 'classification']
```

To read fewer points, narrow the output with these arguments (shared by both
methods):

- **`lod`** — an inclusive level-of-detail ceiling. `0` is the coarsest sample
  and each higher value adds finer points; omit it to read every point. Valid
  values are `0` through `lod_levels - 1` (see `metadata()` below).
- **`classes`** — ASPRS classification codes to keep, e.g. `[2, 5]` for ground
  and high vegetation.
- **`columns`** — the stored columns to read, in the returned order.
- **`decode_coordinates`** — `True` (default) decodes `X`/`Y`/`Z` to CRS
  coordinates; `False` keeps them as the stored scaled integers.

```python
# Ground returns only, as CRS coordinates.
ground = pc.to_dataframe(classes=[2], columns=["X", "Y", "Z", "classification"])
```

To inspect the tile index — occupied tiles, stored columns and dtypes, the
coordinate encoding, and the point count at each level of detail — without
downloading any points, call `metadata()`:

```python
meta = pc.metadata()
```

```python
>>> meta.lod_levels
5
>>> len(meta.tiles)
4
```

!!! tip "Wait before reading"
    `metadata()`, `to_numpy()`, and `to_dataframe()` require a completed point
    cloud; call `wait()` first or they raise `ValueError`.

## List point clouds

To list your point clouds, optionally narrowed to a domain, a scan type, a
source, or a tag:

```python
clouds = ff.list_point_clouds(domain)
als_only = ff.list_point_clouds(domain, point_cloud_type="als")
tagged = ff.list_point_clouds(tag="2024")
```

Omit `domain` to list point clouds across all of your domains.

## Error handling

Wrapper functions and methods raise typed exceptions from
`fastfuels_sdk.v2.exceptions`:

```python
import fastfuels_sdk.v2 as ff
from fastfuels_sdk.v2.exceptions import NotFoundException

try:
    pc = ff.get_point_cloud(domain, "does-not-exist")
except NotFoundException:
    print("No such point cloud (or you don't have access to it)")
```

## Next steps

- Turn a completed airborne point cloud into a canopy-height grid with
  [`create_canopy_height_grid_from_point_cloud`](creating-grids.md#canopy-grids)
- Full signatures — see the [Reference](../reference.md)
