# How to Create a Tree Inventory from Point Cloud Data

This guide shows you how to create a tree inventory from airborne laser scanning (ALS) point cloud data. Point cloud-derived inventories use LiDAR to segment individual trees, producing high-fidelity tree locations and heights directly from remote sensing data.

For learning the basics, see the [Getting Started tutorial]. For detailed reference, see the [API Reference].

## How to Create an ALS Point Cloud from 3DEP

Before creating a tree inventory from point cloud data, you need an ALS point cloud resource in your domain. The simplest approach uses publicly available [USGS 3DEP](https://www.usgs.gov/3d-elevation-program) data:

```python
from fastfuels_sdk import PointClouds

# Initialize from your domain
point_clouds = PointClouds.from_domain_id("your_domain_id")

# Create ALS point cloud from 3DEP data
als_point_cloud = point_clouds.create_als_point_cloud(sources=["3DEP"])

# Wait for processing to complete (this may take several minutes)
als_point_cloud.wait_until_completed(verbose=True)
```

Processing time depends on your domain size. Use `verbose=True` to monitor progress.

## How to Create a Tree Inventory from Point Cloud Data

Once the ALS point cloud is completed, create a tree inventory from it:

```python
from fastfuels_sdk import Inventories

# Initialize from your domain
inventories = Inventories.from_domain_id("your_domain_id")

# Create tree inventory from the point cloud
tree_inventory = inventories.create_tree_inventory_from_point_cloud()

# Wait for processing to complete
tree_inventory = tree_inventory.wait_until_completed()
```

The point cloud processing pipeline segments individual trees from the ALS data to derive tree locations and heights.

## How to Check Point Cloud Status

To check whether a domain already has an ALS point cloud:

```python
point_clouds = PointClouds.from_domain_id("your_domain_id")

if point_clouds.als:
    print(f"ALS point cloud status: {point_clouds.als.status}")
else:
    print("No ALS point cloud exists for this domain")
```

To refresh the status of an existing point cloud:

```python
als_point_cloud = point_clouds.als.get()
print(f"Status: {als_point_cloud.status}")
```

## How to Delete an ALS Point Cloud

To remove an ALS point cloud from your domain:

```python
point_clouds = PointClouds.from_domain_id("your_domain_id")

if point_clouds.als:
    point_clouds.als.delete()
```

## Complete Workflow Example

This example demonstrates the full workflow from domain creation to tree inventory export:

```python
import geopandas as gpd
from shapely.geometry import Polygon

from fastfuels_sdk import Domain, PointClouds, Inventories

# Step 1: Create a domain
coordinates = [
    [-113.43635, 46.89739],
    [-113.44842, 46.88948],
    [-113.44763, 46.88741],
    [-113.44994, 46.88585],
    [-113.44924, 46.88430],
    [-113.44274, 46.88390],
    [-113.43539, 46.88237],
    [-113.42006, 46.88523],
    [-113.42329, 46.88920],
    [-113.42361, 46.89257],
    [-113.42635, 46.89528],
    [-113.42696, 46.89597],
    [-113.42854, 46.89916],
    [-113.42711, 46.90211],
    [-113.42798, 46.90336],
    [-113.42933, 46.90300],
    [-113.43242, 46.90099],
    [-113.43446, 46.89802],
    [-113.43635, 46.89739],
]

polygon = Polygon(coordinates)
roi = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")

domain = Domain.from_geodataframe(
    geodataframe=roi,
    name="Lubrecht ALS Example",
    description="Lubrecht Experimental Forest",
    horizontal_resolution=2.0,
    vertical_resolution=1.0,
)

# Step 2: Create ALS point cloud
als_point_cloud = (
    PointClouds.from_domain_id(domain.id)
    .create_als_point_cloud(sources=["3DEP"])
)
als_point_cloud.wait_until_completed(verbose=True)

# Step 3: Create tree inventory from point cloud
tree_inventory = (
    Inventories.from_domain_id(domain.id)
    .create_tree_inventory_from_point_cloud()
)
tree_inventory = tree_inventory.wait_until_completed()

# Step 4: Export the inventory
export = tree_inventory.create_export("csv")
export = export.wait_until_completed()
export.to_file("point_cloud_trees.csv")
```

## Using the Convenience Function

You can accomplish the entire point cloud workflow with a single call to `export_roi()`:

```python
from fastfuels_sdk import export_roi

tree_inventory_config = {
    "source": "pointcloud",
    "pointCloudSources": ["3DEP"],
}

export = export_roi(
    roi=roi,
    export_path="als_export.zip",
    tree_inventory_config=tree_inventory_config,
    verbose=True,
)
```

This handles point cloud creation, tree inventory generation, grid creation, and export in a single function call.
