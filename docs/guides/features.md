# How to Work with Features in FastFuels SDK

This guide shows you how to work with geographic features (roads and water bodies) in your domains using the FastFuels SDK.

## Get Features for a Domain

Features are always associated with a domain. To access features:

```python
from fastfuels_sdk import Features

# Get Feature data from an existing domain ID.
features = Features.from_domain_id("your_domain_id")
```

# Check what features exist
if features.road:
    print("Domain has road features")
if features.water:
    print("Domain has water features")
```

## Create Road Features

### Basic Road Feature Creation

The simplest way to create road features is using OpenStreetMap (OSM) data:

```python
# Using the convenience method
road = features.create_road_feature_from_osm()

# Or the general method
road = features.create_road_feature(sources="OSM")
```

### Update Features Instance

To automatically update the Features object when creating road features:

```python
# Create features and update the Features instance
road = features.create_road_feature_from_osm(in_place=True)

# Now features.road points to the new road features
assert features.road is road
```

### Wait for Processing

Road feature creation happens asynchronously. Wait for processing to complete:

```python
# Wait with status updates
road.wait_until_completed(
    step=5,          # Check every 5 seconds
    timeout=300,     # Wait up to 5 minutes
    verbose=True     # Print status updates
)

print(f"Status: {road.status}")  # Should print 'completed'
```

## Create Water Features

### Basic Water Feature Creation

Similar to roads, create water features from OSM data:

```python
# Using the convenience method
water = features.create_water_feature_from_osm()

# Or the general method
water = features.create_water_feature(sources="OSM")

# Wait for processing
water.wait_until_completed(in_place=True)
```

### Update Features Instance

To automatically update the Features object:

```python
water = features.create_water_feature_from_osm(in_place=True)
assert features.water is water
```

## Get Updated Feature Data

### Refresh All Features

To get the latest data for all features:

```python
# Get new instance with fresh data
updated_features = features.get()

# Or update in place
features.get(in_place=True)
```

### Refresh Specific Features

To update just road or water features:

```python
if features.road:
    # Get new instance with fresh data
    updated_road = features.road.get()
    
    # Or update in place
    features.road.get(in_place=True)

if features.water:
    # Get new instance with fresh data
    updated_water = features.water.get()
    
    # Or update in place
    features.water.get(in_place=True)
```

## Delete Features

### Delete Road Features

To remove road features from a domain:

```python
if features.road:
    # Delete the road features
    features.road.delete()
    
    # Refresh features to reflect deletion
    features.get(in_place=True)
    assert features.road is None
```

### Delete Water Features

Similarly for water features:

```python
if features.water:
    # Delete the water features
    features.water.delete()
    
    # Refresh features to reflect deletion
    features.get(in_place=True)
    assert features.water is None
```

## Complete Example

Here's a complete example showing how to work with both road and water features:

```python
from fastfuels_sdk import Features

# Get domain and features
features = Features.from_domain_id("your_domain_id")

# Create road features and wait for completion
road = features.create_road_feature_from_osm(in_place=True)
road.wait_until_completed(verbose=True)

# Create water features and wait for completion
water = features.create_water_feature_from_osm(in_place=True)
water.wait_until_completed(verbose=True)

# Get latest feature data
features.get(in_place=True)

# Process based on feature status
if features.road and features.road.status == "completed":
    print("Road features ready")
if features.water and features.water.status == "completed":
    print("Water features ready")

# Clean up when done
if features.road:
    features.road.delete()
if features.water:
    features.water.delete()
```