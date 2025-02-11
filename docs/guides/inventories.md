# How to Work with FastFuels Inventories

This guide shows you how to accomplish common tasks with FastFuels inventories. For learning the basics, see the [Getting Started tutorial]. For detailed reference, see the [API Reference].

## How to Create a Tree Inventory from TreeMap Data

To generate a tree inventory using TreeMap's nationwide coverage:

```python
from fastfuels_sdk import Inventories

# Initialize from your domain
inventories = Inventories.from_domain_id("your_domain_id")

# Create basic inventory
tree_inventory = inventories.create_tree_inventory_from_treemap()

# Wait for processing to complete
tree_inventory = tree_inventory.wait_until_completed()
```

To make the inventory reproducible, specify a seed:

```python
tree_inventory = inventories.create_tree_inventory_from_treemap(
    version="2016",
    seed=42
)
```

## How to Upload Your Own Tree Data

If you have your own tree measurements, you can upload them from a CSV file:

```python
from pathlib import Path

# Create inventory from your CSV file
tree_inventory = inventories.create_tree_inventory_from_file_upload(
    file_path=Path("my_trees.csv")
)

# Wait for processing
tree_inventory = tree_inventory.wait_until_completed()
```

Your CSV file must include these columns:
- TREE_ID (Integer): Unique identifier for each tree
- SPCD (Integer): FIA species code
- STATUSCD (Integer): Tree status (1: Live, 2: Dead, etc.)
- DIA (Float): Diameter in cm
- HT (Float): Height in meters
- CR (Float): Crown ratio (0-1)
- X (Float): X coordinate
- Y (Float): Y coordinate

## How to Modify Tree Attributes

To adjust tree measurements based on conditions:

```python
# Reduce height of all trees over 20m by 10%
tree_inventory = inventories.create_tree_inventory_from_treemap(
    modifications={
        "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
        "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
    }
)
```

To remove trees from roads and water bodies:

```python
tree_inventory = inventories.create_tree_inventory_from_treemap(
    feature_masks=["road", "water"]
)
```

## How to Apply Forest Management Treatments

To thin to a target basal area:

```python
# Thin to 25 m²/ha basal area
tree_inventory = inventories.create_tree_inventory_from_treemap(
    treatments={
        "method": "proportionalThinning",
        "targetMetric": "basalArea",
        "targetValue": 25.0
    }
)
```

To remove trees below a diameter threshold:

```python
# Remove trees under 30cm diameter
tree_inventory = inventories.create_tree_inventory_from_treemap(
    treatments={
        "method": "directionalThinning",
        "direction": "below",
        "targetMetric": "diameter",
        "targetValue": 30.0
    }
)
```

## How to Export Inventory Data

To save your inventory data to a file:

```python
# Create export in desired format
export = tree_inventory.create_export("csv")  # or "parquet" or "geojson"
export = export.wait_until_completed()

# Download to specific file
export.to_file("trees.csv")

# Or download to directory (uses default filename)
export.to_file(Path("output_directory"))
```

## How to Manage Existing Inventories

To check if inventories exist:

```python
inventories = inventories.get()
if inventories.tree:
    print("Tree inventory exists")
```

To delete an inventory:

```python
if inventories.tree:
    inventories.tree.delete()
```

## Common Workflows

### Complete Processing Pipeline

If you need to create an inventory with multiple modifications:

```python
# Create inventory with multiple settings
tree_inventory = inventories.create_tree_inventory_from_treemap(
    seed=42,
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

# Wait for processing and export
tree_inventory = tree_inventory.wait_until_completed()
export = tree_inventory.create_export("csv")
export = export.wait_until_completed()
export.to_file("processed_trees.csv")
```

### Converting Your Data to FastFuels Format

To process your own tree measurements and apply treatments:

```python
# Upload your data
tree_inventory = inventories.create_tree_inventory_from_file_upload(
    file_path=Path("field_measurements.csv")
)

# Wait for processing
tree_inventory = tree_inventory.wait_until_completed()

# Apply treatments and export
tree_inventory = inventories.create_tree_inventory_from_treemap(
    treatments={
        "method": "proportionalThinning",
        "targetMetric": "basalArea",
        "targetValue": 25.0
    }
)
tree_inventory = tree_inventory.wait_until_completed()

# Export results
export = tree_inventory.create_export("csv")
export = export.wait_until_completed()
export.to_file("processed_measurements.csv")
```
