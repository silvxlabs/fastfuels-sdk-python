"""
tests/v2/test_modifications.py

Unit tests for the inventory modification builders and the ``feature_masks``
expansion (no API). The grid `mask` builder is exercised in
tests/v2/test_grids.py.
"""

# Core imports
from types import SimpleNamespace

# Internal imports
from fastfuels_sdk.v2 import features
from fastfuels_sdk.v2.grids import Grid
from fastfuels_sdk.v2.inventories import Inventory
from fastfuels_sdk.v2.modifications import (
    _grid_feature_masks,
    _inventory_feature_masks,
    modify_trees,
    remove_trees,
    tree_attribute,
    tree_within,
)
from fastfuels_sdk.v2.client_library.models import (
    FeatureType,
    GridSource,
    InventoryAttribute,
    InventoryFeatureSpatialCondition,
    InventoryModification,
    InventoryModificationAction,
    InventoryModificationCondition,
    JobStatus,
    Modifier,
    Operator,
    RemoveAction,
    SpatialOperator,
)

# External imports
import pytest


class TestTreeAttribute:
    def test_symbolic_operator(self):
        condition = tree_attribute("dbh", "<", 10)
        assert isinstance(condition, InventoryModificationCondition)
        assert condition.attribute == InventoryAttribute.DBH
        assert condition.operator == Operator.LT
        assert condition.value == 10

    def test_enum_name_operator(self):
        assert tree_attribute("height", "ge", 2).operator == Operator.GE

    def test_operator_member_passes_through(self):
        assert tree_attribute("dbh", Operator.NE, 0).operator is Operator.NE

    def test_invalid_operator_raises(self):
        with pytest.raises(ValueError):
            tree_attribute("dbh", "~", 1)

    def test_unknown_attribute_passes_through(self):
        """The API validates it, so an attribute added later can still be sent."""
        condition = tree_attribute("girth", "<", 1)
        assert condition.attribute.name == "UNKNOWN"
        assert condition.to_dict()["attribute"] == "girth"

    def test_crown_base_height_attribute(self):
        condition = tree_attribute("crown_base_height", ">", 2)
        assert condition.attribute == InventoryAttribute.CROWN_BASE_HEIGHT

    def test_crown_ratio_is_not_a_known_attribute(self):
        assert tree_attribute("crown_ratio", "<", 0.5).attribute.name == "UNKNOWN"


class TestTreeWithin:
    def test_builds_feature_condition(self):
        condition = tree_within("feat123", buffer_m=5)
        assert isinstance(condition, InventoryFeatureSpatialCondition)
        assert condition.source == "feature"
        assert condition.feature_id == "feat123"
        assert condition.operator == SpatialOperator.WITHIN
        assert condition.buffer_m == 5

    def test_accepts_feature_object(self):
        assert tree_within(SimpleNamespace(id="f1")).feature_id == "f1"

    def test_operator(self):
        assert tree_within("f", operator="outside").operator == SpatialOperator.OUTSIDE


class TestRemoveTrees:
    def test_builds_modification(self):
        modification = remove_trees(tree_attribute("dbh", "<", 10))
        assert isinstance(modification, InventoryModification)
        assert len(modification.conditions) == 1
        assert len(modification.actions) == 1
        assert isinstance(modification.actions[0], RemoveAction)

    def test_requires_at_least_one_condition(self):
        with pytest.raises(ValueError, match="condition"):
            remove_trees()

    def test_multiple_conditions_anded(self):
        modification = remove_trees(tree_attribute("dbh", "<", 10), tree_within("f"))
        assert len(modification.conditions) == 2


class TestModifyTrees:
    def test_builds_action(self):
        modification = modify_trees(
            "height", "multiply", 0.9, tree_attribute("dbh", ">", 0)
        )
        action = modification.actions[0]
        assert isinstance(action, InventoryModificationAction)
        assert action.attribute == InventoryAttribute.HEIGHT
        assert action.modifier == Modifier.MULTIPLY
        assert action.value == 0.9
        assert len(modification.conditions) == 1

    def test_requires_at_least_one_condition(self):
        with pytest.raises(ValueError, match="condition"):
            modify_trees("height", "multiply", 0.9)

    def test_remove_is_not_a_known_modifier(self):
        # "remove" is RemoveAction, not a modifier value; the API rejects it.
        modification = modify_trees(
            "height", "remove", 0, tree_attribute("dbh", ">", 0)
        )
        assert modification.actions[0].modifier.name == "UNKNOWN"


def _feature(feature_id, feature_type):
    return SimpleNamespace(id=feature_id, type_=FeatureType(feature_type))


