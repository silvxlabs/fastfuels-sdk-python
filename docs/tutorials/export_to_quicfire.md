from grids.test_feature_grid import feature_grid_fixture

# Tutorial: Create and Export QUIC-Fire Inputs with FastFuels SDK

In this tutorial, you'll learn how to use the FastFuels SDK to create QUIC-Fire input files for a region of interest. We'll walk through each step of the process, from authentication to final export.

## Prerequisites

Before starting this tutorial, make sure you have:
- FastFuels SDK installed (`pip install fastfuels-sdk`)
- A valid FastFuels API key
- Basic familiarity with Python and GeoPandas

## What You'll Learn

By the end of this tutorial, you'll know how to:
- Set up authentication for the FastFuels SDK
- Create and work with Domains
- Generate grids for fuels and topography
- Export the data to QUIC-Fire format
- Use the convenience function for simplified workflows

## Step 1: Set Up Authentication

First, let's configure the SDK with your API key. While you can use environment variables, we'll set it programmatically for this tutorial:

```python
from fastfuels_sdk import api

# Configure the API key
api.set_api_key("your-api-key-here")
```

## Step 2: Create a Region of Interest

Let's create a GeoDataFrame representing an area in the Blue Mountain Recreation Area:

```python
import geopandas as gpd
from shapely.geometry import Polygon

# Define the polygon coordinates for Blue Mountain area
coordinates = [
    [-114.09957018646286, 46.82933208815811],
    [-114.10141707482919, 46.828370407248826],
    [-114.10010954324228, 46.82690548814563],
    [-114.09560673134018, 46.8271123684554],
    [-114.09592544216444, 46.829058122675065],
    [-114.09957018646286, 46.82933208815811]
]

# Create a GeoDataFrame
polygon = Polygon(coordinates)
roi = gpd.GeoDataFrame(
    geometry=[polygon],
    crs="EPSG:4326"  # WGS 84 coordinate system
)
```

## Step 3: Create a Domain

Now let's create a Domain from our ROI:

```python
from fastfuels_sdk.domains import Domain

domain = Domain.from_geodataframe(
    geodataframe=roi,
    name="Blue Mountain ROI",
    description="Test area in Blue Mountain Recreation Area",
    horizontal_resolution=2.0,  # 2-meter horizontal resolution
    vertical_resolution=1.0     # 1-meter vertical resolution
)

print(f"Created domain with ID: {domain.id}")
```

## Step 4: Create Road and Water Features

Let's add road and water features from OpenStreetMap:

```python
from fastfuels_sdk.features import Features

# Initialize Features for our domain
features = Features.from_domain_id(domain.id)

# Create features from OpenStreetMap
road_feature = features.create_road_feature_from_osm()
water_feature = features.create_water_feature_from_osm()

# Wait for features to be ready
road_feature.wait_until_completed()
water_feature.wait_until_completed()
```

## Step 5: Create Feature Grid

