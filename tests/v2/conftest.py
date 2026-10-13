"""
tests/v2/conftest.py

Session-scoped resources shared across the v2 test modules.

These fixtures are READ-ONLY by convention: they are shared by every
module in the session, so any test that mutates or deletes a resource
must create its own throwaway instead. Expensive job resources (the
completed OSM road feature and the completed topography grid) are built
once per session and torn down with the domain — deleting the domain
cascades to everything created inside it.

Fixtures that wait on a job carry a ``completed_`` prefix; resources
that are born complete (layerset uploads) don't need one.

Every request sends the skip-dispatch header by default, so a create
stores the resource but starts no worker job and it stays pending. Tests
that only check what a create returns need nothing more. Tests that wait
on a job or read its results request the ``real_dispatch`` fixture, and
fixtures that build completed resources create them inside
``real_dispatch_client()``.
"""

import pytest

from fastfuels_sdk.v2.features import (
    create_crown_feature_from_chm,
    create_layerset_feature_from_geojson,
    create_road_feature_from_osm,
)
from fastfuels_sdk.v2.grids import (
    create_canopy_height_grid_from_meta,
    create_fuel_model_grid_from_landfire_fbfm13,
    create_fuel_model_grid_from_landfire_fbfm40,
    create_fuel_model_grid_from_landfire_fccs,
    create_pim_grid_from_treemap,
    create_topography_grid_from_3dep,
)
from fastfuels_sdk.v2.inventories import (
    create_tree_inventory_from_chm_grid,
    create_tree_inventory_from_pim_grid,
)
from tests.v2.utils import (
    create_default_domain,
    create_default_layerset_geojson,
    install_skip_dispatch_client,
    real_dispatch_client,
    sweep_leftover_domains,
)


@pytest.fixture(scope="session", autouse=True)
def skip_dispatch_by_default():
    """Send the skip-dispatch header on every request unless a test or
    fixture opts into real dispatch.
    """
    install_skip_dispatch_client()


@pytest.fixture
def real_dispatch():
    """Send this test's requests without the skip-dispatch header, so its
    creates start real worker jobs. Request it in tests that wait on a job
    or read its results.
    """
    with real_dispatch_client():
        yield


@pytest.fixture(scope="session")
def test_domain():
    """The session-wide test domain. READ-ONLY: shared by every module."""
    sweep_leftover_domains()
    domain = create_default_domain()
    yield domain
    # Cleanup: force-delete cascades to the domain's features and grids
    domain.delete(force=True)


@pytest.fixture(scope="session")
def completed_road_feature(test_domain):
    """A completed OSM road feature. READ-ONLY: shared by every module."""
    with real_dispatch_client():
        feature = create_road_feature_from_osm(
            test_domain,
            name="test_road",
            description="Road feature for testing v2 feature operations",
            tags=["test"],
        )
        feature.wait()
    return feature


@pytest.fixture(scope="session")
def layerset_feature(test_domain):
    """A layerset feature (born completed). READ-ONLY: shared by every module."""
    return create_layerset_feature_from_geojson(
        test_domain,
        create_default_layerset_geojson(),
        name="test_layerset",
        description="Layerset feature for testing v2 feature operations",
        tags=["layerset-test"],
    )


@pytest.fixture(scope="session")
def completed_topography_grid(test_domain):
    """A completed 3DEP topography grid. READ-ONLY: shared by every module."""
    with real_dispatch_client():
        grid = create_topography_grid_from_3dep(
            test_domain,
            output_resolution_m=10,
            name="test_topography",
            description="Topography grid for testing v2 grid operations",
            tags=["test"],
        )
        grid.wait()
    return grid


@pytest.fixture(scope="session")
def completed_fbfm40_grid(test_domain):
    """A completed LANDFIRE FBFM40 fuel model grid. READ-ONLY: shared by
    every module. Provides the FBFM40 codes that
    ``create_fuel_grid_from_fbfm40_lookup`` reads.
    """
    with real_dispatch_client():
        grid = create_fuel_model_grid_from_landfire_fbfm40(
            test_domain,
            output_resolution_m=30,
            name="test_fbfm40",
            description="FBFM40 grid for testing v2 grid lookup operations",
            tags=["test"],
        )
        grid.wait()
    return grid


