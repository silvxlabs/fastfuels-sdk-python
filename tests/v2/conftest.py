"""
tests/v2/conftest.py

Session-scoped resources shared across the v2 test modules.

These fixtures are READ-ONLY by convention: they are shared by every
module in the session, so any test that mutates or deletes a resource
must create its own throwaway instead. Expensive job resources are built
once per session and torn down with their domain — deleting the domain
cascades to everything created inside it.

Fixtures that wait on a job carry a ``completed_`` prefix; resources
that are born complete (layerset uploads) don't need one.

Every request sends the skip-dispatch header by default, so a create
stores the resource but starts no worker job and it stays pending. Tests
that only check what a create returns need nothing more. Tests that wait
on a job or read its results request the ``real_dispatch`` fixture, and
fixtures that build completed resources create them inside
``real_dispatch_client()``.

Jobs that take minutes carry a ``dispatched_`` prefix: the fixture
creates the resource without waiting, and ``start_long_jobs`` requests it
at session start so the job runs server-side while the rest of the suite
does. The test that uses it calls ``wait()`` itself.
"""

import pytest

from fastfuels_sdk.v2 import _jobs
from fastfuels_sdk.v2.calibrations import duet_calibration
from fastfuels_sdk.v2.features import (
    create_building_feature_from_overture,
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
    create_surface_fuel_grid_from_duet,
    create_topography_grid_from_3dep,
)
from fastfuels_sdk.v2.inventories import (
    create_tree_inventory_from_chm_grid,
    create_tree_inventory_from_pim_grid,
)
from fastfuels_sdk.v2.domains import Domain
from fastfuels_sdk.v2.exceptions import NotFoundException
from fastfuels_sdk.v2.point_clouds import (
    check_3dep_coverage as check_3dep_point_cloud_coverage,
    create_point_cloud_from_3dep,
)
from tests.v2.utils import (
    create_building_domain,
    create_default_domain,
    create_duet_domain,
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


# Most test jobs finish in a second or two, so the SDK's 5 s poll interval
# would dominate every wait
TEST_POLL_SECONDS = 1


@pytest.fixture(scope="session", autouse=True)
def fast_polling():
    """Poll job status every ``TEST_POLL_SECONDS`` instead of the SDK default."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(_jobs, "_POLL_SECONDS", TEST_POLL_SECONDS)
        yield


# Fixtures for jobs that take minutes, started at session start when a
# collected test requests them
LONG_JOB_FIXTURES = ("dispatched_duet_surface_grid",)


def _uses_long_job(item):
    return any(name in item.fixturenames for name in LONG_JOB_FIXTURES)


def pytest_collection_modifyitems(items):
    """Run the tests that use ``LONG_JOB_FIXTURES`` last, so their jobs
    (dispatched at session start) get the whole suite to finish.
    """
    items[:] = [i for i in items if not _uses_long_job(i)] + [
        i for i in items if _uses_long_job(i)
    ]


@pytest.fixture(scope="session", autouse=True)
def start_long_jobs(request, skip_dispatch_by_default):
    """Dispatch the ``LONG_JOB_FIXTURES`` that this session's tests use
    before any test runs, so their jobs overlap the rest of the suite.
    """
    for name in LONG_JOB_FIXTURES:
        if not any(name in item.fixturenames for item in request.session.items):
            continue
        try:
            request.getfixturevalue(name)
        except Exception:
            # pytest caches the failure and re-raises it in the tests that
            # request the fixture; don't error the whole session here
            pass


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
def building_domain():
    """A session-wide domain over a residential area, for building
    features (the default test domain has no buildings). READ-ONLY.
    """
    domain = create_building_domain()
    yield domain
    domain.delete(force=True)


@pytest.fixture(scope="session")
def completed_building_feature(building_domain):
    """A completed Overture building feature in ``building_domain``.
    READ-ONLY: shared by every module.
    """
    with real_dispatch_client():
        feature = create_building_feature_from_overture(
            building_domain,
            name="test_buildings",
            description="Building feature for testing v2 feature operations",
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
    """A completed 3DEP topography grid at 30 m, on the same lattice as the
    LANDFIRE fixtures. READ-ONLY: shared by every module.
    """
    with real_dispatch_client():
        grid = create_topography_grid_from_3dep(
            test_domain,
            output_resolution_m=30,
            bands=["elevation", "slope", "aspect"],
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


@pytest.fixture(scope="session")
def completed_voxel_grid(completed_tree_inventory):
    """A completed 2 m x 1 m voxelization of ``completed_tree_inventory``
    carrying the bands the DUET, LeafLux, Fosberg, and QUIC-Fire tests
    read. READ-ONLY: shared by every module.
    """
    with real_dispatch_client():
        voxels = completed_tree_inventory.voxelize(
            horizontal_resolution_m=2,
            vertical_resolution_m=1,
            bands=[
                "bulk_density.foliage.live",
                "spcd",
                "fuel_moisture.live",
                "leaf_area_density",
            ],
            name="test_voxels",
            tags=["test"],
        )
        voxels.wait()
    return voxels


@pytest.fixture(scope="session")
def duet_domain():
    """A small session-wide domain for DUET, which rejects source grids
    with more than 600,000 horizontal cells (the default test domain has
    more). READ-ONLY.
    """
    domain = create_duet_domain()
    yield domain
    domain.delete(force=True)


@pytest.fixture(scope="session")
def completed_duet_voxel_grid(duet_domain):
    """A completed 2 m x 1 m voxelization of a PIM-expanded inventory over
    ``duet_domain``, carrying the bands DUET reads. READ-ONLY.
    """
    with real_dispatch_client():
        pim = create_pim_grid_from_treemap(
            duet_domain,
            output_resolution_m=30,
            resampling="nearest",
            name="test_duet_pim",
            tags=["test"],
        )
        pim.wait()
        inventory = create_tree_inventory_from_pim_grid(
            duet_domain, pim, seed=42, name="test_duet_inventory", tags=["test"]
        )
        inventory.wait()
        voxels = inventory.voxelize(
            horizontal_resolution_m=2,
            vertical_resolution_m=1,
            bands=["bulk_density.foliage.live", "spcd", "fuel_moisture.live"],
            name="test_duet_voxels",
            tags=["test"],
        )
        voxels.wait()
    return voxels


@pytest.fixture(scope="session")
def dispatched_duet_surface_grid(completed_duet_voxel_grid):
    """A DUET surface fuel grid over ``completed_duet_voxel_grid``,
    dispatched but not waited on (see ``start_long_jobs``). READ-ONLY.
    """
    with real_dispatch_client():
        surface = create_surface_fuel_grid_from_duet(
            completed_duet_voxel_grid,
            # DUET runtime grows faster than the square of the simulated
            # years; one year is enough to exercise the path
            years_since_burn=1,
            bands=[
                "fuel_load.grass",
                "fuel_load.litter",
                "fuel_depth.grass",
                "fuel_depth.litter",
            ],
            calibration=duet_calibration(
                fuel_load={
                    "grass": {"mean": 0.5, "sd": 0.25},
                    "litter": {"max": 5, "min": 0},
                },
                fuel_depth={
                    "grass": {"value": 0.3},
                    "litter": {"value": 0.06},
                },
            ),
            name="test_duet_surface_fuels",
            tags=["test"],
        )
    yield surface
    try:
        surface.delete()
    except NotFoundException:
        pass


@pytest.fixture(scope="session")
def completed_voxel_topography_grid(completed_voxel_grid):
    """A completed 3DEP topography grid on the horizontal lattice of
    ``completed_voxel_grid``. READ-ONLY: shared by every module.
    """
    with real_dispatch_client():
        grid = create_topography_grid_from_3dep(
            completed_voxel_grid.domain_id,
            align_to=completed_voxel_grid,
            bands=["elevation", "slope", "aspect"],
            name="test_voxel_topography",
            tags=["test"],
        )
        grid.wait()
    return grid


@pytest.fixture(scope="session")
def completed_inventory_csv_export(completed_tree_inventory):
    """A completed CSV export of ``completed_tree_inventory``. READ-ONLY."""
    with real_dispatch_client():
        export = completed_tree_inventory.export(format="csv", tags=["test"])
        export.wait()
    return export


@pytest.fixture(scope="session")
def covered_3dep_domain():
    """A small Bondurant, WY domain with stable 3DEP LiDAR coverage."""
    geojson = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:32612"}},
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [522800, 4720400],
                            [523300, 4720400],
                            [523300, 4720900],
                            [522800, 4720900],
                            [522800, 4720400],
                        ]
                    ],
                },
            }
        ],
    }
    domain = Domain.from_geojson(
        geojson,
        name="test_3dep_point_cloud_domain",
        tags=["sdk-test"],
    )
    yield domain
    domain.delete(force=True)


@pytest.fixture(scope="session")
def completed_3dep_point_cloud(covered_3dep_domain):
    """A completed ALS point cloud from 3DEP over ``covered_3dep_domain``.
    READ-ONLY: shared by every module.
    """
    coverage = check_3dep_point_cloud_coverage(covered_3dep_domain)
    with real_dispatch_client():
        point_cloud = create_point_cloud_from_3dep(
            covered_3dep_domain,
            datasets=[coverage.datasets[0].name],
            name="test_3dep_point_cloud",
            tags=["sdk-test"],
        )
        point_cloud.wait()
    yield point_cloud
    try:
        point_cloud.delete()
    except NotFoundException:
        pass
