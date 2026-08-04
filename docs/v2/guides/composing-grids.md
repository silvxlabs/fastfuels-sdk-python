# How to Compose Grids

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

Use grid composition to copy and calculate bands from completed grids on the
same two-dimensional lattice. For creating the source grids, see
[Creating grids](creating-grids.md); for alignment options, see
[Align grids to each other](creating-grids.md#align-grids-to-each-other).

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable
- One or more completed 2D grids in the same domain, with the same CRS,
  transform, and shape
- For the example below, a completed FBFM40 grid assigned to `fbfm40`

## Select and calculate output bands

Give each input grid an alias. Use that alias when referring to its bands in
select and compute operations:

```python
import fastfuels_sdk.v2 as ff

fuel_grid = ff.grids.create_fuel_grid_from_fbfm40_lookup(
    fbfm40,
    bands=["fuel_load.1hr", "fuel_depth"],
)
fuel_grid.wait()

composed = ff.grids.create_grid_from_compose(
    {"fuels": fuel_grid},
    select=[
        ff.compose.select("fuel_depth", "fuels.fuel_depth"),
    ],
    compute=[
        ff.compose.compute(
            "fuel_load.1hr",
            "multiply",
            ["fuels.fuel_load.1hr", 0.5],
            conditions=[
                ff.compose.condition("fuels.fuel_load.1hr", "gt", 0),
            ],
            else_=ff.compose.literal(0, unit="kg/m**2"),
        ),
    ],
)
composed.wait()
```

The alias mapping can contain more than one grid. Every band reference uses
the form `alias.band_key`; output names must be unique across the `select` and
`compute` lists.

The arithmetic operators are `add`, `subtract`, `multiply`, `divide`, `min`,
`max`, and `average`. Conditions are ANDed together and require an `else_`
fallback. A fallback may be another band, a number, a typed literal, a fuel
model label, or an `ff.compose.inline_compute(...)` result.

The API derives output units from compute operands. Pass `unit=` to
`ff.compose.compute` only to request a dimensionally compatible output unit.
