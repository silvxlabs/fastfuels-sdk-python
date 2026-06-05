"""
tests/v2/conftest.py

Session-scoped resources shared across the v2 test modules.

These fixtures are READ-ONLY by convention: they are shared by every
module in the session, so any test that mutates or deletes a resource
must create its own throwaway instead. Expensive job resources (the
completed OSM road feature; later, grids and inventories) are built once
per session and torn down with the domain — deleting the domain cascades
to everything created inside it.

Fixtures that wait on a job carry a ``completed_`` prefix; resources
that are born complete (layerset uploads) don't need one.
"""

import pytest

from fastfuels_sdk.v2.features import Feature
from tests.v2.utils import (
    create_default_domain,
    create_default_layerset_geojson,
    sweep_leftover_domains,
)


@pytest.fixture(scope="session")
def test_domain():
    """The session-wide test domain. READ-ONLY: shared by every module."""
    sweep_leftover_domains()
    domain = create_default_domain()
    yield domain
    # Cleanup: deleting the domain also deletes its features
    domain.delete()


@pytest.fixture(scope="session")
def completed_road_feature(test_domain):
    """A completed OSM road feature. READ-ONLY: shared by every module."""
    feature = Feature.create_osm_road(
        test_domain.id,
        name="test_road",
        description="Road feature for testing v2 feature operations",
        tags=["test"],
    )
    feature.wait_until_completed(step=2)
    return feature


@pytest.fixture(scope="session")
def layerset_feature(test_domain):
    """A layerset feature (born completed). READ-ONLY: shared by every module."""
    return Feature.create_layerset(
        test_domain.id,
        create_default_layerset_geojson(),
        name="test_layerset",
        description="Layerset feature for testing v2 feature operations",
        tags=["layerset-test"],
    )
