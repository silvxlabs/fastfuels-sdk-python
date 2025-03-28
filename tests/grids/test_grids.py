"""
grids/test_grids.py
"""

# Core imports
from uuid import uuid4

# Internal imports
from tests.utils import create_default_domain
from fastfuels_sdk.grids import Grids
from fastfuels_sdk.exports import Export
from fastfuels_sdk.client_library.exceptions import NotFoundException, ApiException

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
def test_grids(test_domain):
    """Fixture that creates a test grids object to be used by the tests"""
    grids = Grids.from_domain_id(test_domain.id)

    # Return the grids for use in tests
    yield grids
    # Cleanup handled by test_domain fixture


@pytest.fixture(scope="module")
def test_surface_grid_complete(test_grids):
    """Fixture that creates a complete surface grid for testing"""
    # Create a complete surface grid
    surface_grid = test_grids.create_surface_grid(
        attributes=["fuelMoisture"], fuel_moisture={"source": "uniform", "value": 10}
    )
    surface_grid.wait_until_completed()

    # Return the complete surface grid for use in tests
    yield surface_grid

    # Cleanup: Delete the surface grid after the tests
    surface_grid.delete()


class TestGridsFromDomain:
    def test_success(self, test_domain):
        """Test successful retrieval of grids from a domain"""
        # Get grids using domain
        grids = Grids.from_domain_id(test_domain.id)

        # Verify basic structure and domain relationship
        assert grids is not None
        assert isinstance(grids, Grids)
        assert grids.domain_id == test_domain.id

        # Verify optional grid attributes
        assert hasattr(grids, "tree")
        assert hasattr(grids, "surface")
        assert hasattr(grids, "topography")
        assert hasattr(grids, "feature")

    def test_bad_domain_id(self, test_domain):
        """Test error handling for a non-existent domain ID"""
        bad_test_domain = test_domain.model_copy(deep=True)
        bad_test_domain.id = uuid4().hex
        with pytest.raises(NotFoundException):
            Grids.from_domain_id(bad_test_domain.id)


class TestGetGrids:
    def test_get_update_default(self, test_grids):
        """Test get() returns new instance with updated data by default"""
        original_grids = test_grids
        updated_grids = original_grids.get()

        # Verify new instance returned
        assert updated_grids is not original_grids

        # Verify data matches
        assert updated_grids.domain_id == original_grids.domain_id
        if original_grids.tree:
            assert updated_grids.tree is not None
            assert updated_grids.tree == original_grids.tree
        if original_grids.surface:
            assert updated_grids.surface is not None
            assert updated_grids.surface == original_grids.surface
        if original_grids.topography:
            assert updated_grids.topography is not None
            assert updated_grids.topography == original_grids.topography
        if original_grids.feature:
            assert updated_grids.feature is not None
            assert updated_grids.feature == original_grids.feature

    def test_get_update_in_place(self, test_grids):
        """Test get(in_place=True) updates existing instance"""
        grids = test_grids
        result = grids.get(in_place=True)

        # Verify same instance returned
        assert result is grids

        # Verify instance was updated
        assert isinstance(result, Grids)
        assert result.domain_id == test_grids.domain_id

    def test_get_nonexistent_domain(self, test_grids):
        """Test error handling when domain no longer exists"""
        # Store original domain_id
        original_id = test_grids.domain_id

        # Set invalid domain_id
        test_grids.domain_id = uuid4().hex

        # Verify exception raised
        with pytest.raises(NotFoundException):
            test_grids.get()

        # Restore original domain_id
        test_grids.domain_id = original_id


class TestCreateGridExport:
    @pytest.mark.parametrize("export_format", ["zarr", "QUIC-Fire"])
    def test_create(self, test_grids, export_format, test_surface_grid_complete):
        """Test creating grid exports in different formats"""
        export = test_grids.create_export(export_format=export_format)

        assert export is not None
        assert isinstance(export, Export)
        assert export.status == "pending"
        assert export.domain_id == test_grids.domain_id
        assert export.format == export_format
        assert export.signed_url is None
        assert export.created_on is not None
        assert export.modified_on is not None
        assert export.expires_on is not None

    def test_invalid_format(self, test_grids):
        """Test error handling for invalid export format"""
        with pytest.raises(ApiException):
            test_grids.create_export(export_format="invalid_format")

    def test_nonexistent_domain(self, test_grids):
        """Test error handling when domain does not exist"""
        bad_grids = test_grids.model_copy(deep=True)
        bad_grids.domain_id = uuid4().hex

        with pytest.raises(NotFoundException):
            bad_grids.create_export(export_format="zarr")


class TestGetGridExport:
    @pytest.mark.parametrize("export_format", ["zarr", "QUIC-Fire"])
    def test_get_export(self, test_grids, export_format):
        """Test retrieving grid export status"""
        # First create an export
        test_grids.create_export(export_format=export_format)

        # Get the export status
        retrieved_export = test_grids.get_export(export_format=export_format)

        assert retrieved_export is not None
        assert isinstance(retrieved_export, Export)
        assert retrieved_export.domain_id == test_grids.domain_id
        assert retrieved_export.format == export_format
        assert retrieved_export.status in ["pending", "running", "completed", "failed"]

    @pytest.mark.parametrize("export_format", ["zarr", "QUIC-Fire"])
    def test_nonexistent_export(self, export_format):
        """Test error handling when export does not exist"""
        new_domain = create_default_domain()
        new_grid = Grids.from_domain_id(new_domain.id)
        with pytest.raises(NotFoundException):
            new_grid.get_export(export_format=export_format)
        new_domain.delete()

    def test_invalid_format(self, test_grids):
        """Test error handling for invalid export format"""
        with pytest.raises(ApiException):
            test_grids.get_export(export_format="invalid_format")
