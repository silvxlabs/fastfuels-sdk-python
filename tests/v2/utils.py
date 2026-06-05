"""
tests/v2/utils.py
"""

import json
from tests import TEST_DATA_DIR
from fastfuels_sdk.v2.domains import Domain


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
        pad_to_resolution=2.0,
    )

    return domain
