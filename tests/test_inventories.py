"""
tests/test_inventories.py
"""

# Internal imports
from tests.utils import create_default_domain
from fastfuels_sdk.inventories import Inventories, TreeInventory
from fastfuels_sdk.client_library.exceptions import NotFoundException
from fastfuels_sdk.client_library import TreeInventoryModification

# External imports
import pytest


@pytest.fixture(scope="module")
def test_domain():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


@pytest.fixture(scope="module")
def test_inventories(test_domain):
    """Fixture that creates a test inventories object to be used by the tests"""
    inventories = Inventories.from_domain(test_domain)

    # Return the inventory for use in tests
    yield inventories
    # Cleanup: Handled by the test_domain fixture


class TestInventoriesFromId:
    def test_success(self, test_domain):
        """
        Tests whether inventories are successfully created and initialized from the given domain.

        The function verifies the successful creation of an `Inventories` object based on the
        provided domain identifier. It asserts that the resulting object is not `None`, its type
        matches the expected `Inventories` class, and it correctly initializes with the domain's
        ID and a `None` tree attribute.
        """
        inventories = Inventories.from_domain(test_domain)
        assert inventories is not None
        assert isinstance(inventories, Inventories)
        assert inventories.domain_id == test_domain.id
        assert inventories.tree is None

    def test_bad_domain_id(self, test_domain):
        """
        This function tests handling of a domain object with an invalid ID. It creates a copy of the provided
        test domain with its `id` attribute modified to an invalid value. When attempting to retrieve
        inventories based on this modified test domain, it expects a `NotFoundException` to be raised.
        """
        bad_test_domain = test_domain.model_copy(deep=True)
        bad_test_domain.id = "bad_id"
        with pytest.raises(NotFoundException):
            Inventories.from_domain(bad_test_domain)


class TestGetInventories:
    def test_default(self, test_inventories):
        """
        Tests whether inventories are successfully fetched and updated using assignment.
        """
        new_inventories = test_inventories.get()
        assert new_inventories is not None
        assert isinstance(new_inventories, Inventories)
        assert new_inventories is not test_inventories
        assert new_inventories.domain_id == test_inventories.domain_id
        assert new_inventories.tree == test_inventories.tree

    def test_in_place(self, test_inventories):
        """
        Tests whether inventories are successfully fetched and updated in place.
        """
        test_inventories.get(in_place=True)
        assert test_inventories is not None
        assert isinstance(test_inventories, Inventories)

    def test_in_place_with_assignment(self, test_inventories):
        """
        Tests whether inventories are successfully fetched and updated in place with assignment.
        """
        new_inventories = test_inventories.get(in_place=True)
        assert new_inventories is test_inventories
        assert new_inventories.domain_id == test_inventories.domain_id
        assert new_inventories.tree == test_inventories.tree


