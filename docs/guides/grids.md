# How to Work with Grids in FastFuels SDK

This guide shows you how to work with grid data in the FastFuels SDK. Grids contain spatial data about terrain, vegetation, and other features within a domain's boundaries.

## Creating and Updating Grid Objects

### How to Create a Grids Object

To work with grids, you first need to create a Grids object from an existing domain ID. Here's how to do it:

```python
from fastfuels_sdk import Grids

# Create a Grids object from a domain ID
domain_id = "abc123"  # Replace with your domain ID
grids = Grids.from_domain_id(domain_id)
```

Once you have a Grids object, you can check which types of grids are available:

```python
# Check for available grid types
if grids.tree:
    print("Domain has tree canopy data")
if grids.surface:
    print("Domain has surface fuel data")
if grids.topography:
    print("Domain has elevation data")
if grids.feature:
    print("Domain has geographic feature data")
```

### How to Update Grid Data

Grid data can change over time as new data becomes available or processing completes. There are two ways to update your Grids object with the latest data:

1. Create a new Grids object with updated data:
```python
# Get fresh data in a new instance
updated_grids = grids.get()
```

2. Update the existing Grids object in place:
```python
# Update the existing instance
grids.get(in_place=True)
```

Choose the first approach if you want to compare old and new data, or the second approach if you just want to ensure you're working with the latest data.

## Creating Grids Directly

Once you have a Grids object, you can create different types of grids directly using its creation methods:

### Surface Grids

Surface grids contain data about surface fuels. Create them using `create_surface_grid()`:

```python
# Create a simple surface grid with uniform values
surface_grid = grids.create_surface_grid(
    attributes=["fuelLoad", "fuelMoisture"],
    fuel_load={"source": "uniform", "value": 0.5},
    fuel_moisture={"source": "uniform", "value": 15.0}
)
```

### Topography Grids 

Topography grids contain elevation and terrain data. Create them using `create_topography_grid()`:

```python
# Create a topography grid using 3DEP data
topo_grid = grids.create_topography_grid(
    attributes=["elevation", "slope"],
    elevation={"source": "3DEP", "interpolationMethod": "cubic"},
    slope={"source": "3DEP", "interpolationMethod": "cubic"}
)
```

### Tree Grids

Tree grids contain canopy and tree data. Create them using `create_tree_grid()`:

```python
# Create a tree grid with inventory and uniform values
tree_grid = grids.create_tree_grid(
    attributes=["bulkDensity", "SPCD", "fuelMoisture"],
    bulk_density={"source": "inventory"},
    spcd={"source": "inventory"},
    fuel_moisture={"source": "uniform", "value": 15.0}
)
```

### Feature Grids

Feature grids contain geographic features. Create them using `create_feature_grid()`:

```python
# Create a feature grid with roads and water bodies
feature_grid = grids.create_feature_grid(
    attributes=["roads", "water_bodies"]
)
```

## Using Grid Builders

For more complex grid configurations, FastFuels SDK provides builder classes that offer a fluent interface and better parameter validation. The builders help construct grid configurations step by step.

Key benefits of using builders:
- Clearer, more readable code
- Better parameter validation
- Chainable methods
- Reusable configurations

### Surface Grid Builder

The SurfaceGridBuilder helps create surface grids with complex configurations:

```python
from fastfuels_sdk import SurfaceGridBuilder

# Create a surface grid with multiple attributes
surface_grid = (SurfaceGridBuilder("abc123")
    .with_fuel_load_from_landfire(
        product="FBFM40",
        version="2022",
        feature_masks=["road", "water"]
    )
    .with_uniform_fuel_moisture_by_size_class(
        one_hour=10.0,
        ten_hour=15.0,
        hundred_hour=20.0,
        live_herbaceous=75.0,
        live_woody=90.0
    )
    .with_modification(
        actions={"attribute": "FBFM", "modifier": "replace", "value": "GR2"},
        conditions={"attribute": "FBFM", "operator": "eq", "value": "GR1"}
    )
    .build())
```

### Topography Grid Builder

The TopographyGridBuilder helps create topography grids:

```python
from fastfuels_sdk import TopographyGridBuilder

# Create a topography grid with multiple data sources
topo_grid = (TopographyGridBuilder("abc123")
    .with_elevation_from_3dep(interpolation_method="cubic")
    .with_slope_from_landfire(interpolation_method="cubic")
    .with_aspect_from_3dep()
    .build())
```

### Tree Grid Builder

The TreeGridBuilder helps create tree grids:

```python
from fastfuels_sdk import TreeGridBuilder

# Create a tree grid with inventory and uniform values
tree_grid = (TreeGridBuilder("abc123")
    .with_bulk_density_from_tree_inventory()
    .with_spcd_from_tree_inventory()
    .with_uniform_fuel_moisture(15.0)
    .build())
```

### Best Practices for Builders

When using grid builders:

1. Clear the builder if reusing it for multiple grids:
```python
builder = SurfaceGridBuilder("abc123")
grid1 = builder.with_uniform_fuel_load(0.5).build()
builder.clear()  # Reset the builder
grid2 = builder.with_uniform_fuel_moisture(15.0).build()
```

2. Chain methods for better readability:
```python
grid = (builder
    .with_uniform_fuel_load(0.5)
    .with_uniform_fuel_moisture(15.0)
    .build())
```

3. Use feature masks when appropriate to improve grid resolution:
```python
grid = (builder
    .with_fuel_load_from_landfire(
        product="FBFM40",
        feature_masks=["road", "water"],
        remove_non_burnable=["NB1", "NB2"]
    )
    .build())
```

## Exporting Grid Data

The Grids object provides methods to export grid data in different formats for use in fire behavior models. The two main export formats are:

- "zarr": A compressed array format for general use
- "QUIC-Fire": Specific format for the QUIC-Fire fire behavior model

### How to Export to QUIC-Fire Format

To export your grid data for use with QUIC-Fire:

```python
# Create the export
export = grids.create_export("QUIC-Fire")

# Wait for the export to complete
export.wait_until_completed()

# Save to a file
export.to_file("grid_data.zip")
```

The QUIC-Fire export creates a zip file containing:
- `treesrhof.dat`: Bulk density data
- `treesmoist.dat`: Moisture content data
- `treesdepth.dat`: Canopy depth data
- `topo.dat`: Topography data (if available)

### How to Check Export Status

You can check the status of an existing export:

```python
# Get the current status of an export
export = grids.get_export("QUIC-Fire")

# Check if it's ready
if export.status == "completed":
    export.to_file("grid_data.zip")
```

### Export Best Practices

When working with exports:

1. Always wait for completion before saving:
```python
export = grids.create_export("QUIC-Fire")
export.wait_until_completed()  # Blocks until export is ready
export.to_file("output.zip")
```

2. Handle exports asynchronously for large datasets:
```python
export = grids.create_export("QUIC-Fire")
# Do other work while export processes
status = grids.get_export("QUIC-Fire")
if status.status == "completed":
    export.to_file("output.zip")
```

3. Use zarr format for programmatic access to the data:
```python
export = grids.create_export("zarr")
export.wait_until_completed()
export.to_file("grid_data.zarr")
```