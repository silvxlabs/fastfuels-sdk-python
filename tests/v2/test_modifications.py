"""
tests/v2/test_modifications.py

Unit tests for the inventory modification builders (no API). The grid `mask`
builder is exercised in tests/v2/test_grids.py.
"""

# Core imports
from types import SimpleNamespace

# Internal imports
from fastfuels_sdk.v2.modifications import (
    modify_trees,
    remove_trees,
    tree_attribute,
    tree_within,
)
from fastfuels_sdk.v2.client_library.models import (
    InventoryAttribute,
    InventoryFeatureSpatialCondition,
    InventoryModification,
    InventoryModificationAction,
    InventoryModificationCondition,
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

    def test_invalid_attribute_raises(self):
        with pytest.raises(ValueError):
            tree_attribute("girth", "<", 1)


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

    def test_remove_is_not_a_modifier(self):
        # "remove" is RemoveAction, not a modifier value
        with pytest.raises(ValueError):
            modify_trees("height", "remove", 0, tree_attribute("dbh", ">", 0))
