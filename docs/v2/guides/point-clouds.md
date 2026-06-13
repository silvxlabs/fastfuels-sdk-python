# How to Work with Point Clouds in FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

A point cloud is a 3D LiDAR dataset within a domain, uploaded from your own
airborne (ALS) or terrestrial (TLS) scan. For what point clouds *are* and how
they fit the platform, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com); this guide
covers uploading and managing them from Python.

The v2 surface is functional: you **create** a point cloud by uploading a file
to a domain, and everything you do with one you already hold is a **method** on
it.

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
- A local LiDAR file (`.las`/`.laz`)

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

- Full signatures — see the [Reference](../reference.md)
