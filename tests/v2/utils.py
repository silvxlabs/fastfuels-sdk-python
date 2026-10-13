"""
tests/v2/utils.py
"""

import json
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

from tests import TEST_DATA_DIR
from fastfuels_sdk.v2 import api
from fastfuels_sdk.v2.domains import Domain, list_domains

# Fingerprint tag for test-created domains, so the session-start sweep
# can find resources leaked by crashed runs
SWEEP_TAG = "sdk-test"

# The API stores a resource created with this header but queues no worker
# job, so it stays pending (silvxlabs/FastFuels-API-v2#680)
SKIP_DISPATCH_HEADER = {"X-FastFuels-Skip-Dispatch": "1"}

# Client without SKIP_DISPATCH_HEADER, set by install_skip_dispatch_client
_real_client = None

# Required fuelbed input columns for layerset features
DEFAULT_LAYERSET_PROPERTIES = {
    "fuel_type": "grass",
    "fuel_loading": 0.5,
    "fuel_height": 0.3,
    "percent_cover": 80.0,
    "distribution": "homogeneous",
}


def create_default_domain() -> Domain:
    """Creates a default v2 Domain resource for testing."""
    # Load test GeoJSON data
    with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
        geojson = json.load(f)

    # Create a domain using the GeoJSON
    domain = Domain.from_geojson(
        geojson,
        name="test_domain",
        description="Domain for testing v2 domain operations",
        tags=[SWEEP_TAG],
        pad_to_resolution=2.0,
    )

    return domain


def sweep_leftover_domains(max_age: timedelta = timedelta(hours=2)) -> None:
    """Delete test domains leaked by crashed or interrupted runs.

    Teardown never runs when a session is killed mid-flight, so test
    domains can accumulate on the live account. Deletes domains carrying
    SWEEP_TAG that are older than ``max_age``; the age gate keeps
    concurrent runs (e.g. local + CI) from sweeping each other's live
    resources.
    """
    cutoff = datetime.now(timezone.utc) - max_age
    for domain in list_domains(size=100):
        if SWEEP_TAG in (domain.tags or []) and domain.created_on < cutoff:
            domain.delete(force=True)


def create_default_layerset_geojson() -> dict:
    """Build a valid layerset FeatureCollection for testing.

    Layersets require a projected CRS, so this uses the EPSG:5070 variant
    of the blue_mtn geometry with the required fuelbed properties on each
    feature.
    """
    with open(TEST_DATA_DIR / "blue_mtn_5070.geojson") as f:
        geojson = json.load(f)
    for feature in geojson["features"]:
        feature["properties"] = dict(DEFAULT_LAYERSET_PROPERTIES)
    return geojson


def install_skip_dispatch_client() -> None:
    """Make the SDK send SKIP_DISPATCH_HEADER on every request by default.

    Swaps the SDK's cached client for one carrying the header and keeps a
    header-free client for ``real_dispatch_client``. Does nothing when no
    API key is configured.
    """
    global _real_client
    api._client = None
    _real_client = api.get_client()
    if _real_client is not None:
        api._client = _real_client.with_headers(SKIP_DISPATCH_HEADER)


@contextmanager
def real_dispatch_client():
    """Send requests without SKIP_DISPATCH_HEADER, so creates start real jobs.

    Use around any create whose resource is waited on or read.
    """
    previous = api._client
    api._client = _real_client
    try:
        yield
    finally:
        api._client = previous
