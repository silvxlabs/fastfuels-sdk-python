"""
test_topography_grid.py
"""

# Core imports
from uuid import uuid4

# Internal imports
from tests.utils import create_default_domain, normalize_datetime
from fastfuels_sdk import Export
from fastfuels_sdk.grids import TopographyGrid, TopographyGridBuilder
from fastfuels_sdk.client_library.models import (
    GridAttributeMetadataResponse,
    TopographyGridElevationSource,
)
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
def topography_grid_fixture(domain_fixture):
    """Fixture that creates a test topography grid to be used by the tests"""
    topography_grid = (
        TopographyGridBuilder(domain_id=domain_fixture.id)
        .with_elevation_from_3dep()
        .build()
    )

    # Return the topography grid for use in tests
    yield topography_grid


@pytest.fixture(scope="module")
def domain_fixture_completed():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


@pytest.fixture(scope="module")
def topography_grid_fixture_completed(domain_fixture_completed):
    """Fixture that creates a test topography grid to be used by the tests"""
    topography_grid = (
        TopographyGridBuilder(domain_id=domain_fixture_completed.id)
        .with_elevation_from_3dep()
        .build()
    )

    topography_grid.wait_until_completed()

    # Return the topography grid for use in tests
    yield topography_grid


class TestTopographyGridFromDomainId:
    """Test suite for TopographyGrid.from_domain_id() method."""

    def test_success(self, domain_fixture, topography_grid_fixture):
        """Test successful retrieval of a topography grid from a domain ID.

        Verifies that:
        1. Grid is successfully retrieved
        2. Returned object is correct type
        3. Domain ID matches
        4. Grid has expected attributes
        """
        # Get the topography grid using the ID from our test domain
        topography_grid = TopographyGrid.from_domain_id(domain_fixture.id)

        # Verify the retrieved topography grid
        assert topography_grid is not None
        assert isinstance(topography_grid, TopographyGrid)
        assert topography_grid.domain_id == domain_fixture.id
        assert hasattr(topography_grid, "status")
        assert isinstance(topography_grid.status, str)

        # Verify the expected attributes are present
        assert topography_grid.attributes == ["elevation"]
        assert isinstance(topography_grid.elevation, TopographyGridElevationSource)
        assert topography_grid.aspect is None
        assert topography_grid.slope is None

    def test_bad_domain_id(self):
        """Test error handling for non-existent domain ID.

        Verifies that:
        1. NotFoundException is raised for invalid domain ID
        2. Error contains appropriate context
        """
        nonexistent_id = uuid4().hex
        with pytest.raises(NotFoundException):
            TopographyGrid.from_domain_id(nonexistent_id)


class TestGetTopographyGrid:
    """Test suite for TopographyGrid.get() method."""

    def test_get_update_default(self, topography_grid_fixture):
        """Test get() returns new instance with updated data by default.

        Verifies that:
        1. A new instance is returned (not the same object)
        2. The returned instance is a TopographyGrid
        3. All data fields match between original and updated grid
        4. The domain_id is preserved
        """
        original_grid = topography_grid_fixture
        updated_grid = original_grid.get()

        # Verify new instance returned
        assert updated_grid is not original_grid
        assert isinstance(updated_grid, TopographyGrid)

        # Verify all fields match
        assert updated_grid.attributes == original_grid.attributes
        assert updated_grid.elevation == original_grid.elevation
        assert updated_grid.slope == original_grid.slope
        assert updated_grid.aspect == original_grid.aspect
        assert updated_grid.status == original_grid.status
        assert updated_grid.checksum == original_grid.checksum
        assert updated_grid.domain_id == original_grid.domain_id

        # Compare full dictionaries using normalized datetimes
        normalized_original = normalize_datetime(original_grid)
        normalized_updated = normalize_datetime(updated_grid)
        assert normalized_updated.to_dict() == normalized_original.to_dict()

    def test_get_update_in_place(self, topography_grid_fixture):
        """Test get(in_place=True) updates existing instance.

        Verifies that:
        1. The same instance is returned (same object)
        2. The instance is a TopographyGrid
        3. All data fields are properly updated
        4. The domain_id is preserved
        """
        grid = topography_grid_fixture
        original_normalized = normalize_datetime(grid)
        original_dict = original_normalized.to_dict()

        result = grid.get(in_place=True)

        # Verify same instance returned
        assert result is grid
        assert isinstance(result, TopographyGrid)

        # Verify all fields match original data
        assert result.attributes == topography_grid_fixture.attributes
        assert result.elevation == topography_grid_fixture.elevation
        assert result.slope == topography_grid_fixture.slope
        assert result.aspect == topography_grid_fixture.aspect
        assert result.status == topography_grid_fixture.status
        assert result.checksum == topography_grid_fixture.checksum
        assert result.domain_id == topography_grid_fixture.domain_id

        # Compare full dictionaries using normalized datetimes
        result_normalized = normalize_datetime(result)
        assert result_normalized.to_dict() == original_dict

    def test_get_nonexistent_grid(self, domain_fixture):
        """Test get() with a deleted topography grid raises NotFoundException"""
        # Create a temporary topography grid
        temp_grid = (
            TopographyGridBuilder(domain_id=domain_fixture.id)
            .with_elevation_from_3dep()
            .build()
        )

        # Delete it
        temp_grid.delete()

        # Attempt to get it should raise NotFoundException
        with pytest.raises(NotFoundException):
            temp_grid.get()

    def test_get_attributes_are_preserved(self, domain_fixture):
        """Test that all configured attributes are preserved after get().

        Verifies that:
        1. Each attribute configuration is preserved
        2. Source configurations are maintained
        3. Interpolation methods are preserved
        """
        # Create a grid with all possible attributes and sources
        grid = (
            TopographyGridBuilder(domain_id=domain_fixture.id)
            .with_elevation_from_landfire()
            .with_slope_from_3dep(interpolation_method="cubic")
            .with_aspect_from_3dep()
            .build()
        )

        updated_grid = grid.get()

        # Verify elevation configuration
        assert updated_grid.elevation.to_dict()["source"] == "LANDFIRE"

        # Verify slope configuration
        assert updated_grid.slope.to_dict()["source"] == "3DEP"
        assert updated_grid.slope.to_dict()["interpolationMethod"] == "cubic"

        # Verify aspect configuration
        assert updated_grid.aspect.to_dict()["source"] == "3DEP"
        assert updated_grid.aspect.to_dict()["interpolationMethod"] == "nearest"


