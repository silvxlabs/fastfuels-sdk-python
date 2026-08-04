"""
tests/v2/test_treatments.py

Unit tests for the inventory treatment builders (no API).
"""

# Internal imports
from fastfuels_sdk.v2.treatments import basal_area_treatment, diameter_treatment
from fastfuels_sdk.v2.client_library.models import (
    InventoryBasalAreaTreatment,
    InventoryDiameterTreatment,
    InventoryDiameterTreatmentMethod,
    InventoryTreatmentMethod,
)
from fastfuels_sdk.v2.client_library.types import UNSET

# External imports
import pytest


class TestBasalAreaTreatment:
    def test_builds_model(self):
        t = basal_area_treatment("from_below", 25.0)
        assert isinstance(t, InventoryBasalAreaTreatment)
        assert t.method == InventoryTreatmentMethod.FROM_BELOW
        assert t.value == 25.0
        assert t.metric == "basal_area"
        assert t.unit is UNSET
        assert t.conditions is UNSET

    def test_method_enum_passes_through(self):
        t = basal_area_treatment(InventoryTreatmentMethod.PROPORTIONAL, 0.5)
        assert t.method is InventoryTreatmentMethod.PROPORTIONAL

    def test_unit_and_conditions_pass_through(self):
        sentinel = object()
        t = basal_area_treatment(
            "from_below", 25.0, unit="m**2/ha", conditions=[sentinel]
        )
        assert t.unit == "m**2/ha"
        assert t.conditions == [sentinel]

    def test_invalid_method_raises(self):
        with pytest.raises(ValueError):
            basal_area_treatment("sideways", 25.0)


class TestDiameterTreatment:
    def test_builds_model(self):
        t = diameter_treatment("from_below", 10.0)
        assert isinstance(t, InventoryDiameterTreatment)
        assert t.method == InventoryDiameterTreatmentMethod.FROM_BELOW
        assert t.value == 10.0
        assert t.metric == "diameter"

    def test_proportional_not_valid_for_diameter(self):
        # Diameter treatments support only from_below / from_above.
        with pytest.raises(ValueError):
            diameter_treatment("proportional", 10.0)
