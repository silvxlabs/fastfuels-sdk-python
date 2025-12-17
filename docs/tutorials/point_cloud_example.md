
# Tutorial: Incorporate ALS Point Cloud Data into a FastFuels Domain
This tutorial demonstrates how to incorporate airborne laser scanning (ALS / LiDAR) point cloud data into an existing FastFuels domain. It utilizes a point cloud–derived canopy structure to inform the tree inventory and canopy fuel grids, enabling higher‐fidelity fuels representation.

## Prerequisites

Before starting this tutorial, make sure you have:
- FastFuels SDK installed (`pip install fastfuels-sdk`)
- A valid FastFuels API key
- Basic familiarity with Python and GeoPandas

## What You'll Learn

By the end of this tutorial, you'll know how to:
- Create an ALS point cloud within a FastFuels domain
- Generate a tree inventory informed by the ALS data

## Step 1: Create a FastFuels Domain

For the polygon created by the coordinates:
```python
import geopandas as gpd
from shapely.geometry import Polygon

# Define the polygon coordinates for Lubrecht area
coordinates = [
    [-113.43635167116199,46.89738742250387],
    [-113.44842074255764,46.8894785976307],
    [-113.44763362920567,46.88740657162339],
    [-113.44993666456837,46.8858524995899],
    [-113.44923700825561,46.88429838253265],
    [-113.44273603501621,46.88389988372731],
    [-113.43538964373204,46.882365635689325],
    [-113.42005550954369,46.88523484307359],
    [-113.42329141999039,46.88919967571519],
    [-113.42361209580038,46.892566564773205],
    [-113.4263524163587,46.89527586047467],
    [-113.42696461563226,46.895973083547176],
    [-113.42853884233625,46.89916027357725],
    [-113.42711037736427,46.90210825569156],
    [-113.42798494775504,46.90336309078498],
    [-113.42932595568779,46.903004569469715],
    [-113.43241610440292,46.90099282206219],
    [-113.43445676864847,46.8980248588519],
    [-113.43635167116199,46.89738742250387]
]

# Create a GeoDataFrame
polygon = Polygon(coordinates)
roi = gpd.GeoDataFrame(
    geometry=[polygon],
    crs="EPSG:4326"  # WGS 84 coordinate system
)

from fastfuels_sdk.domains import Domain

domain = Domain.from_geodataframe(
    geodataframe=roi,
    name="Blue Mountain ROI",
    description="Test area in Lubrecht Experimental Forest",
    horizontal_resolution=2.0,  # 2-meter horizontal resolution
    vertical_resolution=1.0     # 1-meter vertical resolution
)

print(f"Created domain with ID: {domain.id}")
```

## Step 2: Create an ALS point cloud within FastFuels

Next, use 3DEP data to generate a feature point cloud:

```python
# 1.
from fastfuels_sdk.pointclouds import PointClouds

# 2. Correct Method Name & 3. Added Required 'sources' argument
als_pointcloud = (
    PointClouds.from_domain_id(domain.id)
    .create_als_point_cloud(sources=["3DEP"])
)

# This works because create_als_point_cloud returns the child object
als_pointcloud.wait_until_completed()

```

## Step 3: Create Tree Inventory using the point cloud data

Create a tree inventory and generate the canopy fuel grid:

```python
from fastfuels_sdk.inventories import Inventories
from fastfuels_sdk.grids import TreeGridBuilder

# Create tree inventory
# Note: Ensure Step 2 (Point Cloud creation) is fully completed before running this
tree_inventory = Inventories.from_domain_id(
    domain.id
).create_tree_inventory_from_point_cloud()
tree_inventory.wait_until_completed()
```

## Next Steps
For additional guidance and complementary workflows, refer back to the “Create and Export QUIC-Fire Inputs with FastFuels SDK” tutorial.