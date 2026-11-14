"""
tests/v2/test_unknown_enum_values.py

Responses carrying an enum value this SDK version doesn't know (a new feature
type, job status, band type, ...) still parse. The value comes back as an
``UNKNOWN`` member that keeps it, so a new value in the API doesn't break
older SDKs. No API calls.
"""

import pytest

from fastfuels_sdk.v2.client_library.models.feature_type import FeatureType
from fastfuels_sdk.v2.client_library.models.job_status import JobStatus
from fastfuels_sdk.v2.client_library.models.three_dep_resolution import (
    ThreeDepResolution,
)
from fastfuels_sdk.v2.exports import Export
from fastfuels_sdk.v2.features import Feature
from fastfuels_sdk.v2.grids import Grid
from fastfuels_sdk.v2.inventories import Inventory
from fastfuels_sdk.v2.point_clouds import PointCloud

_RESOURCE = {
    "id": "abc123",
    "domain_id": "def456",
    "status": "a_new_status",
    "source": {"product": "a_new_product"},
    "created_on": "2026-01-01T00:00:00",
    "modified_on": "2026-01-01T00:00:00",
    "tags": [],
}


@pytest.mark.parametrize("resource_class", [Feature, Inventory, PointCloud])
def test_unknown_type_and_status_parse(resource_class):
    resource = resource_class.from_dict({**_RESOURCE, "type": "a_new_type"})

    assert resource.type_.name == "UNKNOWN"
    assert resource.type_ == "a_new_type"
    assert resource.status.name == "UNKNOWN"
    assert resource.status == "a_new_status"


def test_unknown_band_type_parses():
    grid = Grid.from_dict(
        {**_RESOURCE, "bands": [{"key": "a_band", "type": "a_new_type", "index": 0}]}
    )

    assert grid.bands[0].type_.name == "UNKNOWN"
    assert grid.bands[0].type_ == "a_new_type"


def test_unknown_export_status_parses():
    assert Export.from_dict(_RESOURCE).status == "a_new_status"


@pytest.mark.parametrize("resource_class", [Feature, Inventory, PointCloud])
def test_unknown_values_round_trip(resource_class):
    """``to_dict`` sends the unknown value back as given."""
    payload = {**_RESOURCE, "type": "a_new_type"}
    as_dict = resource_class.from_dict(payload).to_dict()

    assert as_dict["type"] == "a_new_type"
    assert as_dict["status"] == "a_new_status"


def test_known_values_are_still_members():
    assert FeatureType("road") is FeatureType.ROAD
    assert JobStatus("completed") is JobStatus.COMPLETED


def test_unknown_value_prints_as_the_value():
    assert str(FeatureType("a_new_type")) == "a_new_type"


def test_unknown_int_enum_value_parses():
    resolution = ThreeDepResolution(7)

    assert resolution.name == "UNKNOWN"
    assert resolution == 7


@pytest.mark.parametrize("value", [None, 1, 1.5])
def test_wrong_type_still_raises(value):
    with pytest.raises(ValueError):
        FeatureType(value)
