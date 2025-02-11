"""
test_tree_grid.py
"""

# Core imports
from __future__ import annotations
from uuid import uuid4

# Internal imports
from fastfuels_sdk import Inventories, TreeGrid, TreeGridBuilder, Export
from fastfuels_sdk.client_library.models import GridAttributeMetadataResponse
from fastfuels_sdk.client_library.exceptions import NotFoundException, ApiException
from tests.utils import create_default_domain, normalize_datetime

# External imports
import pytest


@pytest.fixture(scope="module")
def domain_fixture():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()
    yield domain
    domain.delete()


@pytest.fixture(scope="module")
def tree_inventory_fixture(domain_fixture):
    """Fixture that creates a test tree inventory to be used by the tests"""
    tree_inventory = Inventories.from_domain_id(
        domain_id=domain_fixture.id
    ).create_tree_inventory_from_treemap()

    tree_inventory.wait_until_completed()

    yield tree_inventory


@pytest.fixture(scope="module")
def tree_grid_fixture(domain_fixture, tree_inventory_fixture):
    """Fixture that creates a test tree grid to be used by the tests"""
    tree_grid = (
        TreeGridBuilder(domain_id=domain_fixture.id)
        .with_bulk_density_from_tree_inventory()
        .build()
    )

    yield tree_grid


@pytest.fixture(scope="module")
def domain_fixture_completed():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()
    yield domain
    domain.delete()


@pytest.fixture(scope="module")
def tree_inventory_fixture_completed(domain_fixture_completed):
    """Fixture that creates a test tree inventory to be used by the tests"""
    tree_inventory = Inventories.from_domain_id(
        domain_id=domain_fixture_completed.id
    ).create_tree_inventory_from_treemap()

    tree_inventory.wait_until_completed()

    yield tree_inventory


@pytest.fixture(scope="module")
def tree_grid_fixture_completed(
    domain_fixture_completed, tree_inventory_fixture_completed
):
    """Fixture that creates a test tree grid to be used by the tests"""
    tree_grid = (
        TreeGridBuilder(domain_id=domain_fixture_completed.id)
        .with_bulk_density_from_tree_inventory()
        .build()
    )
    tree_grid.wait_until_completed()

    yield tree_grid


class TestTreeGridFromDomainId:
    """Test suite for TreeGrid.from_domain_id() method."""

    def test_success(self, domain_fixture, tree_grid_fixture):
        """Test successful retrieval of a tree grid from a domain ID.

        Verifies that:
        1. Grid is successfully retrieved
        2. Returned object is correct type
        3. Domain ID matches
        4. Grid has expected attributes
        """
        # Get the tree grid using the ID from our test domain
        tree_grid = TreeGrid.from_domain_id(domain_fixture.id)

        # Verify the retrieved tree grid
        assert tree_grid is not None
        assert isinstance(tree_grid, TreeGrid)
        assert tree_grid.domain_id == domain_fixture.id
        assert hasattr(tree_grid, "status")
        assert isinstance(tree_grid.status, str)

    def test_bad_domain_id(self):
        """Test error handling for non-existent domain ID.

        Verifies that:
        1. NotFoundException is raised for invalid domain ID
        2. Error contains appropriate context
        """
        nonexistent_id = uuid4().hex
        with pytest.raises(NotFoundException):
            TreeGrid.from_domain_id(nonexistent_id)


class TestGetTreeGrid:
    """Test suite for TreeGrid.get() method."""

    def test_get_update_default(self, tree_grid_fixture):
        """Test get() returns new instance with updated data by default.

        Verifies that:
        1. A new instance is returned (not the same object)
        2. The returned instance is a TreeGrid
        3. All data fields match between original and updated grid
        4. The domain_id is preserved
        """
        original_grid = tree_grid_fixture
        updated_grid = original_grid.get()

        # Verify new instance returned
        assert updated_grid is not original_grid
        assert isinstance(updated_grid, TreeGrid)

        # Verify all fields match
        assert updated_grid.attributes == original_grid.attributes
        assert updated_grid.bulk_density == original_grid.bulk_density
        assert updated_grid.status == original_grid.status
        assert updated_grid.checksum == original_grid.checksum
        assert updated_grid.domain_id == original_grid.domain_id

        # Compare full dictionaries using normalized datetimes
        normalized_original = normalize_datetime(original_grid)
        normalized_updated = normalize_datetime(updated_grid)
        assert normalized_updated.to_dict() == normalized_original.to_dict()

    def test_get_update_in_place(self, tree_grid_fixture):
        """Test get(in_place=True) updates existing instance.

        Verifies that:
        1. The same instance is returned (same object)
        2. The instance is a TreeGrid
        3. All data fields are properly updated
        4. The domain_id is preserved
        """
        grid = tree_grid_fixture
        original_normalized = normalize_datetime(grid)
        original_dict = original_normalized.to_dict()

        result = grid.get(in_place=True)

        # Verify same instance returned
        assert result is grid
        assert isinstance(result, TreeGrid)

        # Verify all fields match
        assert result.attributes == tree_grid_fixture.attributes
        assert result.bulk_density == tree_grid_fixture.bulk_density
        assert result.status == tree_grid_fixture.status
        assert result.checksum == tree_grid_fixture.checksum
        assert result.domain_id == tree_grid_fixture.domain_id

        # Compare full dictionaries using normalized datetimes
        result_normalized = normalize_datetime(result)
        assert result_normalized.to_dict() == original_dict

    def test_get_nonexistent_grid(self, domain_fixture, tree_inventory_fixture):
        """Test get() with a deleted tree grid raises NotFoundException"""
        # Create a temporary tree grid
        temp_grid = (
            TreeGridBuilder(domain_id=domain_fixture.id)
            .with_bulk_density_from_tree_inventory()
            .build()
        )

        # Delete it
        temp_grid.delete()

        # Attempt to get it should raise NotFoundException
        with pytest.raises(NotFoundException):
            temp_grid.get()