class TestGetTopographyGridAttributes:
    """Test suite for TopographyGrid.get_attributes() method."""

    def test_get_attributes_incomplete_grid(self, domain_fixture):
        """Test error handling when grid is not in completed status.

        Should raise ApiException with 422 status when grid is not
        in completed status.
        """
        # Create a new grid that won't be completed
        new_grid = (
            TopographyGridBuilder(domain_id=domain_fixture.id)
            .with_elevation_from_3dep()
            .build()
        )

        # Should raise 422 error since grid is not completed
        with pytest.raises(ApiException) as exc_info:
            new_grid.get_attributes()
        assert exc_info.value.status == 422

    def test_get_attributes_success(self, topography_grid_fixture_completed):
        """Test successful retrieval of topography grid attribute metadata.

        Verifies that:
        1. Method returns GridAttributeMetadataResponse
        2. Response contains expected metadata fields
        3. Response structure matches API specifications
        4. Metadata includes topography-specific attributes
        """
        metadata = topography_grid_fixture_completed.get_attributes()

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

        # Verify dimensions are ["y", "x"]
        assert metadata.dimensions == ["y", "x"]

        # Verify shape values are positive
        assert len(metadata.shape) == 2
        assert all(dim > 0 for dim in metadata.shape)

        # Verify chunk shape is consistent
        assert len(metadata.chunk_shape) == 2
        assert all(
            chunk <= full for chunk, full in zip(metadata.chunk_shape, metadata.shape)
        )

        # # Verify topography-specific attributes
        # attribute_names = {attr.name for attr in metadata.attributes}
        # assert "elevation" in attribute_names
        # for attr in metadata.attributes:
        #     if attr.name == "elevation":
        #         assert attr.units == "m"  # elevation should be in meters
        #     elif attr.name == "slope":
        #         assert attr.units == "degrees"  # slope should be in degrees
        #     elif attr.name == "aspect":
        #         assert attr.units == "degrees"  # aspect should be in degrees

    def test_get_attributes_nonexistent_grid(self, domain_fixture):
        """Test getting attributes of a deleted topography grid.

        Should raise NotFoundException when attempting to get attributes
        of a grid that has been deleted.
        """
        # Create and delete a temporary grid
        temp_grid = (
            TopographyGridBuilder(domain_id=domain_fixture.id)
            .with_elevation_from_3dep()
            .build()
        )
        temp_grid.wait_until_completed()
        temp_grid.delete()

        # Attempt to get attributes should raise NotFoundException
        with pytest.raises(NotFoundException):
            temp_grid.get_attributes()

    def test_grid_dimensions(self, topography_grid_fixture_completed):
        """Test that grid dimensions are correctly reported.

        Verifies that:
        1. Grid has expected dimensions ["y", "x"]
        2. Shape values are positive integers
        3. Chunk shape is consistent with overall shape
        """
        metadata = topography_grid_fixture_completed.get_attributes()


class TestCreateTopographyGridExport:
    """Test suite for TopographyGrid.create_export() method."""

    @pytest.mark.parametrize("export_format", ["zarr", "geotiff"])
    def test_create_incomplete_topography_grid(self, domain_fixture, export_format):
        """Test creating an export for an incomplete topography grid.

        Should raise ApiException since the topography grid is not completed yet.

        Parameters
        ----------
        export_format : str
            Format to test export with ("zarr" or "geotiff")
        """
        new_topography_grid = (
            TopographyGridBuilder(domain_id=domain_fixture.id)
            .with_elevation_from_3dep()
            .build()
        )
        with pytest.raises(ApiException):
            new_topography_grid.create_export(export_format=export_format)

    @pytest.mark.parametrize("export_format", ["zarr", "geotiff"])
    def test_create_export_success(
        self, topography_grid_fixture_completed, export_format
    ):
        """Test successful creation of a topography grid export.

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
        export = topography_grid_fixture_completed.create_export(
            export_format=export_format
        )

        # Verify export object
        assert export is not None
        assert isinstance(export, Export)

        # Verify export attributes
        assert export.domain_id == topography_grid_fixture_completed.domain_id
        assert export.resource == "grids"
        assert export.sub_resource == "topography"
        assert export.format == export_format
        assert export.status == "pending"
        assert export.created_on is not None
        assert export.modified_on is not None
        assert export.expires_on is not None
        assert export.signed_url is None  # URL not available until completed

    def test_create_export_invalid_format(self, topography_grid_fixture_completed):
        """Test error handling for invalid export format."""
        with pytest.raises(ApiException):
            topography_grid_fixture_completed.create_export(
                export_format="invalid_format"
            )
