---
title: How to Work with FastFuels Inventory Data
description: Learn how to create, manage, and export inventory data using the FastFuels SDK
---

# How to Work with FastFuels Inventory Data

This guide shows you how to work with inventory data using the FastFuels SDK. You'll learn how to create and manage different types of inventories, with a focus on tree inventories which are currently the main type available. The patterns shown here will apply to other inventory types (such as shrub, log, or grass inventories) as they become available.

## Getting Started with Inventories

Every inventory in FastFuels belongs to a domain. Start by initializing an Inventories object from your domain:

```python
from fastfuels_sdk import Domain, Inventories

domain = Domain.from_id("your_domain_id")
inventories = Inventories.from_domain(domain)
```

Check what inventories currently exist:

```python
# Get latest inventory data
inventories = inventories.get()

# Check available inventories
if inventories.tree:
    print("Tree inventory exists")
```

## Working with Tree Inventories

### Creating a Basic Tree Inventory

The simplest way to create a tree inventory is using TreeMap data:

```python
tree_inventory = inventories.create_tree_inventory(sources="TreeMap")
```

Tree inventory creation happens asynchronously. Wait for processing to complete:

```python
tree_inventory.wait_until_completed(in_place=True)
print(f"Status: {tree_inventory.status}")  # Should print 'completed'
```

### Customizing Your Tree Inventory

#### Control TreeMap Source Settings

You can specify the TreeMap version and set a seed for reproducible results:

```python
tree_inventory = inventories.create_tree_inventory(
    sources="TreeMap",
    tree_map={
        "version": "2016",  # Use 2014 or 2016
        "seed": 42         # For reproducible results
    }
)
```

#### Modify Tree Attributes

Apply modifications to tree attributes based on conditions:

```python
tree_inventory = inventories.create_tree_inventory(
    sources="TreeMap",
    modifications={
        "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
        "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
    }
)
```

Available fields for modifications:
- `HT`: Height (meters)
- `DIA`: Diameter at breast height (centimeters)
- `CR`: Crown ratio (0-1)
- `SPCD`: Species code (integer)

#### Add Silvicultural Treatments

Apply proportional thinning to reach a target basal area:

```python
tree_inventory = inventories.create_tree_inventory(
    sources="TreeMap",
    treatments={
        "method": "proportionalThinning",
        "targetMetric": "basalArea",
        "targetValue": 25.0  # Target in m²/ha
    }
)
```

Or use directional thinning:

```python
tree_inventory = inventories.create_tree_inventory(
    sources="TreeMap",
    treatments={
        "method": "directionalThinning",
        "direction": "below",        # or "above"
        "targetMetric": "diameter",  # or "basalArea"
        "targetValue": 30.0         # cm for diameter, m²/ha for basalArea
    }
)
```

#### Exclude Features

Mask out specific features to exclude trees from those areas:

```python
tree_inventory = inventories.create_tree_inventory(
    sources="TreeMap",
    feature_masks=["road", "water"]
)
```

### Exporting Inventory Data

1. Create an export in your desired format:

```python
# Available formats: "csv", "parquet", "geojson"
export = tree_inventory.create_export("csv")
```

2. Wait for the export to complete and download:

```python
from pathlib import Path

export.wait_until_completed(in_place=True)

# Download with specific filename
export.to_file(Path("trees.csv"))

# Or download to a directory (uses default filename)
export.to_file(Path("output_directory"))
```

### Managing Inventories

Check inventory status:

```python
# Get latest status for all inventories
inventories = inventories.get()

# Check specific tree inventory status
if inventories.tree:
    tree_inventory = inventories.tree.get()
    print(f"Tree inventory status: {tree_inventory.status}")
```

Delete an inventory:

```python
if inventories.tree:
    inventories.tree.delete()
```

## Complete Example

Here's a complete example showing how to create and process a tree inventory with multiple options:

```python
# Create inventory with multiple settings
tree_inventory = inventories.create_tree_inventory(
    sources="TreeMap",
    tree_map={"version": "2016", "seed": 42},
    modifications={
        "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
        "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
    },
    treatments={
        "method": "proportionalThinning",
        "targetMetric": "basalArea",
        "targetValue": 25.0
    },
    feature_masks=["road", "water"]
)

# Wait for processing to complete
tree_inventory.wait_until_completed(in_place=True)

# Create and download export
export = tree_inventory.create_export("csv")
export.wait_until_completed(in_place=True)
export.to_file(Path("processed_trees.csv"))
```
