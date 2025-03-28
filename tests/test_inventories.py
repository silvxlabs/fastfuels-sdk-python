"""
tests/test_inventories.py
"""

# Core imports
from __future__ import annotations
import tempfile
from pathlib import Path

# Internal imports
from tests.utils import create_default_domain, normalize_datetime
from fastfuels_sdk.inventories import Inventories, TreeInventory
from fastfuels_sdk.client_library.exceptions import NotFoundException, ApiException
from fastfuels_sdk.client_library import (
    TreeInventorySource,
    Export,
)

# External imports
import pytest
import numpy as np
import pandas as pd


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
    inventories = Inventories.from_domain_id(test_domain.id)

    # Return the inventory for use in tests
    yield inventories
    # Cleanup: Handled by the test_domain fixture


@pytest.fixture(scope="module")
def test_domain_with_tree_inventory(test_domain, test_inventories):
    """Fixture that creates a test domain with a tree inventory to be used by the tests"""
    test_inventories.create_tree_inventory(sources="TreeMap")

    # Return the domain for use in tests
    yield test_domain
    # Cleanup: Handled by the test_domain fixture


@pytest.fixture(scope="module")
def test_tree_inventory(test_domain_with_tree_inventory):
    """Fixture that creates a test tree inventory to be used by the tests"""
    tree_inventory = TreeInventory.from_domain_id(test_domain_with_tree_inventory.id)

    # Return the tree inventory for use in tests
    yield tree_inventory
    # Cleanup: Handled by the test_domain fixture


