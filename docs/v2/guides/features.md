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

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- An existing [domain](domains.md) to create features in

## Create a Road Feature from OpenStreetMap

To extract the road network within a domain's extent:

```python
from fastfuels_sdk.v2 import Feature

feature = Feature.create_osm_road(
    domain.id,
    name="My Roads",
    description="OSM road network",
)

print(feature.status)  # JobStatus.PENDING
```

Feature generation runs as a background job — the returned feature starts
in `"pending"` status. To include roads just outside the domain, buffer
the query extent by up to 100 meters with `extent_buffer_m`:

```python
feature = Feature.create_osm_road(domain.id, extent_buffer_m=50)
```

## Create a Water Feature from OpenStreetMap

To extract water bodies, use the same calling convention:

```python
feature = Feature.create_osm_water(domain.id, name="My Water")
```

## Wait for a Feature to Complete

To block until a feature job finishes:

```python
feature.wait_until_completed(verbose=True)
```

```text
Feature 36573c0205d147a08011693b7894c0fb: pending (5s)
Feature 36573c0205d147a08011693b7894c0fb: running (15s)
Feature 36573c0205d147a08011693b7894c0fb: completed (20s)
```

`wait_until_completed` raises `TimeoutError` if the job exceeds `timeout`
seconds (default 600) and `RuntimeError` if the job fails. Once
completed, the feature's `georeference` reports the CRS and bounds of the
generated data:

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

with open("fuelbeds.geojson") as f:  # projected CRS + fuelbed properties
    geojson = json.load(f)

feature = Feature.create_layerset(domain.id, geojson, name="My Fuelbeds")

print(feature.status)  # JobStatus.COMPLETED
```

To upload from a GeoPandas GeoDataFrame instead, reproject first if
needed — the GeoDataFrame's CRS is forwarded as-is:

```python
import geopandas as gpd

gdf = gpd.read_file("fuelbeds.shp").to_crs(epsg=5070)
feature = Feature.create_layerset_from_geodataframe(domain.id, gdf)
```

## Retrieve an Existing Feature

To fetch a feature using its domain and feature IDs:

```python
feature = Feature.from_id(domain.id, "36573c0205d147a08011693b7894c0fb")
```

## Get Fresh Feature Data

To fetch the latest state of a feature (for example, to check job
progress yourself):

```python
# Get new instance with fresh data
fresh_feature = feature.get()

# Or refresh the existing instance
feature.get(in_place=True)
```

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
# Create new instance with updates
updated_feature = feature.update(name="New Name", tags=["roads", "osm"])

# Or update in-place
feature.update(name="New Name", in_place=True)
```

## List Features

To list features in a domain:

```python
from fastfuels_sdk.v2 import list_features

features = list_features(domain.id)
```

To list features across all your domains, omit the domain ID:

```python
all_features = list_features()
```

Narrow the results with filters:

```python
roads = list_features(domain.id, feature_type="road")
osm_features = list_features(domain.id, product="osm")
tagged = list_features(domain.id, tag="roads")
```

## Delete a Feature

To permanently delete a feature and its generated data:

```python
feature.delete()
```

Deleting a domain also deletes all of its features.

## Error Handling

Wrapper methods raise typed exceptions from
`fastfuels_sdk.v2.exceptions`:

```python
from fastfuels_sdk.v2 import Feature
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

try:
    feature = Feature.from_id(domain.id, "does-not-exist")
except NotFoundException:
    print("No such feature (or you don't have access to it)")

try:
    metadata = pending_feature.get_data_metadata()
except UnprocessableEntityException as exc:
    print(exc.detail)
    # features/36573c0205d147a08011693b7894c0fb status is 'pending',
    # expected 'completed'.
```