class TestCreateTreeInventory:
    @staticmethod
    def assert_data_validity(tree_inventory, domain_id):
        """Validates the basic tree inventory data"""
        assert tree_inventory is not None
        assert isinstance(tree_inventory, TreeInventory)
        assert tree_inventory.domain_id == domain_id
        assert tree_inventory.status == "pending"
        assert (
            isinstance(tree_inventory.checksum, str)
            and len(tree_inventory.checksum) > 0
        )

    @pytest.mark.parametrize("source", ["TreeMap"])
    def test_defaults(self, test_inventories, source):
        """Tests basic creation with just a source"""
        tree_inventory = test_inventories.create_tree_inventory(sources=source)

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert tree_inventory.sources == [source]
        assert tree_inventory.treatments == []
        assert tree_inventory.modifications == []
        assert tree_inventory.feature_masks == []

    def test_invalid_source(self, test_inventories):
        """Tests error handling for invalid source"""
        with pytest.raises(ValueError):
            test_inventories.create_tree_inventory(sources="invalid_source")

    def test_treemap_configuration(self, test_inventories):
        """Tests TreeMap source configuration"""
        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", tree_map={"version": "2014", "seed": 42}
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert tree_inventory.tree_map.version == "2014"
        assert tree_inventory.tree_map.seed == 42

    @staticmethod
    def validate_modifications(tree_inventory, modifications):
        for i, modification in enumerate(modifications):
            mod = tree_inventory.modifications[i].to_dict()
            assert len(mod["conditions"]) == len(modification["conditions"])
            assert len(mod["actions"]) == len(modification["actions"])
            for condition, mod_condition in zip(
                modification["conditions"], mod["conditions"]
            ):
                assert condition["attribute"] == mod_condition["attribute"]
                assert condition["operator"] == mod_condition["operator"]
                assert condition["value"] == mod_condition["value"]

            for action, mod_action in zip(modification["actions"], mod["actions"]):
                assert action["attribute"] == mod_action["attribute"]
                assert action["modifier"] == mod_action["modifier"]
                if action["modifier"] != "remove":
                    assert action["value"] == mod_action["value"]
                else:
                    assert "value" not in mod_action

    def test_modifications_single(self, test_inventories):
        """Tests single modification"""
        modification = {
            "conditions": [{"attribute": "HT", "operator": "gt", "value": 20}],
            "actions": [{"attribute": "HT", "modifier": "multiply", "value": 0.9}],
        }

        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", modifications=modification
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert len(tree_inventory.modifications) == 1

        # Validate the modification
        self.validate_modifications(tree_inventory, [modification])

    def test_modifications_multiple(self, test_inventories):
        """Tests multiple modifications"""
        modifications = [
            {
                "conditions": [{"attribute": "HT", "operator": "gt", "value": 20}],
                "actions": [{"attribute": "HT", "modifier": "multiply", "value": 0.9}],
            },
            {
                "conditions": [{"attribute": "DIA", "operator": "lt", "value": 10}],
                "actions": [{"attribute": "all", "modifier": "remove"}],
            },
        ]

        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", modifications=modifications
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert len(tree_inventory.modifications) == 2
        self.validate_modifications(tree_inventory, modifications)

    def test_treatments_single(self, test_inventories):
        """Tests single treatment"""
        treatment = {
            "method": "proportionalThinning",
            "targetMetric": "basalArea",
            "targetValue": 25.0,
        }

        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", treatments=treatment
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert len(tree_inventory.treatments) == 1
        treat = tree_inventory.treatments[0]
        assert treat.method == "proportionalThinning"
        assert treat.target_metric == "basalArea"
        assert treat.target_value == 25.0

    def test_treatments_multiple(self, test_inventories):
        """Tests multiple treatments"""
        treatments = [
            {
                "method": "proportionalThinning",
                "targetMetric": "basalArea",
                "targetValue": 25.0,
            },
            {
                "method": "directionalThinning",
                "direction": "below",
                "targetMetric": "diameter",
                "targetValue": 30.0,
            },
        ]

        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", treatments=treatments
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert len(tree_inventory.treatments) == 2

    def test_feature_masks_single(self, test_inventories):
        """Tests single feature mask"""
        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", feature_masks="road"
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert tree_inventory.feature_masks == ["road"]

    def test_feature_masks_multiple(self, test_inventories):
        """Tests multiple feature masks"""
        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", feature_masks=["road", "water"]
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert tree_inventory.feature_masks == ["road", "water"]
        assert len(tree_inventory.feature_masks) == 2

    def test_combined_options(self, test_inventories):
        """Tests combining all options together"""
        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap",
            tree_map={"version": "2014", "seed": 42},
            modifications={
                "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
                "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}],
            },
            treatments={
                "method": "proportionalThinning",
                "targetMetric": "basalArea",
                "targetValue": 25.0,
            },
            feature_masks=["road", "water"],
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert tree_inventory.tree_map.version == "2014"
        assert tree_inventory.tree_map.seed == 42
        assert len(tree_inventory.modifications) == 1
        assert len(tree_inventory.treatments) == 1
        assert len(tree_inventory.feature_masks) == 2

    def test_in_place_update(self, test_inventories):
        """Tests in_place update behavior"""
        original_tree = test_inventories.tree

        tree_inventory = test_inventories.create_tree_inventory(
            sources="TreeMap", in_place=True
        )

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        assert test_inventories.tree is not None
        assert test_inventories.tree is tree_inventory
        assert test_inventories.tree is not original_tree


