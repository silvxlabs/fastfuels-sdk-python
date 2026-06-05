"""
tests/v2/conftest.py

Session-scoped resources shared across the v2 test modules.

These fixtures are READ-ONLY by convention: they are shared by every
module in the session, so any test that mutates or deletes a resource
must create its own throwaway instead. Expensive job resources (the
completed OSM road feature; later, grids and inventories) are built once
per session and torn down with the domain — deleting the domain cascades
to everything created inside it.
"""

from datetime import datetime, timedelta, timezone

import pytest

from fastfuels_sdk.v2.domains import list_domains
from fastfuels_sdk.v2.features import Feature
from tests.v2.utils import (
    SWEEP_TAG,
    create_default_domain,
    create_default_layerset_geojson,
)

# Leaked resources older than this are fair game for the sweeper. The
# age gate keeps the sweeper from deleting the live resources of another
# run happening at the same time (e.g. local + CI).
SWEEP_AGE = timedelta(hours=2)


@pytest.fixture(scope="session")
def _swept_leftover_domains():
    """Delete test domains leaked by crashed or interrupted runs.

    Teardown never runs when a session is killed mid-flight, so tagged
    test domains can accumulate on the live account. Sweep anything
    carrying the test fingerprint tag that is older than SWEEP_AGE.
    """
    cutoff = datetime.now(timezone.utc) - SWEEP_AGE
    for domain in list_domains(size=100):
        tags = domain.tags if isinstance(domain.tags, list) else []
        created_on = domain.created_on
        if (
            SWEEP_TAG in tags
            and isinstance(created_on, datetime)
            and created_on < cutoff
        ):
            domain.delete()


@pytest.fixture(scope="session")
def test_domain(_swept_leftover_domains):
    """The session-wide test domain. READ-ONLY: shared by every module."""
    domain = create_default_domain()
    yield domain
    # Cleanup: deleting the domain also deletes its features
    domain.delete()


@pytest.fixture(scope="session")
def road_feature(test_domain):
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
    """A layerset feature (synchronous upload). READ-ONLY: shared by every module."""
    return Feature.create_layerset(
        test_domain.id,
        create_default_layerset_geojson(),
        name="test_layerset",
        description="Layerset feature for testing v2 feature operations",
        tags=["layerset-test"],
    )