@pytest.fixture(scope="module")
def test_tree_inventory_completed(test_tree_inventory):
    test_tree_inventory.wait_until_completed(in_place=True)

    yield test_tree_inventory
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
        inventories = Inventories.from_domain_id(test_domain.id)
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
            Inventories.from_domain_id(bad_test_domain.id)


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

    @pytest.mark.parametrize(
        "source",
        [
            "TreeMap",
            ["TreeMap"],
            TreeInventorySource.TREEMAP,
            [TreeInventorySource.TREEMAP],
        ],
        ids=["str", "str-list", "enum", "enum-list"],
    )
    def test_create_with_different_source_types(self, test_inventories, source):
        """Tests basic creation with just a source"""
        tree_inventory = test_inventories.create_tree_inventory(sources=source)

        self.assert_data_validity(tree_inventory, test_inventories.domain_id)
        # Convert the sources to their string values for comparison
        actual_sources = [
            src.actual_instance.value if hasattr(src, "actual_instance") else src
            for src in tree_inventory.sources
        ]
        expected_sources = [source] if not isinstance(source, list) else source
        expected_sources = [
            s.value if hasattr(s, "value") else s for s in expected_sources
        ]
        assert actual_sources == expected_sources
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
        response_treatment = tree_inventory.treatments[0].to_dict()
        assert response_treatment == treatment
        assert response_treatment is not treatment

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

        for treatment, response_treatment in zip(treatments, tree_inventory.treatments):
            assert response_treatment.to_dict() == treatment
            assert response_treatment.to_dict() is not treatment

    # def test_feature_masks_single(self, test_inventories):
    #     """Tests single feature mask"""
    #     tree_inventory = test_inventories.create_tree_inventory(
    #         sources="TreeMap", feature_masks="road"
    #     )
    #
    #     self.assert_data_validity(tree_inventory, test_inventories.domain_id)
    #     assert tree_inventory.feature_masks == ["road"]
    #
    # def test_feature_masks_multiple(self, test_inventories):
    #     """Tests multiple feature masks"""
    #     tree_inventory = test_inventories.create_tree_inventory(
    #         sources="TreeMap", feature_masks=["road", "water"]
    #     )
    #
    #     self.assert_data_validity(tree_inventory, test_inventories.domain_id)
    #     assert tree_inventory.feature_masks == ["road", "water"]
    #     assert len(tree_inventory.feature_masks) == 2
    #
    # def test_combined_options(self, test_inventories):
    #     """Tests combining all options together"""
    #     tree_inventory = test_inventories.create_tree_inventory(
    #         sources="TreeMap",
    #         tree_map={"version": "2014", "seed": 42},
    #         modifications={
    #             "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
    #             "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}],
    #         },
    #         treatments={
    #             "method": "proportionalThinning",
    #             "targetMetric": "basalArea",
    #             "targetValue": 25.0,
    #         },
    #         feature_masks=["road", "water"],
    #     )
    #
    #     self.assert_data_validity(tree_inventory, test_inventories.domain_id)
    #     assert tree_inventory.tree_map.version == "2014"
    #     assert tree_inventory.tree_map.seed == 42
    #     assert len(tree_inventory.modifications) == 1
    #     assert len(tree_inventory.treatments) == 1
    #     assert len(tree_inventory.feature_masks) == 2

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
        # Convert the sources to their string values for comparison
        actual_sources = [
            src.actual_instance.value if hasattr(src, "actual_instance") else src
            for src in tree_inventory.sources
        ]
        assert actual_sources == ["TreeMap"]
        assert tree_inventory.tree_map is not None
        assert tree_inventory.tree_map.version == version
        assert (
            isinstance(tree_inventory.tree_map.seed, int)
            and tree_inventory.tree_map.seed > 0
        )

    def test_defaults(self, test_domain, test_inventories):
        """Test basic creation without in_place"""
        tree_inventory = test_inventories.create_tree_inventory_from_treemap()
        self.assert_data_validity(tree_inventory, test_domain.id, "2016")

        # Check if the tree inventory is successfully added to the inventories
        updated_inventory = test_inventories.get()
        assert updated_inventory.tree is not None
        assert isinstance(updated_inventory.tree, TreeInventory)

        # Normalize datetime fields before comparison
        normalized_updated = normalize_datetime(updated_inventory.tree)
        normalized_tree = normalize_datetime(tree_inventory)

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
        normalized_updated = normalize_datetime(updated_inventory.tree)
        normalized_tree = normalize_datetime(tree_inventory)

        assert normalized_updated == normalized_tree

    @pytest.mark.parametrize("chm_source", ["Meta2024", None])
    def test_canopy_height_map_source(self, test_domain, test_inventories, chm_source):
        """Test creating a tree inventory from TreeMap using a specific CHM source"""
        tree_inventory = test_inventories.create_tree_inventory_from_treemap(
            canopy_height_map_source=chm_source
        )

        # Verify the inventory was created correctly
        self.assert_data_validity(tree_inventory, test_domain.id, "2016")
        if chm_source:
            assert tree_inventory.tree_map.canopy_height_map_configuration is not None
            assert (
                tree_inventory.tree_map.canopy_height_map_configuration.actual_instance.source
                == chm_source
            )
        else:
            assert tree_inventory.tree_map.canopy_height_map_configuration is None

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
        normalized_stored = normalize_datetime(test_inventories.tree)
        normalized_returned = normalize_datetime(tree_inventory)
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

    def test_invalid_chm_source(self, test_domain, test_inventories):
        """Test creation with invalid chm source"""
        with pytest.raises(ValueError):
            test_inventories.create_tree_inventory_from_treemap(
                canopy_height_map_source="invalid_source"
            )