@pytest.fixture(scope="session")
def completed_fbfm13_grid(test_domain):
    """A completed LANDFIRE FBFM13 fuel model grid. READ-ONLY."""
    with real_dispatch_client():
        grid = create_fuel_model_grid_from_landfire_fbfm13(
            test_domain,
            version="2024",
            remove_non_burnable=["NB1", "NB2"],
            output_resolution_m=30,
            name="test_fbfm13",
            description="FBFM13 grid for testing v2 grid lookup operations",
            tags=["test"],
        )
        grid.wait()
    return grid


@pytest.fixture(scope="session")
def completed_fccs_grid(test_domain):
    """A completed LANDFIRE FCCS fuelbed grid. READ-ONLY."""
    with real_dispatch_client():
        grid = create_fuel_model_grid_from_landfire_fccs(
            test_domain,
            remove_bare_ground=True,
            output_resolution_m=30,
            name="test_fccs",
            description="FCCS grid for testing v2 grid lookup operations",
            tags=["test"],
        )
        grid.wait()
    return grid


@pytest.fixture(scope="session")
def completed_pim_grid(test_domain):
    """A completed TreeMap PIM grid. READ-ONLY: shared by every module."""
    with real_dispatch_client():
        grid = create_pim_grid_from_treemap(
            test_domain,
            output_resolution_m=30,
            resampling="nearest",
            name="test_pim",
            description="PIM grid for testing v2 inventory operations",
            tags=["test"],
        )
        grid.wait()
    return grid


@pytest.fixture(scope="session")
def completed_tree_inventory(test_domain, completed_pim_grid):
    """A completed PIM-expanded tree inventory. READ-ONLY: shared by every
    module. Tests that mutate (update, apply_modifications) work on a
    duplicate or a throwaway instead.
    """
    with real_dispatch_client():
        inventory = create_tree_inventory_from_pim_grid(
            test_domain,
            completed_pim_grid,
            seed=42,
            name="test_inventory",
            description="Tree inventory for testing v2 inventory operations",
            tags=["test"],
        )
        inventory.wait()
    return inventory


@pytest.fixture(scope="session")
def completed_fine_chm_grid(test_domain):
    """A completed Meta CHM at 1 m, fine enough for crown segmentation
    (2 m or finer). READ-ONLY: shared by every module.
    """
    with real_dispatch_client():
        grid = create_canopy_height_grid_from_meta(
            test_domain,
            output_resolution_m=1,
            name="test_fine_chm",
            description="1 m CHM for testing v2 crown features",
            tags=["test"],
        )
        grid.wait()
    return grid


@pytest.fixture(scope="session")
def completed_chm_inventory(test_domain, completed_fine_chm_grid):
    """A completed tree inventory detected from ``completed_fine_chm_grid``.
    READ-ONLY: shared by every module.
    """
    with real_dispatch_client():
        inventory = create_tree_inventory_from_chm_grid(
            test_domain,
            completed_fine_chm_grid,
            name="test_chm_inventory",
            description="CHM-detected inventory for testing v2 crown features",
            tags=["test"],
        )
        inventory.wait()
    return inventory


@pytest.fixture(scope="session")
def completed_crown_feature(
    test_domain, completed_chm_inventory, completed_fine_chm_grid
):
    """A completed crown feature built from ``completed_chm_inventory`` and
    ``completed_fine_chm_grid``. READ-ONLY: shared by every module.
    """
    with real_dispatch_client():
        feature = create_crown_feature_from_chm(
            test_domain,
            completed_chm_inventory,
            completed_fine_chm_grid,
            name="test_crowns",
            description="Crown feature for testing v2 measured crowns",
            tags=["test"],
        )
        feature.wait()
    return feature
