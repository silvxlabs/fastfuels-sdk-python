# How to Work with Features in FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

Features are geographic data within a domain: roads and water bodies
extracted from OpenStreetMap, or custom layersets of fuelbed polygons you
upload yourself. This guide covers working with features from Python; for
what features *are* and how the platform treats them, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com). Coming
from the v1 SDK? Start with the [migration guide](migration.md#features).

The v2 surface is functional: you **create** a feature by calling a
`create_..._feature_from_...` function on a domain, and everything you do
with a feature you already hold is a **method** on it.

```python
import fastfuels_sdk.v2 as ff

feature = ff.features.create_road_feature_from_osm(domain)
feature.wait()
```

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- An existing [domain](domains.md) to create features in

## Create a Road Feature from OpenStreetMap

To extract the road network within a domain's extent:

```python
import fastfuels_sdk.v2 as ff

feature = ff.features.create_road_feature_from_osm(
    domain,
    name="My Roads",
    description="OSM road network",
)

print(feature.status)  # pending
```

Feature generation runs as a background job — the returned feature starts
in `"pending"` status. To include roads just outside the domain, buffer
the query extent by up to 100 meters with `extent_buffer_m`:

```python
feature = ff.features.create_road_feature_from_osm(domain, extent_buffer_m=50)
```

The first argument accepts either a `Domain` or a bare domain id string.

## Create a Water Feature from OpenStreetMap

To extract water bodies, use the same calling convention:

```python
feature = ff.features.create_water_feature_from_osm(domain, name="My Water")
```

## Wait for a Feature to Complete

To block until a feature job finishes:

```python
feature.wait(verbose=True)
```

```text
Feature 36573c0205d147a08011693b7894c0fb: pending (5s)
Feature 36573c0205d147a08011693b7894c0fb: running (15s)
Feature 36573c0205d147a08011693b7894c0fb: completed (20s)
```

`wait` polls until the job reaches a terminal status and returns the
feature (so calls chain). By default it waits indefinitely; pass `timeout`
(seconds) to bound the wait, which raises `TimeoutError` if exceeded. A
failed job raises `JobFailedError`, carrying the API's `code`, `message`,
and `suggestion`. To wait on several jobs at once, use `ff.wait_all`:

```python
roads = ff.features.create_road_feature_from_osm(domain)
water = ff.features.create_water_feature_from_osm(domain)

ff.wait_all([roads, water])  # jobs run server-side in parallel
```

Once completed, the feature's `georeference` reports the CRS and bounds of
the generated data:

```python
print(feature.georeference.crs)     # 'EPSG:32611'
print(feature.georeference.bounds)  # [720192.0, 5189446.0, 721918.0, 5190852.0]
```

## Upload a Custom Layerset

A layerset is a FeatureCollection of fuelbed polygons you supply
yourself. Unlike OSM features, the upload is synchronous — the returned
feature is already `"completed"`.

!!! warning "Projected CRS required"
    The FeatureCollection's `crs` member must declare a **projected** CRS
    (e.g. EPSG:5070 or a UTM zone). Geographic coordinates (EPSG:4326)
    are rejected, because rasterization requires cell sizes in meters.

Each polygon's `properties` must carry the fuelbed input columns
`fuel_type`, `fuel_loading`, `fuel_height`, `percent_cover`, and
`distribution` (`"homogeneous"`, `"random_clusters"`, or
`"uniform_random"`):

```python
import json
import fastfuels_sdk.v2 as ff

with open("fuelbeds.geojson") as f:  # projected CRS + fuelbed properties
    geojson = json.load(f)

feature = ff.features.create_layerset_feature_from_geojson(
    domain, geojson, name="My Fuelbeds"
)

print(feature.status)  # completed
```

To upload from a GeoPandas GeoDataFrame instead, reproject first if
needed — the GeoDataFrame's CRS is forwarded as-is:

```python
import geopandas as gpd

gdf = gpd.read_file("fuelbeds.shp").to_crs(epsg=5070)
feature = ff.features.create_layerset_feature_from_geodataframe(domain, gdf)
```

## Rasterize a Layerset into a Grid

A completed layerset feature carries vector fuelbed polygons; to burn them
onto a raster grid, call `rasterize`. It returns a pending
[`Grid`](working-with-grids.md):

```python
grid = feature.rasterize(output_resolution_m=2.0)
grid.wait()
```

`rasterize` takes the same alignment arguments as the grid creators
(`output_resolution_m`, `align_to`, `align`, `resampling`) plus an
`overlap_method` controlling how overlapping polygons resolve. See
[Align grids to each other](creating-grids.md#align-grids-to-each-other)
for the alignment model.

## Retrieve an Existing Feature

To fetch a feature using its domain and feature IDs:

```python
feature = ff.get_feature(domain, "36573c0205d147a08011693b7894c0fb")
```

## Refresh Feature Data

To reload a feature's latest state from the API (for example, to check job
progress yourself) in place:

```python
feature.refresh()
print(feature.status)
```

`refresh` updates the feature in place and returns it. To fetch a separate
copy by ID instead, use `ff.get_feature(domain, feature.id)`.

## Access Feature Data

The generated geodata is served in partitions. For most workflows,
retrieve everything at once as a GeoDataFrame:

```python
gdf = feature.to_geodataframe()

print(len(gdf))   # 43
print(gdf.crs)    # EPSG:32611
```

Or as a single GeoJSON FeatureCollection:

```python
data = feature.get_data()
print(len(data["features"]))  # 43
```

To control retrieval partition by partition (useful for large features),
read the partition layout first:

```python
metadata = feature.get_data_metadata()
print(metadata.total_features)   # 43
print(metadata.partition_count)  # 1

for index in range(metadata.partition_count):
    partition = feature.get_data_partition(index)  # GeoJSON FeatureCollection
```

Data is only available once the feature is `"completed"` — earlier calls
raise `UnprocessableEntityException`.

## Update Feature Properties

To modify a feature's name, description, or tags:

```python
feature.update(name="New Name", tags=["roads", "osm"])
```

`update` changes the feature in place and returns it. Only the fields you
pass are sent; passing none makes no API call.

## List Features

To list features in a domain:

```python
features = ff.list_features(domain)
```

To list features across all your domains, omit the domain:

```python
all_features = ff.list_features()
```

Narrow the results with filters:

```python
roads = ff.list_features(domain, feature_type="road")
osm_features = ff.list_features(domain, product="osm")
tagged = ff.list_features(domain, tag="roads")
```

Sort a page by name, creation time, or modification time:

```python
newest_first = ff.list_features(
    domain,
    sort_by="created_on",
    sort_order="descending",
)
```

## Delete a Feature

To permanently delete a feature and its generated data:

```python
feature.delete()
```

Deleting a domain also deletes all of its features.

## Error Handling

Wrapper functions and methods raise typed exceptions from
`fastfuels_sdk.v2.exceptions`:

```python
import fastfuels_sdk.v2 as ff
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

try:
    feature = ff.get_feature(domain, "does-not-exist")
except NotFoundException:
    print("No such feature (or you don't have access to it)")

try:
    metadata = pending_feature.get_data_metadata()
except UnprocessableEntityException as exc:
    print(exc.detail)
    # features/36573c0205d147a08011693b7894c0fb status is 'pending',
    # expected 'completed'.
```