class TestGetTreeGridAttributes:
    """Test suite for TreeGrid.get_attributes() method."""

    def test_get_attributes_incomplete_grid(
        self, domain_fixture, tree_inventory_fixture
    ):
        """Test error handling when grid is not in completed status.

        Should raise ApiException with 422 status when grid is not
        in completed status.
        """
        # Create a new grid that won't be completed
        new_grid = (
            TreeGridBuilder(domain_id=domain_fixture.id)
            .with_bulk_density_from_tree_inventory()
            .build()
        )

        # Should raise 422 error since grid is not completed
        with pytest.raises(ApiException) as exc_info:
            new_grid.get_attributes()
        assert exc_info.value.status == 422

    def test_get_attributes_success(self, tree_grid_fixture_completed):
        """Test successful retrieval of tree grid attribute metadata.

        Verifies that:
        1. Method returns GridAttributeMetadataResponse
        2. Response contains expected metadata fields
        3. Response structure matches API specifications
        4. Metadata includes tree-specific attributes
        """
        metadata = tree_grid_fixture_completed.get_attributes()

        # Verify response type and basic structure
        assert metadata is not None
        assert isinstance(metadata, GridAttributeMetadataResponse)

        # Verify required fields are present
        assert hasattr(metadata, "shape")
        assert hasattr(metadata, "dimensions")
        assert hasattr(metadata, "chunks")
        assert hasattr(metadata, "chunk_shape")
        assert hasattr(metadata, "attributes")

        # Verify field types
        assert isinstance(metadata.shape, list)
        assert isinstance(metadata.dimensions, list)
        assert isinstance(metadata.chunks, list)
        assert isinstance(metadata.chunk_shape, list)
        assert isinstance(metadata.attributes, list)

        # Verify dimensions and chunk shape match
        assert metadata.dimensions == ["z", "y", "x"]
        assert len(metadata.shape) == 3
        assert len(metadata.chunks) == 3


class TestCreateTreeGridExport:
    """Test suite for TreeGrid.create_export() method."""

    @pytest.mark.parametrize("export_format", ["zarr"])
    def test_create_incomplete_tree_grid(self, domain_fixture, export_format):
        """Test creating an export for an incomplete tree grid.

        Should raise ApiException since the tree grid is not completed yet.

        Parameters
        ----------
        export_format : str
            Format to test export with ("zarr")
        """
        new_tree_grid = (
            TreeGridBuilder(domain_id=domain_fixture.id)
            .with_bulk_density_from_tree_inventory()
            .build()
        )
        with pytest.raises(ApiException):
            new_tree_grid.create_export(export_format=export_format)

    @pytest.mark.parametrize("export_format", ["zarr"])
    def test_create_export_success(self, tree_grid_fixture_completed, export_format):
        """Test successful creation of a tree grid export.

        Verifies that:
        1. Export object is created successfully
        2. Export object has correct structure and fields
        3. Export is associated with the correct domain
        4. Export format is set correctly

        Parameters
        ----------
        export_format : str
            Format to test export with ("zarr")
        """
        export = tree_grid_fixture_completed.create_export(export_format=export_format)

        # Verify export object
        assert export is not None
        assert isinstance(export, Export)

        # Verify export attributes
        assert export.domain_id == tree_grid_fixture_completed.domain_id
        assert export.resource == "grids"
        assert export.sub_resource == "tree"
        assert export.format == export_format
        assert export.status == "pending"
        assert export.created_on is not None
        assert export.modified_on is not None
        assert export.expires_on is not None
        assert export.signed_url is None  # URL not available until completed

    def test_create_export_invalid_format(self, tree_grid_fixture_completed):
        """Test error handling for invalid export format."""
        with pytest.raises(ApiException):
            tree_grid_fixture_completed.create_export(export_format="invalid_format")
