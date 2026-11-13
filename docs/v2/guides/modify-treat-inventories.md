# How to Modify and Treat Tree Inventories

Two tools reshape a tree inventory's stems:

- **Modifications** — general rules that filter trees by *conditions* and
  apply *actions* (remove, multiply, replace, …) to the matching rows.
- **Treatments** — silvicultural thinning prescriptions that remove stems
  until the stand reaches a target basal area, diameter, or crown spacing.

Both can be applied two ways: at **creation**, via a creator's
`modifications=` / `treatments=` argument, or to an inventory you already
**hold**, via `apply_modifications` / `apply_treatments`. This guide covers
both. For creating and reading inventories in the first place, see
[Tree inventories](inventories.md); for what modifications and treatments do
to a stand, see
[Editing the stand](https://docs.fastfuels.silvxlabs.com/v2/api/explanation/inventories/#editing-the-stand-modifications-and-treatments)
in the FastFuels documentation.

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- An [inventory](inventories.md), or the grids to create one

## Modifications

A modification is a rule with two parts: `conditions` (all ANDed — a tree must
satisfy every one) and `actions` (applied to the matching trees). Build
conditions with `ff.tree_attribute` (a per-tree attribute test) or
`ff.tree_within` (trees inside a feature), then assemble the rule with
`ff.remove_trees` (drop the matching trees) or `ff.modify_trees` (change an
attribute on them):

```python
import fastfuels_sdk.v2 as ff

# Remove every tree under 10 cm DBH
ff.remove_trees(ff.tree_attribute("dbh", "<", 10))

# Raise crown bases by 2 m on the largest trees inside a stand boundary
ff.modify_trees(
    "crown_base_height", "add", 2.0,
    ff.tree_attribute("dbh", ">", 40),
    ff.tree_within(stand),
)
```

`tree_attribute` takes an attribute (`"dbh"` in cm, `"height"` and
`"crown_base_height"` in m, `"fia_species_code"`, or `"tree_id"`), a
comparison (`"<"`, `"<="`, `">"`, `">="`, `"=="`, `"!="`), and a value; pass
`unit=` to give the value in another unit. Pass several conditions to AND
them. `modify_trees`'s modifier is
`"replace"`, `"add"`, `"subtract"`, `"multiply"`, or `"divide"`.

## Treatments

A treatment thins to a target. Build one with `ff.basal_area_treatment`
(residual basal area), `ff.diameter_treatment` (diameter limit), or
`ff.crown_spacing_treatment` (minimum crown spacing) rather than
hand-building the model:

```python
import fastfuels_sdk.v2 as ff

# Thin from below to a residual basal area of 25 m**2/ha
treatment = ff.basal_area_treatment("from_below", 25.0)

# Or remove every stem under 10 cm dbh
treatment = ff.diameter_treatment("from_below", 10.0)

# Or leave at least 3 m between crowns
treatment = ff.crown_spacing_treatment(3.0)
```

`method` is `"from_below"` (smallest first), `"from_above"` (largest first),
or — for basal area only — `"proportional"` (across all size classes).

Basal area is in m²/ha and diameter in cm dbh by default; pass `unit=` to
use another unit. The inventory must have every column a treatment reads.
Basal-area and diameter treatments read `dbh`.

## Thin to a crown spacing

To thin a stand until every retained crown is at least a given distance from
its neighbors, crown edge to crown edge, pass the gap in meters to
`ff.crown_spacing_treatment`. By default the larger-diameter tree is kept
when two crowns are too close, and crown radii come from the Purves
allometry:

```python
treatment = ff.crown_spacing_treatment(3.0)
```

To give the gap in another unit, pass `unit=`. To keep the taller tree
instead, pass `rank_by="height"`. To size crowns with the Crookston & Stage
equations, pass `max_crown_radius_equations="crookston_stage"`; to read a
measured radius in meters from an inventory column, pass
`max_crown_radius_column=` instead:

```python
treatment = ff.crown_spacing_treatment(
    10.0,
    unit="ft",
    rank_by="height",
    max_crown_radius_equations="crookston_stage",
)
```

The default treatment reads `dbh`, `height`, `crown_base_height`, and
`fia_species_code`, which a
[TreeMap inventory](inventories.md#from-treemap-to-trees) has.

### Thin a CHM inventory

A [CHM-derived inventory](inventories.md#create-an-inventory-from-a-canopy-height-model)
has no `dbh`, so the only crown spacing treatment that applies to it ranks
trees by height and reads the `crown_radius` column that
`crown_segmentation=` adds:

```python
treatment = ff.crown_spacing_treatment(
    3.0, rank_by="height", max_crown_radius_column="crown_radius"
)

inventory = ff.inventories.create_tree_inventory_from_chm_grid(
    domain, chm, crown_segmentation={}, treatments=[treatment]
)
inventory.wait()
```

To thin a segmented CHM inventory you already hold, pass the same treatment
to [`apply_treatments`](#apply-to-an-inventory-you-hold). Any other treatment
on a CHM inventory raises `UnprocessableEntityException`.

## Apply at creation

`create_tree_inventory_from_pim_grid`, `create_tree_inventory_from_pim_chm_fusion`,
and `create_tree_inventory_from_chm_grid` accept `modifications=` and
`treatments=`; modifications run first, then treatments, while the inventory is
derived. To reshape an uploaded or GDAM-imputed inventory, use the
[`apply_*` methods](#apply-to-an-inventory-you-hold) once it completes.

```python
thinned = ff.inventories.create_tree_inventory_from_pim_grid(
    domain,
    pim,
    seed=42,
    modifications=[ff.remove_trees(ff.tree_attribute("dbh", "<", 10))],
    treatments=[ff.basal_area_treatment("from_below", 25.0)],
    name="Thinned",
)
thinned.wait()
```

## Apply to an inventory you hold

`apply_modifications` and `apply_treatments` reshape an inventory **in place**:
its ID is kept and the data is re-derived as a background job. The submitted
rules are queued while the inventory is `"pending"`, then appended to the
cumulative `modifications` / `treatments` list when processing completes. Call
`wait()` before using the inventory again or reading those ledgers.

```python
inventory.apply_treatments([ff.basal_area_treatment("from_below", 25.0)])
inventory.wait()

inventory.apply_modifications([ff.remove_trees(ff.tree_attribute("dbh", "<", 10))])
inventory.wait()
```

Both must be called on a `completed` inventory. Re-deriving overwrites the
inventory's data, so to keep the original, [duplicate](#branch-a-scenario) it
first and reshape the copy.

## Remove trees inside features

To drop the trees that fall inside roads, water, or building footprints, pass
the completed [features](features.md) in the PIM, PIM–CHM fusion, or CHM
creator's `feature_masks` argument:

```python
roads = ff.features.create_road_feature_from_osm(domain)
water = ff.features.create_water_feature_from_osm(domain)
pim = ff.grids.create_pim_grid_from_treemap(domain, output_resolution_m=30)
ff.wait_all([roads, water, pim])

trees = ff.inventories.create_tree_inventory_from_pim_grid(
    domain, pim, seed=42, feature_masks=[roads, water]
)
trees.wait()
```

The masks are applied after any `modifications` and before any `treatments`.
A feature with no geometry — e.g. OpenStreetMap water in a domain without
any — removes nothing.

To remove them from an inventory you already hold, call
`apply_feature_masks`:

```python
inventory.apply_feature_masks([roads, water])
inventory.wait()
```

To widen a feature — e.g. a small buffer around building footprints to catch
stems at their edges — build the rule with `ff.tree_within` and
`ff.remove_trees` instead:

```python
buildings = ff.features.create_building_feature_from_overture(domain)
chm = ff.grids.create_canopy_height_grid_from_meta(domain, output_resolution_m=1)
ff.wait_all([buildings, chm])

trees = ff.inventories.create_tree_inventory_from_chm_grid(
    domain,
    chm,
    modifications=[ff.remove_trees(ff.tree_within(buildings, buffer_m=2))],
)
trees.wait()
```

## Branch a scenario

To compare scenarios — a thinned stand against the original — keep the
original untouched and work on copies. `duplicate` makes an independent copy
under a new ID, byte-copying the finished data rather than re-deriving it, so
the copy starts identical (same `checksum`):

```python
copy = inventory.duplicate(name="Thinning scenario")
copy.wait()
copy.apply_treatments([ff.basal_area_treatment("from_below", 25.0)])
copy.wait()
```

See [Duplicate an inventory](inventories.md#duplicate-an-inventory) for how
`checksum` tracks an inventory's content.

## Next steps

- Create and read inventories — see [Tree inventories](inventories.md)
- Voxelize a reshaped inventory into a 3D fuel grid — see
  [Voxelize into a 3D fuel grid](inventories.md#voxelize-into-a-3d-fuel-grid)
- Full signatures — see the [Reference](../reference.md)
