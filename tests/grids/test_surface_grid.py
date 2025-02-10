"""
test_surface_grid.py
"""

# Core imports
from uuid import uuid4

# Internal imports
from tests.utils import create_default_domain, normalize_datetime
from fastfuels_sdk.exports import Export
from fastfuels_sdk.grids import SurfaceGrid, SurfaceGridBuilder
from fastfuels_sdk.client_library.models import GridAttributeMetadataResponse
from fastfuels_sdk.client_library.exceptions import NotFoundException, ApiException

# External imports
import pytest


@pytest.fixture(scope="module")
def domain_fixture():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


@pytest.fixture(scope="module")
def surface_grid_fixture(domain_fixture):
    """Fixture that creates a test surface grid to be used by the tests"""
    surface_grid = (
        SurfaceGridBuilder(domain_id=domain_fixture.id)
        .with_uniform_fuel_load(value=1.0)
        .with_uniform_fuel_moisture(value=15)
        .with_uniform_fuel_depth(value=1.0)
        .build()
    )

    # Return the surface grid for use in tests
    yield surface_grid


@pytest.fixture(scope="module")
def domain_fixture_completed():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


@pytest.fixture(scope="module")
def surface_grid_fixture_completed(domain_fixture):
    """Fixture that creates a test surface grid to be used by the tests"""
    surface_grid = (
        SurfaceGridBuilder(domain_id=domain_fixture.id)
        .with_uniform_fuel_load(value=1.0)
        .with_uniform_fuel_moisture(value=15)
        .with_uniform_fuel_depth(value=1.0)
        .build()
    )

    surface_grid.wait_until_completed()

    # Return the surface grid for use in tests
    yield surface_grid


class TestSurfaceGridFromDomainId:
    def test_success(self, domain_fixture, surface_grid_fixture):
        """Test successful retrieval of a surface grid from a domain ID"""
        # Get the surface grid using the ID from our test domain
        surface_grid = SurfaceGrid.from_domain_id(domain_fixture.id)

        # Verify the retrieved surface grid
        assert surface_grid is not None
        assert isinstance(surface_grid, SurfaceGrid)
        assert surface_grid.domain_id == domain_fixture.id
        assert hasattr(surface_grid, "status")
        assert isinstance(surface_grid.status, str)

    def test_bad_domain_id(self):
        """Test error handling for non-existent domain ID"""
        with pytest.raises(NotFoundException):
            SurfaceGrid.from_domain_id(uuid4().hex)


class TestGetSurfaceGrid:
    """Test suite for SurfaceGrid.get() method."""

    def test_get_update_default(self, surface_grid_fixture):
        """Test get() returns new instance with updated data by default.

        Verifies that:
        1. A new instance is returned (not the same object)
        2. The returned instance is a SurfaceGrid
        3. All data fields match between original and updated grid
        4. The domain_id is preserved
        """
        original_grid = surface_grid_fixture
        updated_grid = original_grid.get()

        # Verify new instance returned
        assert updated_grid is not original_grid
        assert isinstance(updated_grid, SurfaceGrid)

        # Verify all fields match
        assert updated_grid.attributes == original_grid.attributes
        assert updated_grid.fuel_load == original_grid.fuel_load
        assert updated_grid.fuel_depth == original_grid.fuel_depth
        assert updated_grid.fuel_moisture == original_grid.fuel_moisture
        assert updated_grid.savr == original_grid.savr
        assert updated_grid.fbfm == original_grid.fbfm
        assert updated_grid.modifications == original_grid.modifications
        assert updated_grid.status == original_grid.status
        assert updated_grid.checksum == original_grid.checksum
        assert updated_grid.domain_id == original_grid.domain_id

        # Compare full dictionaries using normalized datetimes
        normalized_original = normalize_datetime(original_grid)
        normalized_updated = normalize_datetime(updated_grid)
        assert normalized_updated.to_dict() == normalized_original.to_dict()

    def test_get_update_in_place(self, surface_grid_fixture):
        """Test get(in_place=True) updates existing instance.

        Verifies that:
        1. The same instance is returned (same object)
        2. The instance is a SurfaceGrid
        3. All data fields are properly updated
        4. The domain_id is preserved
        """
        grid = surface_grid_fixture
        original_normalized = normalize_datetime(grid)
        original_dict = original_normalized.to_dict()

        result = grid.get(in_place=True)

        # Verify same instance returned
        assert result is grid
        assert isinstance(result, SurfaceGrid)

        # Verify all fields match
        assert result.attributes == surface_grid_fixture.attributes
        assert result.fuel_load == surface_grid_fixture.fuel_load
        assert result.fuel_depth == surface_grid_fixture.fuel_depth
        assert result.fuel_moisture == surface_grid_fixture.fuel_moisture
        assert result.savr == surface_grid_fixture.savr
        assert result.fbfm == surface_grid_fixture.fbfm
        assert result.modifications == surface_grid_fixture.modifications
        assert result.status == surface_grid_fixture.status
        assert result.checksum == surface_grid_fixture.checksum
        assert result.domain_id == surface_grid_fixture.domain_id

        # Compare full dictionaries using normalized datetimes
        result_normalized = normalize_datetime(result)
        assert result_normalized.to_dict() == original_dict

    def test_get_nonexistent_grid(self, domain_fixture):
        """Test get() with a deleted surface grid raises NotFoundException"""
        # Create a temporary surface grid
        temp_grid = (
            SurfaceGridBuilder(domain_id=domain_fixture.id)
            .with_uniform_fuel_load(value=1.0)
            .build()
        )

        # Delete it
        temp_grid.delete()

        # Attempt to get it should raise NotFoundException
        with pytest.raises(NotFoundException):
            temp_grid.get()


