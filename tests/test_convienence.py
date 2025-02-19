"""
tests/test_convienence.py
"""

# Core imports
from __future__ import annotations
from pathlib import Path

# Internal imports
from fastfuels_sdk import export_roi_to_quicfire

# External imports
import geopandas as gpd

TEST_DIR = Path(__file__).parent
TEST_DATA_DIR = TEST_DIR / "data"
TEST_TMP_DIR = TEST_DIR / "tmp"


def test_blue_mountain():
    # Load the Blue Mountain ROI
    blue_mountain = gpd.read_file(TEST_DATA_DIR / "blue_mtn.geojson")

    # Export the Blue Mountain ROI to QUIC-Fire
    export = export_roi_to_quicfire(blue_mountain, export_path=TEST_TMP_DIR)

    # Check that the export was successful
    assert export.status == "completed"

    # Check that the export file exists
    assert (TEST_TMP_DIR / "quicfire.zip").exists()
