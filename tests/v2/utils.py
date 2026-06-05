"""
tests/v2/utils.py
"""

import json
from tests import TEST_DATA_DIR
from fastfuels_sdk.v2.domains import Domain

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
        pad_to_resolution=2.0,
    )

    return domain


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