class TestGetSurfaceGridAttributes:
    """Test suite for SurfaceGrid.get_attributes() method."""

    def test_get_attributes_incomplete_grid(self, domain_fixture):
        """Test error handling when grid is not in completed status.

        Should raise ApiException with 422 status when grid is not
        in completed status.
        """
        # Create a new grid that won't be completed
        new_grid = (
            SurfaceGridBuilder(domain_id=domain_fixture.id)
            .with_uniform_fuel_load(value=1.0)
            .build()
        )

        # Should raise 422 error since grid is not completed
        with pytest.raises(ApiException) as exc_info:
            new_grid.get_attributes()
        assert exc_info.value.status == 422

    def test_get_attributes_success(self, surface_grid_fixture_completed):
        """Test successful retrieval of surface grid attribute metadata.

        Verifies that:
        1. Method returns GridAttributeMetadataResponse
        2. Response contains expected metadata fields
        3. Response structure matches API specifications
        """
        metadata = surface_grid_fixture_completed.get_attributes()

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


class TestCreateSurfaceGridExport:
    """Test suite for SurfaceGrid.create_export() method."""

    @pytest.mark.parametrize("export_format", ["zarr", "geotiff"])
    def test_create_incomplete_surface_grid(self, domain_fixture, export_format):
        """Test creating an export for an incomplete surface grid.

        Should raise ApiException since the surface grid is not completed yet.

        Parameters
        ----------
        export_format : str
            Format to test export with ("zarr" or "geotiff")
        """
        new_surface_grid = (
            SurfaceGridBuilder(domain_id=domain_fixture.id)
            .with_uniform_fuel_load(value=1.0)
            .build()
        )
        with pytest.raises(ApiException):
            new_surface_grid.create_export(export_format=export_format)

    @pytest.mark.parametrize("export_format", ["zarr", "geotiff"])
    def test_create_export_success(self, surface_grid_fixture_completed, export_format):
        """Test successful creation of a surface grid export.

        Verifies that:
        1. Export object is created successfully
        2. Export object has correct structure and fields
        3. Export is associated with the correct domain
        4. Export format is set correctly

        Parameters
        ----------
        export_format : str
            Format to test export with ("zarr" or "geotiff")
        """
        export = surface_grid_fixture_completed.create_export(
            export_format=export_format
        )

        # Verify export object
        assert export is not None
        assert isinstance(export, Export)

        # Verify export attributes
        assert export.domain_id == surface_grid_fixture_completed.domain_id
        assert export.resource == "grids"
        assert export.sub_resource == "surface"
        assert export.format == export_format
        assert export.status == "pending"
        assert export.created_on is not None
        assert export.modified_on is not None
        assert export.expires_on is not None
        assert export.signed_url is None  # URL not available until completed

    def test_create_export_invalid_format(self, surface_grid_fixture_completed):
        """Test error handling for invalid export format."""
        with pytest.raises(ApiException):
            surface_grid_fixture_completed.create_export(export_format="invalid_format")

    def test_create_export_deleted_grid(self, domain_fixture):
        """Test creating export for a deleted surface grid.

        Should raise NotFoundException when attempting to create an export
        for a grid that has been deleted.
        """
        # Create and delete a temporary grid
        temp_grid = (
            SurfaceGridBuilder(domain_id=domain_fixture.id)
            .with_uniform_fuel_load(value=1.0)
            .build()
        )
        temp_grid.wait_until_completed()
        temp_grid.delete()

        # Attempt to create export should raise NotFoundException
        with pytest.raises(NotFoundException):
            temp_grid.create_export(export_format="zarr")