class TestCreateTreeInventoryFromFileUpload:
    @pytest.fixture
    def valid_tree_data(self):
        """Fixture to create valid tree inventory data"""
        num_trees = int(1e4)
        data = {
            "TREE_ID": np.arange(num_trees, dtype=np.int64),
            "SPCD": np.random.randint(1, 100, num_trees),
            "STATUSCD": np.random.randint(0, 4, num_trees),
            "DIA": np.random.uniform(0, 1200, num_trees),
            "HT": np.random.uniform(0, 116, num_trees),
            "CR": np.random.uniform(0, 1, num_trees),
            "X": np.random.uniform(721064.0, 721514.0, num_trees),
            "Y": np.random.uniform(5190012.0, 5190284.0, num_trees),
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def temp_csv_file(self, valid_tree_data):
        """Fixture to create a temporary CSV file with valid data"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            valid_tree_data.to_csv(tmp.name, index=False)
            return Path(tmp.name)

    def test_valid_upload(self, test_inventories, temp_csv_file):
        """Test successful upload of valid tree inventory data"""
        tree_inventory = test_inventories.create_tree_inventory_from_file_upload(
            temp_csv_file
        )

        assert tree_inventory is not None
        assert tree_inventory.status == "pending"
        assert tree_inventory.domain_id == test_inventories.domain_id
        assert tree_inventory.sources == ["file"]

        tree_inventory.wait_until_completed()

        # Verify the inventory was created correctly
        assert tree_inventory.status == "completed"

    def test_file_not_found(self, test_inventories):
        """Test handling of non-existent file"""
        with pytest.raises(FileNotFoundError):
            test_inventories.create_tree_inventory_from_file_upload("nonexistent.csv")

    def test_invalid_file_type(self, test_inventories, tmp_path):
        """Test handling of non-CSV file"""
        invalid_file = tmp_path / "test.txt"
        invalid_file.write_text("some content")

        with pytest.raises(ValueError, match="File must be a CSV"):
            test_inventories.create_tree_inventory_from_file_upload(invalid_file)

    # TODO: Consider adding local checks to create_tree_inventory_from_file_upload for this. Otherwise, we will rely on API tests
    # def test_file_too_large(self, test_inventories, valid_tree_data):
    #     """Test handling of file exceeding size limit"""
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
    #         # Create large dataset by repeating the data
    #         repetitions = int(1e3)
    #         large_df = pd.concat([valid_tree_data] * repetitions, ignore_index=True)
    #         large_df.to_csv(tmp.name, index=False)
    #
    #         with pytest.raises(ValueError, match="File size exceeds 500MB limit"):
    #             test_inventories.create_tree_inventory_from_file_upload(tmp.name)
    #
    # def test_missing_column(self, test_inventories, valid_tree_data):
    #     """Test handling of CSV with missing required column"""
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
    #         # Drop a required column
    #         invalid_data = valid_tree_data.drop("TREE_ID", axis=1)
    #         invalid_data.to_csv(tmp.name, index=False)
    #
    #         with pytest.raises(ApiException):
    #             test_inventories.create_tree_inventory_from_file_upload(tmp.name)
    #
    # def test_invalid_column_name(self, test_inventories, valid_tree_data):
    #     """Test handling of CSV with invalid column name"""
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
    #         # Rename a column to invalid name
    #         invalid_data = valid_tree_data.rename(columns={"TREE_ID": "BAD_SCHEMA"})
    #         invalid_data.to_csv(tmp.name, index=False)
    #
    #         with pytest.raises(ApiException):
    #             test_inventories.create_tree_inventory_from_file_upload(tmp.name)
    #
    # def test_invalid_data_type(self, test_inventories, valid_tree_data):
    #     """Test handling of CSV with invalid data type"""
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
    #         # Change SPCD to invalid type (float instead of int)
    #         invalid_data = valid_tree_data.copy()
    #         invalid_data["SPCD"] = np.random.uniform(0, 1, len(invalid_data))
    #         invalid_data.to_csv(tmp.name, index=False)
    #
    #         with pytest.raises(ApiException):
    #             test_inventories.create_tree_inventory_from_file_upload(tmp.name)
    #
    # def test_out_of_bounds_tree(self, test_inventories, valid_tree_data):
    #     """Test handling of CSV with tree locations out of bounds"""
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
    #         # Put trees out of bounds
    #         invalid_data = valid_tree_data.copy()
    #         invalid_data["X"] = invalid_data["X"] * 10
    #         invalid_data.to_csv(tmp.name, index=False)
    #
    #         with pytest.raises(ApiException):
    #             test_inventories.create_tree_inventory_from_file_upload(tmp.name)

    def teardown_method(self, method):
        """Clean up any temporary files after each test"""
        # Clean up any files created during the test
        for tmp_file in Path().glob("*.csv"):
            if tmp_file.is_file():
                tmp_file.unlink()


class TestTreeInventoryFromDomain:
    def test_valid_domain(self, test_domain_with_tree_inventory):
        """Test creation of TreeInventory from a valid domain"""
        tree_inventory = TreeInventory.from_domain_id(
            test_domain_with_tree_inventory.id
        )
        assert tree_inventory is not None
        assert isinstance(tree_inventory, TreeInventory)
        assert tree_inventory.domain_id == test_domain_with_tree_inventory.id

    def test_invalid_domain(self, test_domain):
        """Test creation of TreeInventory from an invalid domain"""
        bad_test_domain = test_domain.model_copy(deep=True)
        bad_test_domain.id = "bad_id"
        with pytest.raises(NotFoundException):
            TreeInventory.from_domain_id(bad_test_domain.id)


class TestGetTreeInventory:
    def test_default(self, test_tree_inventory):
        """Tests fetching the tree inventory"""
        tree_inventory = test_tree_inventory.get()
        assert tree_inventory is not None
        assert isinstance(tree_inventory, TreeInventory)
        assert tree_inventory is not test_tree_inventory
        assert tree_inventory == test_tree_inventory

    def test_in_place(self, test_tree_inventory):
        """Tests fetching the tree inventory in place"""
        test_tree_inventory.get(in_place=True)
        assert test_tree_inventory is not None
        assert isinstance(test_tree_inventory, TreeInventory)

    def test_in_place_with_assignment(self, test_tree_inventory):
        """Tests fetching the tree inventory in place with assignment"""
        new_tree_inventory = test_tree_inventory.get(in_place=True)
        assert new_tree_inventory is test_tree_inventory
        assert new_tree_inventory == test_tree_inventory


class TestCreateTreeInventoryExport:
    @pytest.mark.parametrize("export_format", ["csv", "parquet", "geojson"])
    def test_create_incomplete_tree_inventory(self, test_tree_inventory, export_format):
        """
        Tests the creation of an export for an incomplete tree inventory. This should raise an
        ApiException since the tree inventory has not been completed yet.
        """
        with pytest.raises(ApiException):
            test_tree_inventory.create_export(export_format=export_format)

    @pytest.mark.parametrize("export_format", ["csv", "parquet", "geojson"])
    def test_create(self, test_tree_inventory_completed, export_format):
        export = test_tree_inventory_completed.create_export(
            export_format=export_format
        )
        assert export is not None
        assert isinstance(export, Export)
        assert export.domain_id == test_tree_inventory_completed.domain_id
        assert export.resource == "inventories"
        assert export.sub_resource == "tree"
        assert export.attribute is None
        assert export.format == export_format
        assert export.status == "pending"
        assert export.created_on is not None
        assert export.modified_on is not None
        assert export.expires_on is not None
        assert export.signed_url is None

    def test_create_invalid_format(self, test_tree_inventory_completed):
        with pytest.raises(ApiException):
            test_tree_inventory_completed.create_export(export_format="invalid_format")


class TestDeleteTreeInventory:

    def test_delete_existing_inventory(self, test_inventories, test_tree_inventory):
        """Tests deleting an existing tree inventory"""
        test_tree_inventory.delete()

        # Verify the inventory was deleted
        with pytest.raises(NotFoundException, match="Reason: Not Found"):
            test_tree_inventory.get()

        test_inventories.get(in_place=True)
        assert test_inventories.tree is None