Next, use the road and water features we created in [Step 4](#step-4-create-road-and-water-features) to generate a feature grid:

```python
from fastfuels_sdk.grids import Grids

# Create feature grid
feature_grid = (
    Grids.from_domain_id(domain.id)
    .create_feature_grid(
        attributes=["road", "water"],
    )
)

feature_grid.wait_until_completed()

```

This will be used to mask out trees and non-burnable areas when we create the tree inventory in [Step 7](#step-7-create-tree-inventory-and-grid) and the surface grid in [Step 8](#step-8-create-surface-grid).

## Step 6: Create Topography Grid

Add elevation data from 3DEP:

```python
from fastfuels_sdk.grids import TopographyGridBuilder

topography_grid = (
    TopographyGridBuilder(domain_id=domain.id)
    .with_elevation_from_3dep(interpolation_method="linear")
    .build()
)

topography_grid.wait_until_completed()
```

## Step 7: Create Tree Inventory and Grid

Create a tree inventory and generate the canopy fuel grid:

```python
from fastfuels_sdk.inventories import Inventories
from fastfuels_sdk.grids import TreeGridBuilder

# Create tree inventory
tree_inventory = Inventories.from_domain_id(
    domain.id
).create_tree_inventory_from_treemap(
    feature_masks=["road", "water"]
)
tree_inventory.wait_until_completed()

# Create tree grid
tree_grid = (
    TreeGridBuilder(domain_id=domain.id)
    .with_bulk_density_from_tree_inventory()
    .build()
)
tree_grid.wait_until_completed()
```

## Step 8: Create Surface Grid

Generate the surface fuels grid:

```python
from fastfuels_sdk.grids import SurfaceGridBuilder

surface_grid = (
    SurfaceGridBuilder(domain_id=domain.id)
    .with_fuel_load_from_landfire(
        product="FBFM40",
        version="2022",
        interpolation_method="cubic",
        curing_live_herbaceous=0.25,
        curing_live_woody=0.1,
        groups=["oneHour"],
        feature_masks=["road", "water"],
        remove_non_burnable=["NB1", "NB2"],
    )
    .with_fuel_depth_from_landfire(
        product="FBFM40",
        version="2022",
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

## Step 9: Export to QUIC-Fire Format

Create and download the QUIC-Fire export:

```python
from fastfuels_sdk.grids import Grids
from pathlib import Path

# Create the export
export = Grids.from_domain_id(domain.id).create_export("QUIC-Fire")
export.wait_until_completed()

# Download to a local directory
export_path = Path("quicfire_export")
export.to_file(export_path)
```

## Using the Convenience Function

Now that you understand the complete process, you can use the convenience function to accomplish the same result with less code:

```python
from fastfuels_sdk.convenience import export_roi_to_quicfire

# Export using the convenience function
export = export_roi_to_quicfire(
    roi=roi,
    export_path=Path("quicfire_export"),
    verbose=True  # See progress updates
)
```

### Customizing the Export with Configuration Options

The `export_roi_to_quicfire()` function supports extensive configuration options that let you customize every aspect of the export process. Instead of writing complex builder chains (as shown in the manual process above), you can use simple dictionary-based configurations that mirror the underlying API structures.

**Why use configuration dictionaries?** They provide the same power as the manual approach but with much simpler syntax. Each configuration parameter in `export_roi_to_quicfire()` directly maps to the builder methods you saw earlier:

- `surface_config` → `SurfaceGridBuilder` methods
- `topography_config` → `TopographyGridBuilder` methods
- `tree_config` → `TreeGridBuilder` methods
- `features_config` → Feature creation controls
- `tree_inventory_config` → Tree inventory parameters

#### Most Common Use Cases

**Change surface fuel moisture (the #1 most common customization):**

This replaces the manual `.with_uniform_fuel_moisture()` call from Step 8 above:

```python
# Set surface fuel moisture to 5% for dry conditions
surface_config = {
    "fuelMoisture": {
        "source": "uniform",
        "value": 0.05,  # 5% moisture content
        "featureMasks": ["road", "water"]
    }
}

export = export_roi_to_quicfire(
    roi, "dry_conditions_export",
    surface_config=surface_config,
    verbose=True
)
```

**Use newer LANDFIRE data:**

This replaces the `version="2022"` parameters from the manual process:

```python
# Use LANDFIRE 2023 data instead of default 2022
surface_config = {
    "fuelLoad": {"version": "2023"},
    "fuelDepth": {"version": "2023"}
}

export = export_roi_to_quicfire(
    roi, "landfire_2023_export",
    surface_config=surface_config
)
```

**Skip water features for faster processing:**

This replaces the manual feature creation from Step 4:

```python
# Skip water feature creation (roads only)
features_config = {
    "createWaterFeatures": False
}

export = export_roi_to_quicfire(
    roi, "roads_only_export",
    features_config=features_config
)

#### Complete Configuration Reference

##### Topography Configuration

```python
topography_config = {
    "attributes": ["elevation"],
    "elevation": {
        "source": "3DEP",  # "3DEP", "LANDFIRE", or "uniform"
        "interpolationMethod": "linear"  # "linear", "cubic", or "nearest"
        # For uniform source only:
        # "value": 1500.0  # Elevation in meters
    }
}
```

##### Surface Configuration

```python
surface_config = {
    "attributes": ["fuelLoad", "fuelDepth", "fuelMoisture"],

    "fuelLoad": {
        "source": "LANDFIRE",  # "LANDFIRE" or "uniform"
        "product": "FBFM40",   # LANDFIRE product
        "version": "2022",     # LANDFIRE version year
        "interpolationMethod": "cubic",
        "curingLiveHerbaceous": 0.25,  # 0.0-1.0
        "curingLiveWoody": 0.1,        # 0.0-1.0
        "groups": ["oneHour", "tenHour", "hundredHour", "liveHerbaceous", "liveWoody"],
        "featureMasks": ["road", "water"],
        "removeNonBurnable": ["NB1", "NB2", "NB3", "NB8", "NB9"],
        # For uniform source only:
        # "value": 2.5  # kg/m²
    },

    "fuelDepth": {
        "source": "LANDFIRE",  # Similar structure to fuelLoad
        "product": "FBFM40",
        "version": "2022",
        "interpolationMethod": "cubic",
        "featureMasks": ["road", "water"],
        "removeNonBurnable": ["NB1", "NB2", "NB3", "NB8", "NB9"]
        # For uniform: "value": 0.3  # meters
    },

    "fuelMoisture": {
        "source": "uniform",  # Currently only uniform supported
        "value": 0.15,        # Moisture content (0.0-1.0)
        "featureMasks": ["road", "water"]
    }
}
```

##### Tree Configuration

```python
tree_config = {
    "attributes": ["bulkDensity", "fuelMoisture"],

    "bulkDensity": {
        "source": "inventory",  # "inventory" or "uniform"
        # For uniform source only:
        # "value": 0.5  # kg/m³
    },

    "fuelMoisture": {
        "source": "uniform",
        "value": 100  # Moisture content (typically 50-150)
    }
}
```

##### Features Configuration

```python
features_config = {
    "createRoadFeatures": True,     # Create road features from OSM
    "createWaterFeatures": True,    # Create water features from OSM
    "featureGridAttributes": ["road", "water"]  # Grid attributes to create
}
```

##### Tree Inventory Configuration

```python
tree_inventory_config = {
    "featureMasks": ["road", "water"]  # Features to mask from inventory
}
```

#### Advanced Configuration Examples

**Completely custom surface grid:**

```python
surface_config = {
    "fuelLoad": {
        "source": "uniform",
        "value": 1.5,  # kg/m²
        "featureMasks": ["road"]  # Only mask roads, not water
    },
    "fuelDepth": {
        "source": "uniform",
        "value": 0.2,  # meters
        "featureMasks": ["road"]
    },
    "fuelMoisture": {
        "source": "uniform",
        "value": 0.08,  # Very dry conditions (8%)
        "featureMasks": ["road"]
    }
}
```

**High-resolution with cubic interpolation:**

```python
topography_config = {
    "elevation": {
        "source": "3DEP",
        "interpolationMethod": "cubic"  # Higher quality interpolation
    }
}

surface_config = {
    "fuelLoad": {
        "interpolationMethod": "cubic",
        "groups": ["oneHour", "tenHour", "hundredHour"]  # Include more fuel classes
    },
    "fuelDepth": {
        "interpolationMethod": "cubic"
    }
}
```

**Roads-only configuration:**

```python
features_config = {
    "createRoadFeatures": True,
    "createWaterFeatures": False,    # Skip water features
    "featureGridAttributes": ["road"]  # Only roads in feature grid
}

# Update other configs to only mask roads
surface_config = {
    "fuelMoisture": {
        "source": "uniform",
        "value": 0.12,
        "featureMasks": ["road"]  # Only road masks
    }
}

tree_inventory_config = {
    "featureMasks": ["road"]  # Only mask roads from tree inventory
}
```

#### Configuration Tips

1. **Partial Overrides**: Only specify the parameters you want to change. The function will merge your configuration with sensible defaults.

2. **Feature Mask Consistency**: Make sure `featureMasks` in your surface and tree configs match the features you're actually creating.

3. **Performance Trade-offs**:
   - `"cubic"` interpolation is higher quality but slower
   - Disabling water features speeds up processing
   - Fewer fuel load groups process faster

4. **Validation**: The function validates your configuration against the API requirements and will provide helpful error messages.

5. **Backwards Compatibility**: Existing code without configuration parameters will continue to work exactly as before.

## Verifying the Export

Check your export directory for the QUIC-Fire input files:

```python
# List the exported files
for file in Path("quicfire_export").glob("*.dat"):
    print(f"Found QUIC-Fire input file: {file.name}")
```

You should see:
- `treesrhof.dat`: Fuel bulk density
- `treesmoist.dat`: Fuel moisture content
- `treesfueldepth.dat`: Surface fuel bed depth
- `topo.dat`: Elevation data

## Next Steps

Now that you can create QUIC-Fire inputs, you might want to:
- Experiment with different regions and resolutions
- Customize the grid parameters for your specific needs
- Learn about more advanced features of the FastFuels SDK

## Troubleshooting

If you encounter issues:
- Check that your API key is valid and properly configured
- Verify that your ROI polygon is valid and uses the correct coordinate system
- Ensure you have sufficient permissions to write to the export directory
- Check the status of resources using their `status` property
