# FastFuels SDK v2 (Beta)

!!! warning "Beta"
    You are reading the documentation for the **v2 SDK**, which targets
    the FastFuels v2 API and is under active development. The v1 SDK
    remains the default — its documentation lives in the main sections
    of this site. Import v2 explicitly from `fastfuels_sdk.v2`.

The FastFuels v1 and v2 APIs are separate live services, and the SDK
ships an interface to each as versioned subpackages, so you can use them
side by side during migration:

```python
from fastfuels_sdk.v1 import Domain   # v1 (current default)
from fastfuels_sdk.v2 import Domain   # v2 (Beta)
```

Both subpackages read the same `FASTFUELS_API_KEY` environment variable.

The [FastFuels documentation](https://docs.fastfuels.silvxlabs.com)
covers the v2 platform itself: the web application, the HTTP API, and
explanations of the core concepts (domains, grids, inventories,
features). This section covers how to work with it from Python:

- Coming from v1? Start with [Migrating from v1](guides/migration.md).
- How-to guides: [Domains](guides/domains.md) and
  [Features](guides/features.md).
- The [v2 Reference](../v2/reference.md) documents the full
  `fastfuels_sdk.v2` surface.
