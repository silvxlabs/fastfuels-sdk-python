"""
FastFuels SDK.

The top-level namespace re-exports the default API version (currently v1),
loading it on first access. Import from a versioned subpackage to pin an API
version explicitly:

    from fastfuels_sdk.v1 import Domain   # explicit v1
    from fastfuels_sdk import Domain      # default (v1 until 2.0.0)
"""

import importlib


def _v1():
    return importlib.import_module("fastfuels_sdk.v1")


# PEP 562: resolve v1's public names (and __all__, for star-imports) on first
# access, so `import fastfuels_sdk.v2` doesn't load v1.
def __getattr__(name):
    if name == "v1":
        return _v1()
    # Private names and the v2 subpackage must not load v1: the import system
    # probes for them (e.g. `from fastfuels_sdk import v2`).
    if name == "v2" or (name.startswith("_") and name != "__all__"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    v1 = _v1()
    if name == "__all__":
        return v1.__all__
    if name in v1.__all__:
        return getattr(v1, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted({*globals(), *_v1().__all__})
