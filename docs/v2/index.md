# FastFuels Python SDK

!!! note "v2 SDK"
    You are reading the documentation for the **v2 SDK**, which targets
    the FastFuels v2 API. The v1 SDK remains the default — switch
    versions with the selector in the header. Import v2 explicitly from
    `fastfuels_sdk.v2`.

The FastFuels Python SDK is the Python interface to the FastFuels API. Use it
to create domains, grids, tree inventories, features, and point clouds; to
read their data into NumPy, pandas, GeoPandas, and xarray; and to export
files for fire behavior models such as QUIC-Fire and FlamMap.

This site covers working with FastFuels from Python. The
[FastFuels documentation](https://docs.fastfuels.silvxlabs.com) covers the
platform itself — the web application, the HTTP API, and explanations of the
core concepts. Start with
[Introduction](https://docs.fastfuels.silvxlabs.com/v2/api/explanation/introduction/)
for an overview.

## Installation

Install the SDK with `pip`:

```bash
pip install fastfuels-sdk
```

## Authentication

The SDK reads your API key from the `FASTFUELS_API_KEY` environment variable:

```bash
export FASTFUELS_API_KEY="your-api-key"
```

To set the key in code instead, call `set_api_key` before any other call:

```python
import fastfuels_sdk.v2 as ff

ff.set_api_key("your-api-key")
```

The SDK authenticates with an existing API key. Create, rotate, and revoke
keys in the FastFuels console.

## Using the v2 SDK

The v1 and v2 APIs are separate live services, and the SDK ships both as
versioned subpackages, so you can use them side by side during migration:

```python
from fastfuels_sdk.v1 import Domain   # v1 (current default)
from fastfuels_sdk.v2 import Domain   # v2
```

Coming from v1? Start with [Migrating from v1](guides/migration.md).

## How these docs are organized

- **[Tutorial](tutorials/export_to_quicfire.md)** — build a complete set of
  QUIC-Fire inputs from scratch, end to end.
- **How-to guides** — task-focused instructions for each resource:
  [domains](guides/domains.md), [features](guides/features.md),
  [creating](guides/creating-grids.md),
  [composing](guides/composing-grids.md), and
  [working with](guides/working-with-grids.md) grids,
  [tree inventories](guides/inventories.md),
  [modifications and treatments](guides/modify-treat-inventories.md),
  [point clouds](guides/point-clouds.md), [exports](guides/exports.md), and
  [quotas](guides/quotas.md).
- **[Reference](reference.md)** — every public function, class, and
  exception, generated from the source.
