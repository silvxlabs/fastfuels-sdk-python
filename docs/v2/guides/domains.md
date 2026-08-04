# How to Work with Domains in FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

A domain is the spatial container every other FastFuels resource lives in.
This guide covers working with domains from Python; for what domains *are*
and how the platform treats them, see the
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com). Coming
from the v1 SDK? Start with the [migration guide](migration.md#domains).

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key

The v2 SDK reads your API key from the `FASTFUELS_API_KEY` environment
variable, the same variable the v1 SDK uses:

```bash
export FASTFUELS_API_KEY="your-api-key"
```

Or set it programmatically:

```python
from fastfuels_sdk.v2 import set_api_key

set_api_key("your-api-key")
```

## Create a Domain from GeoJSON

To create a domain from a GeoJSON file:

```python
import json
from fastfuels_sdk.v2.domains import Domain

with open("area.geojson") as f:
    geojson = json.load(f)

domain = Domain.from_geojson(
    geojson=geojson,
    name="My Domain",
    description="Forest area for analysis",
    pad_to_resolution=2.0,
)
```

The v2 API accepts a GeoJSON FeatureCollection; the SDK automatically
wraps a single Feature for you.

## Create a Domain from a GeoDataFrame or a File

If your spatial data is in a format supported by GeoPandas (Shapefile,
KML, GeoPackage, etc.):

```python
import geopandas as gpd
from fastfuels_sdk.v2.domains import Domain

gdf = gpd.read_file("forest_area.shp")

domain = Domain.from_geodataframe(
    geodataframe=gdf,
    name="Forest Domain",
    description="Imported from shapefile",
)

# Or skip the GeoPandas step entirely:
domain = Domain.from_file("forest_area.shp", name="Forest Domain")
```

## Preview a Domain Before Creating It

`Domain.preview` runs the same validation and projection pipeline as
creation but persists nothing — useful for showing a user the projected,
padded bounding box before committing:

```python
previewed = Domain.preview(geojson, pad_to_resolution=2.0)

print(previewed.id)    # always "preview" — not a real identifier
print(previewed.bbox)  # the projected, padded bounding box
```

## Retrieve an Existing Domain

To fetch a domain using its ID:

```python
domain = Domain.from_id("abc123")
```

## Update Domain Properties

To modify a domain's name, description, or tags:

```python
domain.update(
    name="New Name",
    description="Updated description",
    tags=["forest", "analysis"],
)
```

`update` changes the domain in place and returns it, so calls chain. Only
the fields you pass are sent; passing none makes no API call.

## Refresh Domain Data

To reload a domain's latest state from the API in place:

```python
domain.refresh()
```

`refresh` updates the domain in place and returns it. To fetch a separate
copy by ID instead, use `Domain.from_id(domain.id)`.

## Get the Pixel Lattice for a Domain

To align a raster with the grids FastFuels will produce for a domain,
fetch its pixel lattice (affine transform + shape) at a resolution:

```python
lattice = domain.get_lattice(resolution=2.0)

print(lattice.crs)        # e.g. "EPSG:32611"
print(lattice.transform)  # affine coefficients [a, b, c, d, e, f]
print(lattice.shape)      # [height, width] in pixels

# Expand the lattice by N cells on each side, mirroring the
# extent_buffer_cells semantics of the grid creation endpoints
buffered = domain.get_lattice(resolution=2.0, num_buffer_cells=5)
```

## Reproject GeoJSON

A stateless utility — no resource is created:

```python
from fastfuels_sdk.v2.domains import reproject_geojson

projected = reproject_geojson(geojson, target_epsg=5070)
print(projected["crs"]["properties"]["name"])  # "EPSG:5070"
```

## List Available Domains

To list domains with pagination:

```python
from fastfuels_sdk.v2.domains import list_domains

# Get first page with default size (100)
domains = list_domains()

# Custom page and size
domains = list_domains(
    page=2,
    size=50,
    sort_by="name",
    sort_order="ascending",
)

for domain in domains:
    print(f"{domain.id}: {domain.name}")
```

## Delete a Domain

To permanently delete a domain and all resources associated with it:

```python
domain.delete()
```

## Error Handling

Wrapper methods raise typed exceptions from
`fastfuels_sdk.v2.exceptions`:

```python
from fastfuels_sdk.v2.domains import Domain
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

try:
    domain = Domain.from_id("does-not-exist")
except NotFoundException:
    print("No such domain (or you don't have access to it)")

try:
    domain = Domain.from_geojson(too_big_geojson)
except UnprocessableEntityException as exc:
    print(f"Invalid domain: {exc.detail}")
```
