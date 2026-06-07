# Tutorial: Incorporate ALS Point Cloud Data into a FastFuels Domain

This tutorial walks you through incorporating airborne laser scanning (ALS / LiDAR) point cloud data into a FastFuels domain. Unlike TreeMap-based inventories that rely on statistical imputation, point cloud-derived inventories use LiDAR to segment individual trees directly from remote sensing data. This produces higher-fidelity tree locations and heights, which in turn enables more accurate canopy fuel grids for fire modeling.

## Prerequisites

Before starting this tutorial, make sure you have:

- FastFuels SDK installed (`pip install fastfuels-sdk`)
- A valid FastFuels API key
- Basic familiarity with Python and GeoPandas

## What You'll Learn

By the end of this tutorial, you'll understand:

- Why point cloud data produces higher-fidelity tree inventories than TreeMap
- How the ALS pipeline works: point cloud creation, tree segmentation, and inventory generation
- When to choose point cloud-based inventories over other data sources

## When to Use Point Cloud Data

FastFuels supports three tree inventory sources, each suited to different use cases:

- **TreeMap**: Nationwide statistical coverage based on FIA plot data. Best for large-area studies where broad coverage matters more than local precision.
- **File upload**: Your own field measurements. Best when you have site-specific survey data.
- **Point cloud**: ALS/LiDAR-derived tree segmentation. Best when you need spatially explicit tree positions and heights that reflect actual canopy structure.

Point cloud inventories are particularly valuable when:

- Your study area has 3DEP LiDAR coverage (check [USGS 3DEP availability](https://www.usgs.gov/3d-elevation-program))
- Accurate tree positions matter for your fire modeling scenario
- You want tree heights derived from direct measurement rather than statistical imputation

The trade-off is processing time — point cloud inventories take longer to generate than TreeMap inventories because the pipeline must download, process, and segment the raw LiDAR data.

## Step 1: Create a Domain

First, define a region of interest. This example uses an area in the Lubrecht Experimental Forest in Montana:

```python
import geopandas as gpd
from shapely.geometry import Polygon
from fastfuels_sdk import Domain

coordinates = [
    [-113.43635167116199, 46.89738742250387],
    [-113.44842074255764, 46.88947859763070],
    [-113.44763362920567, 46.88740657162339],
    [-113.44993666456837, 46.88585249958990],
    [-113.44923700825561, 46.88429838253265],
    [-113.44273603501621, 46.88389988372731],
    [-113.43538964373204, 46.88236563568933],
    [-113.42005550954369, 46.88523484307359],
    [-113.42329141999039, 46.88919967571519],
    [-113.42361209580038, 46.89256656477321],
    [-113.42635241635870, 46.89527586047467],
    [-113.42696461563226, 46.89597308354718],
    [-113.42853884233625, 46.89916027357725],
    [-113.42711037736427, 46.90210825569156],
    [-113.42798494775504, 46.90336309078498],
    [-113.42932595568779, 46.90300456946972],
    [-113.43241610440292, 46.90099282206219],
    [-113.43445676864847, 46.89802485885190],
    [-113.43635167116199, 46.89738742250387],
]

roi = gpd.GeoDataFrame(
    geometry=[Polygon(coordinates)],
    crs="EPSG:4326",
)

domain = Domain.from_geodataframe(
    geodataframe=roi,
    name="Lubrecht ALS Example",
    description="Lubrecht Experimental Forest - ALS tutorial",
    horizontal_resolution=2.0,
    vertical_resolution=1.0,
)

print(f"Created domain with ID: {domain.id}")
```

## Step 2: Create an ALS Point Cloud

With the domain created, the next step is to fetch ALS data. The SDK retrieves publicly available LiDAR data from the USGS 3D Elevation Program (3DEP) and processes it within your domain's spatial extent.

```python
from fastfuels_sdk import PointClouds

als_point_cloud = (
    PointClouds.from_domain_id(domain.id)
    .create_als_point_cloud(sources=["3DEP"])
)

als_point_cloud.wait_until_completed(verbose=True)
```

This step downloads the relevant 3DEP tiles, clips them to your domain boundary, and prepares the point cloud for tree segmentation. Processing time depends on domain size and data density — expect anywhere from a few seconds to several minutes.

## Step 3: Create a Tree Inventory from the Point Cloud

Once the point cloud is ready, the SDK can segment individual trees from it. This process identifies tree tops, delineates crowns, and extracts tree-level attributes (location and height) from the LiDAR returns.

```python
from fastfuels_sdk import Inventories

tree_inventory = (
    Inventories.from_domain_id(domain.id)
    .create_tree_inventory_from_point_cloud()
)

tree_inventory = tree_inventory.wait_until_completed()
```

The point cloud must be in `"completed"` status before this step. If you call `create_tree_inventory_from_point_cloud()` before the point cloud finishes, the API will return an error.

## What's Next

With a completed tree inventory, you can:

- **Create fuel grids** for fire modeling — see the [Export to QUIC-Fire tutorial](export_to_quicfire.md)
- **Export the inventory** to CSV, Parquet, or GeoJSON for analysis
- **Manage point cloud resources** (check status, delete) — see the [Point Clouds how-to guide](../guides/point_clouds.md)

For quick-reference on the point cloud API, see the [Point Clouds how-to guide](../guides/point_clouds.md).
