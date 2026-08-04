# How to Work with Tree Inventories in FastFuels SDK

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

An inventory is a table of individual trees within a domain — one row per
tree, with its coordinates, species, diameter, height, and crown ratio.
Inventories sit between grids: they are generated *from* a grid (a PIM grid
or a canopy height model) or from your own data, and they are voxelized
*into* the 3D canopy fuel grid that 3D fire models consume. This guide
covers working with inventories from Python; for what inventories *are*,
see the [FastFuels documentation](https://docs.fastfuels.silvxlabs.com).
Coming from the v1 SDK? Start with the
[migration guide](migration.md#inventories).

The v2 surface is functional: you **create** an inventory by calling a
`create_tree_inventory_from_...` function on a domain, and everything you
do with an inventory you already hold is a **method** on it.

```python
import fastfuels_sdk.v2 as ff

inventory = ff.inventories.create_tree_inventory_from_pim_grid(domain, pim)
trees = inventory.wait().to_dataframe()
```

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- An existing [domain](domains.md) — every creator's first argument is a
  `Domain` (or a bare domain id string)

## From TreeMap to trees

The most common workflow generates a tree inventory for anywhere in the
conterminous US: create a [PIM grid](creating-grids.md#3d-tree-fuel-grids-voxelization)
that matches each cell to a TreeMap forest inventory plot, then expand the
matched plots into individual trees. Pass a `seed` to make the expansion
reproducible:

```python
import fastfuels_sdk.v2 as ff

pim = ff.grids.create_pim_grid_from_treemap(
    domain, output_resolution_m=30, resampling="nearest"
)
pim.wait()

inventory = ff.inventories.create_tree_inventory_from_pim_grid(
    domain, pim, seed=42, name="Blue Mountain trees"
)
inventory.wait()
```

Expansion runs as a background job — the returned inventory starts in
`"pending"` status and `wait()` blocks until it is ready. Once completed,
load the trees as a pandas DataFrame:

```python
>>> trees = inventory.to_dataframe()
>>> len(trees)
71619
>>> trees.head()
               x             y  fia_species_code  ...     dbh   height  crown_ratio
0  721167.447037  5.190627e+06               122  ...  10.160   6.7056         0.10
1  721169.886263  5.190628e+06               122  ...  22.606  10.3632         0.80
2  721172.889178  5.190630e+06               122  ...  10.160   6.7056         0.10
3  721167.558322  5.190629e+06               122  ...   8.128   4.5720         0.08
4  721177.067389  5.190639e+06               122  ...   8.128   4.5720         0.08
```

Coordinates are in the domain CRS in meters, `dbh` is in centimeters, and
`height` is in meters; the inventory's `columns` attribute records each
column's type and unit.

## Create an inventory from a canopy height model

To detect individual trees in a completed
[canopy height model grid](creating-grids.md#canopy-grids) instead — useful
where you want trees derived from remotely sensed canopy structure:

```python
chm = ff.grids.create_canopy_height_grid_from_meta(domain, output_resolution_m=1)
chm.wait()

inventory = ff.inventories.create_tree_inventory_from_chm_grid(domain, chm)
inventory.wait()
```

Stem isolation defaults to local maximum filtering with a 2 m minimum
height. To tune the algorithm, pass a `StemIsolationLmf` or
`StemIsolationVwf` (variable window filtering) model as `algorithm=`. A
CHM-derived inventory carries only what the canopy surface reveals — `x`,
`y`, and `height` columns — so it cannot be voxelized directly (voxelization
needs the per-tree measurements a PIM expansion or an upload provides).

## Upload your own tree records

To create an inventory from your own measurements, upload a `.csv`,
`.geojson`, or `.gpkg` file. Coordinates must be in the domain's CRS:

```python
inventory = ff.inventories.create_tree_inventory_from_file(
    domain, "plot_trees.csv", name="Field plot"
)
inventory.wait()
```

The standard column roles are `x`, `y`, `height` (m), `dbh` (cm),
`crown_ratio`, `fia_species_code`, and `fia_status_code`. Columns whose
names already match need no mapping; otherwise map your file's column names
onto the roles:

```python
inventory = ff.inventories.create_tree_inventory_from_file(
    domain,
    "plot_trees.csv",
    columns={"x": "X_UTM", "y": "Y_UTM", "dbh": "DBH_CM", "height": "HT_M"},
)
```

The upload itself is synchronous, but processing the file runs as a
background job — `wait()` before reading data back:

```python
>>> inventory.wait().to_dataframe()
          x          y  height  ...  crown_ratio  fia_species_code  fia_status_code
0  721055.0  5190149.0    12.0  ...         0.40               122                1
1  721065.0  5190159.0     8.5  ...         0.50               122                1
2  721075.0  5190169.0    15.2  ...         0.35               202                1
```

## Impute missing morphology with GDAM

An uploaded inventory may carry only some columns — coordinates and heights,
say, without diameters or species. `create_tree_inventory_from_gdam` fills in
the missing morphology (`dbh`, `crown_ratio`, `fia_species_code`) for a
completed inventory using GDAM allometry, producing a new inventory:

```python
sparse = ff.inventories.create_tree_inventory_from_file(domain, "stems.csv")
sparse.wait()

full = ff.inventories.create_tree_inventory_from_gdam(domain, sparse)
full.wait()
```

Existing values are preserved — only missing cells are imputed. Pass
`impute_columns=["fia_species_code"]` to impute just a subset.

## Wait for an inventory to finish

`wait` polls until the job reaches a terminal status and returns the
inventory (so calls chain). By default it waits indefinitely; pass
`timeout` (seconds) to bound the wait, which raises `TimeoutError` if
exceeded. A failed job raises `JobFailedError`. To join several jobs at
once, use `ff.wait_all`:

```python
ff.wait_all([pim, inventory], verbose=True)
```

```text
Inventory 7b02df6f583a418da3ec9929037d876d: completed (5s)
```

## Access the tree records

For most workflows, `to_dataframe()` (shown above) is all you need — it
retrieves every partition and assembles one DataFrame. Pass `columns=` to
retrieve a subset.

The records are served in fixed-size partitions; to control retrieval
partition by partition (useful for large inventories), read the partition
layout first:

```python
>>> metadata = inventory.get_data_metadata()
>>> metadata.total_rows
71619
>>> metadata.num_partitions
4
>>> partition = inventory.get_data_partition(0)
>>> partition.num_rows
34831
```

Data is only available once the inventory is `"completed"` — earlier calls
raise `UnprocessableEntityException`.

## Inspect stand-level forestry metrics

Once a tree inventory completes, read its server-computed forestry metrics
without downloading the tree records:

```python
metrics = inventory.forestry_metrics

tree_count = metrics.tree_count
basal_area_per_acre = metrics.basal_area_per_area
trees_per_acre = metrics.tree_density
quadratic_mean_diameter_inches = metrics.quadratic_mean_diameter

dominant_groups = [
    (group.spgrpcd, group.name, group.basal_area_share)
    for group in metrics.dominant_species_groups
]
```

`dominant_species_groups` is ordered by decreasing basal-area share and
contains the leading FIA species groups. Only the leading groups are returned,
so their shares may sum to less than one. `forestry_metrics` is `None` when
metrics are unavailable, including before processing completes.

## Reshape the trees

Every creator accepts `modifications=` (rules that filter trees by conditions
and act on them) and `treatments=` (silvicultural thinning to a target), and
you can reshape an inventory you already hold with `apply_modifications` /
`apply_treatments`. See
[Modify and treat tree inventories](modify-treat-inventories.md) for the full
workflow.

## Duplicate an inventory

`duplicate` makes an independent copy under a new ID, byte-copying the finished
data rather than re-deriving it, so the copy starts identical to the source:

```python
>>> copy = inventory.duplicate(name="Scenario A")
>>> copy.wait()
>>> copy.checksum == inventory.checksum
True
```

The `checksum` is a version marker for an inventory's content: it changes each
time the data is rebuilt and is unaffected by metadata-only edits, so an
identical checksum means identical trees. Duplicate before reshaping to keep
the original untouched (see
[Branch a scenario](modify-treat-inventories.md#branch-a-scenario)).

## Voxelize into a 3D fuel grid

A completed PIM-expanded or uploaded inventory voxelizes into the
[3D tree fuel grid](creating-grids.md#3d-tree-fuel-grids-voxelization) —
per-voxel canopy bulk density on a 3D lattice:

```python
voxels = inventory.voxelize(
    horizontal_resolution_m=2.0, vertical_resolution_m=1.0
)
voxels.wait()
```

```python
>>> [b.key for b in voxels.bands]
['bulk_density.foliage.live']
>>> voxels.georeference.crs
'EPSG:32611'
>>> voxels.georeference.shape   # [layers, rows, cols]
[37, 703, 863]
```

By default each tree's foliage biomass is distributed with the Purves
crown profile model using NSVB allometry. Request more bands with
`bands=` (e.g. `"bulk_density.branchwood.live"`, `"fuel_moisture.dead"`,
`"spcd"`, `"tree_id"`), switch the crown shape with
`crown_profile_model="beta"`, and pass a `seed` for reproducibility.
Because the result is a 3D product, it supports neither resampling nor
grid modifications — modify the trees on the inventory instead, before
voxelizing.

## Export an inventory

To export the tree records to a downloadable file and save it, call
`export` with a format — `"parquet"` (zipped, default), `"csv"`,
`"geojson"`, or `"geopackage"` — and chain the export job's `wait` into
`to_file`:

```python
export = inventory.export(format="csv")
export.wait().to_file("trees.csv")
```

Pass `columns=` to export a column subset. For managing exports, see the
[Exports guide](exports.md).

## Retrieve an existing inventory

To fetch an inventory using its domain and inventory IDs:

```python
inventory = ff.get_inventory(domain, "7b02df6f583a418da3ec9929037d876d")
```

## Refresh and update

To reload an inventory's latest state from the API in place:

```python
inventory.refresh()
print(inventory.status)
```

To modify an inventory's name, description, or tags:

```python
inventory.update(name="New Name", tags=["thinned"])
```

Both update the inventory in place and return it. `update` sends only the
fields you pass; passing none makes no API call.

## List inventories

To list inventories in a domain:

```python
inventories = ff.list_inventories(domain)
```

To list inventories across all your domains, omit the domain:

```python
all_inventories = ff.list_inventories()
```

Narrow the results with filters:

```python
pim_inventories = ff.list_inventories(domain, source="pim")
tagged = ff.list_inventories(domain, tag="thinned")
```

## Delete an inventory

To permanently delete an inventory and its tree records:

```python
inventory.delete()
```

Deleting a domain also deletes all of its inventories.

## Error handling

Wrapper functions and methods raise typed exceptions from
`fastfuels_sdk.v2.exceptions`:

```python
import fastfuels_sdk.v2 as ff
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

try:
    inventory = ff.get_inventory(domain, "does-not-exist")
except NotFoundException:
    print("No such inventory (or you don't have access to it)")

try:
    trees = running_inventory.to_dataframe()
except UnprocessableEntityException as exc:
    print(exc.detail)
    # inventories/a6840e0c7cd64de896954d95afc6aea0 status is 'running',
    # expected 'completed'.
```

Deriving from an inventory that is not completed raises a `ValueError`
before any API call:

```python
>>> pending_inventory.voxelize(horizontal_resolution_m=2.0, vertical_resolution_m=1.0)
ValueError: Cannot voxelize an inventory with status 'pending'. Call .wait() until it completes first.
```

## Next steps

- Voxelize alongside aligned 2D grids — see
  [Creating grids](creating-grids.md)
- Wait on, inspect, and manage the voxelized grid — see
  [Working with grids](working-with-grids.md)
- Full signatures — see the [Reference](../reference.md)