class TestCreateTreeInventoryFromTreeMap:
    @staticmethod
    def assert_data_validity(tree_inventory, domain_id, version):
        assert tree_inventory is not None
        assert isinstance(tree_inventory, TreeInventory)
        assert tree_inventory.domain_id == domain_id
        assert tree_inventory.status == "pending"
        assert tree_inventory.treatments == []
        assert tree_inventory.modifications == []
        assert tree_inventory.feature_masks == []
        assert (
            isinstance(tree_inventory.checksum, str)
            and len(tree_inventory.checksum) > 0
        )
        assert tree_inventory.sources == ["TreeMap"]
        assert tree_inventory.tree_map is not None
        assert tree_inventory.tree_map.version == version
        assert (
            isinstance(tree_inventory.tree_map.seed, int)
            and tree_inventory.tree_map.seed > 0
        )

    @staticmethod
    def normalize_datetime(inventory):
        """Normalize datetime fields by ensuring consistent timezone handling"""
        if inventory.created_on and inventory.created_on.tzinfo:
            inventory.created_on = inventory.created_on.replace(tzinfo=None)
        if inventory.modified_on and inventory.modified_on.tzinfo:
            inventory.modified_on = inventory.modified_on.replace(tzinfo=None)
        return inventory

    def test_defaults(self, test_domain, test_inventories):
        """Test basic creation without in_place"""
        tree_inventory = test_inventories.create_tree_inventory_from_treemap()
        self.assert_data_validity(tree_inventory, test_domain.id, "2016")

        # Check if the tree inventory is successfully added to the inventories
        updated_inventory = test_inventories.get()
        assert updated_inventory.tree is not None
        assert isinstance(updated_inventory.tree, TreeInventory)

        # Normalize datetime fields before comparison
        normalized_updated = self.normalize_datetime(updated_inventory.tree)
        normalized_tree = self.normalize_datetime(tree_inventory)

        assert normalized_updated == normalized_tree

    @pytest.mark.parametrize("version", ["2014", "2016"])
    def test_versions(self, test_domain, test_inventories, version):
        """Test basic creation without in_place"""
        tree_inventory = test_inventories.create_tree_inventory_from_treemap(
            version=version
        )
        self.assert_data_validity(tree_inventory, test_domain.id, version)

        # Check if the tree inventory is successfully added to the inventories
        updated_inventory = test_inventories.get()
        assert updated_inventory.tree is not None
        assert isinstance(updated_inventory.tree, TreeInventory)

        # Normalize datetime fields before comparison
        normalized_updated = self.normalize_datetime(updated_inventory.tree)
        normalized_tree = self.normalize_datetime(tree_inventory)

        assert normalized_updated == normalized_tree

    def test_in_place_true(self, test_domain, test_inventories):
        """Test creation with in_place=True"""
        # Store original state
        original_tree = test_inventories.tree

        # Create new inventory with in_place=True
        tree_inventory = test_inventories.create_tree_inventory_from_treemap(
            in_place=True
        )

        # Verify the inventory was created correctly
        self.assert_data_validity(tree_inventory, test_domain.id, "2016")

        # Verify in_place update occurred
        assert test_inventories.tree is not None
        assert test_inventories.tree is tree_inventory
        assert test_inventories.tree is not original_tree

        # Verify the returned inventory matches what's stored
        normalized_stored = self.normalize_datetime(test_inventories.tree)
        normalized_returned = self.normalize_datetime(tree_inventory)
        assert normalized_stored == normalized_returned

    def test_in_place_false(self, test_domain, test_inventories):
        """Test creation with in_place=False (default behavior)"""
        # Store original state
        original_tree = test_inventories.tree

        # Create new inventory with in_place=False
        tree_inventory = test_inventories.create_tree_inventory_from_treemap(
            in_place=False
        )

        # Verify the inventory was created correctly
        self.assert_data_validity(tree_inventory, test_domain.id, "2016")

        # Verify in_place update did not occur
        assert test_inventories.tree is original_tree
        assert test_inventories.tree is not tree_inventory

    def test_with_seed(self, test_domain, test_inventories):
        """Test creation with a specific seed value"""
        seed = 42
        tree_inventory = test_inventories.create_tree_inventory_from_treemap(seed=seed)

        # Verify seed was used
        assert tree_inventory.tree_map.seed == seed

    def test_invalid_version(self, test_domain, test_inventories):
        """Test creation with invalid TreeMap version"""
        with pytest.raises(ValueError):
            test_inventories.create_tree_inventory_from_treemap(
                version="invalid_version"
            )

    def test_invalid_seed(self, test_domain, test_inventories):
        """Test creation with invalid seed value"""
        with pytest.raises(ValueError):
            test_inventories.create_tree_inventory_from_treemap(
                seed="2asfasdsdf123`12"  # noqa
            )
