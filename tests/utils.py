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


def normalize_datetime(resource):
    """Normalize datetime fields by ensuring consistent timezone handling"""
    if resource.created_on and resource.created_on.tzinfo:
        resource.created_on = resource.created_on.replace(tzinfo=None)
    if resource.modified_on and resource.modified_on.tzinfo:
        resource.modified_on = resource.modified_on.replace(tzinfo=None)
    return resource
