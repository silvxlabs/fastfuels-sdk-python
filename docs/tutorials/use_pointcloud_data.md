
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
- Build tree grids using ALS-informed inventories
- Create a Surface Grid utilizing the Fuel Characteristic Classification System

## Step 1: Create a FastFuels Domain

For the polygon created by the coordinates:
```python
>>> from fastfuels_sdk import Inventories
        >>> inventories = Inventories.from_domain_id("abc123")
        >>>
        >>> # Create tree inventory from existing point cloud
        >>> inventory = inventories.create_tree_inventory_from_point_cloud()
        >>> inventory.wait_until_completed()
```
Complete Steps 1–6 of the tutorial “Create and Export QUIC-Fire Inputs with FastFuels SDK”, including:
- Authentication
- Region of interest (ROI) - using these coordinates
- Domain creation
- Road and water features
- Feature grid
- Topography grid

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

## Step 3: Create Tree Inventory and Grid using the point cloud data

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

# Create tree grid
tree_grid = (
    TreeGridBuilder(domain_id=domain.id)
    .with_bulk_density_from_tree_inventory()
    .build()
)
tree_grid.wait_until_completed()
```

## Step 4: Create Surface Grid

Generate the surface fuels grid using LandFire's Fuel Characteristic Classification System

```python
from fastfuels_sdk.grids import SurfaceGridBuilder

surface_grid = (
    SurfaceGridBuilder(domain_id=domain.id)
    .with_fuel_load_from_landfire(
        product="FCCS",
        version="2023",
        interpolation_method="cubic",
        groups=["oneHour"],
        feature_masks=["road", "water"],
        remove_non_burnable=["NB1", "NB2"],
    )
    .with_fuel_depth_from_landfire(
        product="FCCS",
        version="2023",
        interpolation_method="cubic",
        feature_masks=["road", "water"],
        remove_non_burnable=["NB1", "NB2"],
    )
    .with_uniform_fuel_moisture(
        value=0.15,
        feature_masks=["road", "water"]
    )
    .build()
)
surface_grid.wait_until_completed()
```

## Step 5: Export to ZARR Format

Create and download the zarr export:

```python
from fastfuels_sdk.grids import Grids
from pathlib import Path

# Create the export
export = Grids.from_domain_id(domain.id).create_export("zarr")
export.wait_until_completed()

# Download to a local directory
export_path = Path("zarr_export")
export.to_file(export_path)
```

## Next Steps
For additional guidance and complementary workflows, refer back to the “Create and Export QUIC-Fire Inputs with FastFuels SDK” tutorial.
