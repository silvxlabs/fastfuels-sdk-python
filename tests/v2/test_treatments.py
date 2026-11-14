"""
tests/v2/test_treatments.py

Unit tests for the inventory treatment builders (no API).
"""

# Internal imports
import fastfuels_sdk.v2 as ff
from fastfuels_sdk.v2.treatments import (
    basal_area_treatment,
    crown_spacing_treatment,
    diameter_treatment,
)
from fastfuels_sdk.v2.client_library.models import (
    ApplyTreatmentsRequest,
    CanopyAllometryMaxCrownRadiusSource,
    CanopyCrownWidthEquations,
    InventoryBasalAreaTreatment,
    InventoryColumnMaxCrownRadiusSource,
    InventoryCrownSpacingRank,
    InventoryCrownSpacingTreatment,
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

    def test_unknown_method_passes_through(self):
        """The API validates it, so a method added later can still be sent."""
        t = basal_area_treatment("sideways", 25.0)
        assert t.method.name == "UNKNOWN"
        assert t.to_dict()["method"] == "sideways"


class TestDiameterTreatment:
    def test_builds_model(self):
        t = diameter_treatment("from_below", 10.0)
        assert isinstance(t, InventoryDiameterTreatment)
        assert t.method == InventoryDiameterTreatmentMethod.FROM_BELOW
        assert t.value == 10.0
        assert t.metric == "diameter"

    def test_proportional_is_not_a_known_diameter_method(self):
        # Diameter treatments support only from_below / from_above; the API
        # rejects proportional.
        assert diameter_treatment("proportional", 10.0).method.name == "UNKNOWN"


class TestCrownSpacingTreatment:
    def test_defaults(self):
        t = crown_spacing_treatment(3.0)
        assert isinstance(t, InventoryCrownSpacingTreatment)
        assert t.metric == "crown_spacing"
        assert t.value == 3.0
        assert t.unit is UNSET
        assert t.rank_by is UNSET
        assert t.max_crown_radius_source is UNSET
        assert t.conditions is UNSET
        # Omitted fields are left to the API defaults (dbh rank, purves radius).
        assert t.to_dict() == {"metric": "crown_spacing", "value": 3.0}

    def test_top_level_export(self):
        assert ff.crown_spacing_treatment is crown_spacing_treatment

    def test_unit_and_conditions_pass_through(self):
        sentinel = object()
        t = crown_spacing_treatment(10.0, unit="ft", conditions=[sentinel])
        assert t.unit == "ft"
        assert t.conditions == [sentinel]

    @pytest.mark.parametrize(
        "rank_by, expected",
        [
            ("dbh", InventoryCrownSpacingRank.DBH),
            ("height", InventoryCrownSpacingRank.HEIGHT),
            (InventoryCrownSpacingRank.HEIGHT, InventoryCrownSpacingRank.HEIGHT),
        ],
    )
    def test_rank_by(self, rank_by, expected):
        t = crown_spacing_treatment(3.0, rank_by=rank_by)
        assert t.rank_by is expected

    def test_radius_column(self):
        t = crown_spacing_treatment(
            3.0, rank_by="height", max_crown_radius_column="crown_radius"
        )
        assert isinstance(
            t.max_crown_radius_source, InventoryColumnMaxCrownRadiusSource
        )
        assert t.max_crown_radius_source.column == "crown_radius"
        assert t.to_dict() == {
            "metric": "crown_spacing",
            "value": 3.0,
            "rank_by": "height",
            "max_crown_radius_source": {
                "type": "inventory_column",
                "column": "crown_radius",
            },
        }

    @pytest.mark.parametrize(
        "equations, expected",
        [
            ("purves", CanopyCrownWidthEquations.PURVES),
            ("crookston_stage", CanopyCrownWidthEquations.CROOKSTON_STAGE),
        ],
    )
    def test_allometry_equations(self, equations, expected):
        t = crown_spacing_treatment(3.0, max_crown_radius_equations=equations)
        source = t.max_crown_radius_source
        assert isinstance(source, CanopyAllometryMaxCrownRadiusSource)
        assert source.equations is expected
        assert t.to_dict()["max_crown_radius_source"] == {
            "type": "allometry",
            "equations": equations,
        }

    def test_unknown_rank_by_passes_through(self):
        """The API validates it, so a ranking added later can still be sent."""
        t = crown_spacing_treatment(3.0, rank_by="crown_radius")
        assert t.to_dict()["rank_by"] == "crown_radius"

    def test_unknown_equations_pass_through(self):
        t = crown_spacing_treatment(3.0, max_crown_radius_equations="new_equations")
        assert t.to_dict()["max_crown_radius_source"]["equations"] == "new_equations"

    def test_equations_and_column_are_exclusive(self):
        with pytest.raises(ValueError, match="at most one"):
            crown_spacing_treatment(
                3.0,
                max_crown_radius_equations="purves",
                max_crown_radius_column="crown_radius",
            )

    def test_round_trips_through_treatment_union(self):
        # A request carrying every treatment kind parses each back to its own
        # model, so an inventory's treatments ledger reads crown spacing.
        body = ApplyTreatmentsRequest(
            treatments=[
                basal_area_treatment("from_below", 25.0),
                diameter_treatment("from_below", 10.0),
                crown_spacing_treatment(
                    3.0, rank_by="height", max_crown_radius_column="crown_radius"
                ),
            ]
        ).to_dict()
        parsed = ApplyTreatmentsRequest.from_dict(body).treatments
        assert [type(t) for t in parsed] == [
            InventoryBasalAreaTreatment,
            InventoryDiameterTreatment,
            InventoryCrownSpacingTreatment,
        ]
        assert parsed[2].rank_by is InventoryCrownSpacingRank.HEIGHT
        assert parsed[2].max_crown_radius_source.column == "crown_radius"
