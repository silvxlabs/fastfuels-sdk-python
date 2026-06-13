# How to Modify and Treat Tree Inventories

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

Two tools reshape a tree inventory's stems:

- **Modifications** — general rules that filter trees by *conditions* and
  apply *actions* (remove, multiply, replace, …) to the matching rows.
- **Treatments** — silvicultural thinning prescriptions that remove stems
  until the stand reaches a target basal area or diameter.

Both can be applied two ways: at **creation**, via a creator's
`modifications=` / `treatments=` argument, or to an inventory you already
**hold**, via `apply_modifications` / `apply_treatments`. This guide covers
both. For creating and reading inventories in the first place, see
[Inventories](inventories.md).

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- An [inventory](inventories.md) (held or being created)

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

# Shrink crowns on the largest trees inside a stand boundary
ff.modify_trees(
    "crown_ratio", "multiply", 0.8,
    ff.tree_attribute("dbh", ">", 40),
    ff.tree_within(stand),
)
```

`tree_attribute` takes an attribute (`"dbh"`, `"height"`, `"crown_ratio"`,
`"fia_species_code"`) and a comparison (`"<"`, `"<="`, `">"`, `">="`, `"=="`,
`"!="`); pass several conditions to AND them. `modify_trees`'s modifier is
`"replace"`, `"add"`, `"subtract"`, `"multiply"`, or `"divide"`.

## Treatments

A treatment thins to a target. Build one with `ff.basal_area_treatment`
(residual basal area) or `ff.diameter_treatment` (diameter limit) rather than
hand-building the model:

```python
import fastfuels_sdk.v2 as ff

# Thin from below to a residual basal area of 25 m**2/ha
treatment = ff.basal_area_treatment("from_below", 25.0)

# Or remove every stem under 10 cm dbh
treatment = ff.diameter_treatment("from_below", 10.0)
```

`method` is `"from_below"` (smallest first), `"from_above"` (largest first),
or — for basal area only — `"proportional"` (across all size classes).

## Apply at creation

Every `create_tree_inventory_from_*` function accepts `modifications=` and
`treatments=`; modifications run first, then treatments, while the inventory is
derived:

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
the submitted rules are appended to the inventory's cumulative `modifications`
/ `treatments` list, its ID is kept, and the data is re-derived as a background
job — the inventory returns to `"pending"`, so `wait()` before using it again.

```python
inventory.apply_treatments([ff.basal_area_treatment("from_below", 25.0)])
inventory.wait()

inventory.apply_modifications([ff.remove_trees(ff.tree_attribute("dbh", "<", 10))])
inventory.wait()
```

Both must be called on a `completed` inventory. Re-deriving overwrites the
inventory's data, so to keep the original, [duplicate](#branch-a-scenario) it
first and reshape the copy.

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

The `checksum` is a version marker for an inventory's content: it changes each
time the data is rebuilt and is unaffected by metadata-only edits, so an
identical checksum means identical trees.

## Next steps

- Create and read inventories — see [Inventories](inventories.md)
- Voxelize a reshaped inventory into a 3D fuel grid — see
  [Inventories](inventories.md#voxelize-into-a-3d-fuel-grid)
- Full signatures — see the [Reference](../reference.md)
