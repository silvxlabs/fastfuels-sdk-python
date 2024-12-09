# How to Work with Domains in FastFuels SDK

## Create a Domain from GeoJSON

To create a domain from a GeoJSON file:

```python
import json
from fastfuels_sdk.domains import Domain

with open("area.geojson") as f:
    geojson = json.load(f)
    
domain = Domain.from_geojson(
    geojson=geojson,
    name="My Domain",
    description="Forest area for analysis",
    horizontal_resolution=2.0,
    vertical_resolution=1.0
)
```

## Create a Domain from a GeoDataFrame

If your spatial data is in a format supported by GeoPandas (Shapefile, KML etc.):

```python
import geopandas as gpd
from fastfuels_sdk.domains import Domain

gdf = gpd.read_file("forest_area.shp")

domain = Domain.from_geodataframe(
    geodataframe=gdf,
    name="Forest Domain",
    description="Imported from shapefile",
    horizontal_resolution=2.0
)
```

## Retrieve an Existing Domain

To fetch a domain using its ID:

```python
domain = Domain.from_id("abc123")
```

## Update Domain Properties 

To modify a domain's name, description or tags:

```python
# Create new instance with updates
updated_domain = domain.update(
    name="New Name",
    description="Updated description",
    tags=["forest", "analysis"]
)

# Or update in-place
domain.update(
    name="New Name",
    in_place=True
)
```

## Get Fresh Domain Data

To fetch the latest data for a domain:

```python
# Get new instance with fresh data
fresh_domain = domain.get()

# Or refresh existing instance
domain.get(in_place=True)
```

## List Available Domains

To list domains with pagination:

```python
from fastfuels_sdk.domains import list_domains

# Get first page with default size (100)
response = list_domains()

# Custom page and size 
response = list_domains(
    page=2,
    size=50,
    sort_by="name",
    sort_order="ascending"
)

for domain in response.domains:
    print(f"{domain.id}: {domain.name}")
```

## Delete a Domain

To permanently delete a domain:

```python
domain.delete()
```