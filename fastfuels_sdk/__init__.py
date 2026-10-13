"""
FastFuels SDK.

The top-level namespace re-exports the default API version (currently v1),
loading it on first access. Import from a versioned subpackage to pin an API
version explicitly:

    from fastfuels_sdk.v1 import Domain   # explicit v1
    from fastfuels_sdk import Domain      # default (v1 until 2.0.0)
"""

import importlib

# Must equal fastfuels_sdk.v1.__all__ (checked in tests/test_top_level_namespace.py).
__all__ = [
    "Domain",
    "list_domains",
    "Inventories",
    "TreeInventory",
    "Features",
    "RoadFeature",
    "WaterFeature",
    "FeatureDataResponse",
    "Grids",
    "SurfaceGrid",
    "SurfaceGridBuilder",
    "TreeGrid",
    "TreeGridBuilder",
    "TopographyGrid",
    "TopographyGridBuilder",
    "FeatureGrid",
    "Export",
    "export_roi",
    "export_roi_to_quicfire",
    "PointClouds",
    "AlsPointCloud",
]


# PEP 562: keep `import fastfuels_sdk.v2` from loading v1.
def __getattr__(name):
    # Only v1's public names (and the v1 subpackage itself) resolve here, so
    # `from fastfuels_sdk import v2` still falls through to the submodule import.
    if name == "v1":
        return importlib.import_module("fastfuels_sdk.v1")
    if name in __all__:
        value = getattr(importlib.import_module("fastfuels_sdk.v1"), name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted([*globals(), *__all__])