class TestGridFeatureMasks:
    def test_fuel_model_codes_by_feature_type(self):
        # Water becomes NB8 (98); roads and buildings become NB1 (91)
        rules = _grid_feature_masks(
            [_feature("r", "road"), _feature("w", "water"), _feature("b", "building")],
            ["fbfm"],
            "domain-id",
        )
        payloads = [rule.to_dict() for rule in rules]
        assert [p["conditions"] for p in payloads] == [
            [{"source": "feature", "operator": "within", "feature_id": fid}]
            for fid in ("r", "w", "b")
        ]
        assert [p["actions"] for p in payloads] == [
            [{"band": "fbfm", "modifier": "replace", "value": value}]
            for value in (91, 98, 91)
        ]

    def test_fbfm13_band(self):
        (rule,) = _grid_feature_masks(_feature("w", "water"), ["fbfm13"], "d")
        assert rule.to_dict()["actions"][0] == {
            "band": "fbfm13",
            "modifier": "replace",
            "value": 98,
        }

    def test_fuel_and_canopy_bands_zeroed(self):
        bands = ["fccs", "fuel_load.1hr", "fuel_depth", "duff_depth", "savr.1hr"]
        bands += ["cbd", "cbh", "cc", "chm"]
        (rule,) = _grid_feature_masks(_feature("r", "road"), bands, "d")
        actions = rule.to_dict()["actions"]
        assert [a["band"] for a in actions] == bands
        assert {a["value"] for a in actions} == {0}

    def test_moisture_and_curing_left_alone(self):
        bands = ["fuel_load.1hr", "fuel_moisture.1hr", "curing"]
        (rule,) = _grid_feature_masks(_feature("r", "road"), bands, "d")
        assert [a["band"] for a in rule.to_dict()["actions"]] == ["fuel_load.1hr"]

    def test_accepts_enum_bands(self):
        (rule,) = _grid_feature_masks(
            _feature("r", "road"), [SimpleNamespace(value="cbd")], "d"
        )
        assert rule.to_dict()["actions"][0]["band"] == "cbd"

    def test_no_fuel_band_raises(self):
        with pytest.raises(ValueError, match="none of them holds fuel"):
            _grid_feature_masks(_feature("r", "road"), ["fuel_moisture.1hr"], "d")

    def test_empty_list_is_no_rules(self):
        assert _grid_feature_masks([], ["fuel_moisture.1hr"], "d") == []

    def test_bare_id_on_fuel_model_band_fetches_type(self, monkeypatch):
        fetched = []

        def fake_get_feature(domain_id, feature_id):
            fetched.append((domain_id, feature_id))
            return _feature(feature_id, "water")

        monkeypatch.setattr(features, "get_feature", fake_get_feature)
        (rule,) = _grid_feature_masks("feat-1", ["fbfm"], "domain-id")
        assert fetched == [("domain-id", "feat-1")]
        assert rule.to_dict()["actions"][0]["value"] == 98

    def test_bare_id_without_fuel_model_band_skips_fetch(self, monkeypatch):
        def fail(*args, **kwargs):
            raise AssertionError("get_feature should not be called")

        monkeypatch.setattr(features, "get_feature", fail)
        (rule,) = _grid_feature_masks("feat-1", ["fuel_load.1hr"], "d")
        assert rule.to_dict()["conditions"][0]["feature_id"] == "feat-1"


class TestInventoryFeatureMasks:
    def test_one_remove_rule_per_feature(self):
        rules = _inventory_feature_masks([_feature("r", "road"), "w"])
        assert [r.conditions[0].feature_id for r in rules] == ["r", "w"]
        assert all(isinstance(r.actions[0], RemoveAction) for r in rules)
        assert all(r.conditions[0].operator == SpatialOperator.WITHIN for r in rules)

    def test_single_feature(self):
        (rule,) = _inventory_feature_masks(_feature("r", "road"))
        assert rule.conditions[0].feature_id == "r"


class TestApplyFeatureMasks:
    def test_grid_masks_its_own_bands(self, monkeypatch):
        grid = Grid(
            id="g",
            domain_id="d",
            status=JobStatus.COMPLETED,
            source=GridSource(),
            bands=[SimpleNamespace(key="fbfm")],
        )
        captured = []
        monkeypatch.setattr(
            Grid, "apply_modifications", lambda self, rules: captured.extend(rules)
        )
        grid.apply_feature_masks([_feature("w", "water")])
        assert captured[0].to_dict()["actions"] == [
            {"band": "fbfm", "modifier": "replace", "value": 98}
        ]

    def test_grid_requires_completed(self):
        grid = Grid(
            id="g",
            domain_id="d",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        with pytest.raises(ValueError, match="apply feature masks"):
            grid.apply_feature_masks([_feature("r", "road")])

    def test_inventory_removes_trees(self):
        captured = []
        inventory = SimpleNamespace(
            apply_modifications=captured.extend,
            _require_completed=lambda action: None,
        )
        Inventory.apply_feature_masks(inventory, [_feature("r", "road")])
        assert isinstance(captured[0].actions[0], RemoveAction)
