"""
tests/v2/utils.py
"""

import json
from datetime import datetime, timedelta, timezone

from tests import TEST_DATA_DIR
from fastfuels_sdk.v2.domains import Domain, list_domains

# Fingerprint tag for test-created domains, so the session-start sweep
# can find resources leaked by crashed runs
SWEEP_TAG = "sdk-test"

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
