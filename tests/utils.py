"""
tests/utils.py
"""

import json
from tests import TEST_DATA_DIR
from fastfuels_sdk.domains import Domain


def create_default_domain() -> Domain:
    # Load test GeoJSON data
    with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
        geojson = json.load(f)

    # Create a domain using the GeoJSON
    domain = Domain.from_geojson(
        geojson,
        name="test_domain",
        description="Domain for testing domain operations",
        horizontal_resolution=1.0,
        vertical_resolution=1.0,
    )

    return domain
