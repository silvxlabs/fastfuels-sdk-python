"""
tests/test_exports.py
"""

# Internal imports
from tests import TEST_TMP_DIR
from tests.utils import create_default_domain
from fastfuels_sdk.inventories import Inventories

# External imports
import pytest


class TestTreeInventoryExports:
    """Tests specific to tree inventory exports"""

    @pytest.fixture(scope="class")
    def domain(self):
        """Creates a test domain"""
        domain = create_default_domain()
        yield domain
        domain.delete()

    @pytest.fixture(scope="class")
    def tree_inventory(self, domain):
        """Creates and completes a tree inventory"""
        inventories = Inventories.from_domain_id(domain.id)
        tree_inventory = inventories.create_tree_inventory(sources="TreeMap")
        tree_inventory.wait_until_completed(in_place=True)
        return tree_inventory

    @pytest.fixture(scope="class")
    def tree_inventory_export_csv(self, tree_inventory):
        export = tree_inventory.create_export(export_format="csv")
        return export

    @pytest.fixture(scope="class")
    def tree_inventory_export_parquet(self, tree_inventory):
        export = tree_inventory.create_export(export_format="parquet")
        return export

    @pytest.fixture(scope="class")
    def tree_inventory_export_geojson(self, tree_inventory):
        export = tree_inventory.create_export(export_format="geojson")
        return export

    @pytest.mark.parametrize(
        "export_fixture",
        [
            "tree_inventory_export_csv",
            "tree_inventory_export_parquet",
            "tree_inventory_export_geojson",
        ],
        ids=["csv", "parquet", "geojson"],
    )
    def test_to_file_with_filename(self, tree_inventory, export_fixture, request):
        """Test downloading exports with specific filenames"""
        # Create and wait for export to complete
        export = request.getfixturevalue(export_fixture)
        export.wait_until_completed(in_place=True)

        # Download with specific filename
        filename = f"trees.{export.format}"
        file_path = TEST_TMP_DIR / filename
        export.to_file(file_path)

        # Verify file was downloaded with correct name
        assert file_path.exists()
        assert file_path.is_file()
        assert filename in [f.name for f in TEST_TMP_DIR.iterdir()]

    @pytest.mark.parametrize(
        "export_fixture, expected_filename",
        [
            ("tree_inventory_export_csv", "tree_inventory.csv"),
            ("tree_inventory_export_parquet", "tree_inventory.parquet.zip"),
            ("tree_inventory_export_geojson", "tree_inventory.geojson"),
        ],
        ids=["csv", "parquet", "geojson"],
    )
    def test_to_file_with_directory(
        self, tree_inventory, export_fixture, expected_filename, request
    ):
        """Test downloading exports to directory without specifying filename"""
        # Create and wait for export to complete
        export = request.getfixturevalue(export_fixture)
        export.wait_until_completed(in_place=True)

        # Download to directory
        export.to_file(TEST_TMP_DIR)

        # Verify file was downloaded with default name
        expected_path = TEST_TMP_DIR / expected_filename
        assert expected_path.exists()
        assert expected_path.is_file()
        assert expected_filename in [f.name for f in TEST_TMP_DIR.iterdir()]
