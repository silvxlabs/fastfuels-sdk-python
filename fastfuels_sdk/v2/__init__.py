"""
FastFuels SDK v2.

The settled access pattern is a single import reaching everything through the
package namespace::

    import fastfuels_sdk.v2 as ff

    domain = ff.Domain.from_file("aoi.geojson")
    grid = ff.grids.create_topography_grid_from_3dep(domain, output_resolution_m=10)
    grid.wait()

- Resource creators are module-qualified functions: ``ff.grids.create_*``,
  ``ff.features.create_*``.
- Operations on a resource you hold are methods: ``grid.wait()``,
  ``grid.resample(...)``, ``grid.delete()``.
- Cross-cutting helpers are top-level: ``ff.Domain``, ``ff.get_grid``,
  ``ff.list_grids``, ``ff.wait_all``, ``ff.set_api_key``.
"""

from fastfuels_sdk.v2 import features, grids
from fastfuels_sdk.v2._jobs import JobFailedError, wait_all
from fastfuels_sdk.v2.api import set_api_key
from fastfuels_sdk.v2.domains import Domain, list_domains, reproject_geojson
from fastfuels_sdk.v2.features import Feature, get_feature, list_features
from fastfuels_sdk.v2.grids import Grid, get_grid, list_grids

__all__ = [
    # Submodules (resource creators live here: ff.grids.create_*, ff.features.create_*)
    "features",
    "grids",
    # Configuration
    "set_api_key",
    # Records
    "Domain",
    "Feature",
    "Grid",
    # Fetch / list helpers
    "list_domains",
    "list_features",
    "get_feature",
    "list_grids",
    "get_grid",
    "reproject_geojson",
    # Jobs
    "wait_all",
    "JobFailedError",
]
