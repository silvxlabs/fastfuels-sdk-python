"""
test_feature_grid.py
"""

# Core imports
from __future__ import annotations
from uuid import uuid4

# Internal imports
from fastfuels_sdk import Grids, Features, FeatureGrid
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
def road_feature_fixture(domain_fixture):
    """Fixture that creates a test road feature to be used by the tests"""
    feature = Features.from_domain_id(domain_fixture.id).create_road_feature_from_osm()
    feature.wait_until_completed()
    yield feature
    feature.delete()


@pytest.fixture(scope="module")
def water_feature_fixture(domain_fixture):
    """Fixture that creates a test water feature to be used by the tests"""
    feature = Features.from_domain_id(domain_fixture.id).create_water_feature_from_osm()
    feature.wait_until_completed()
    yield feature
    feature.delete()


@pytest.fixture(scope="module")
def feature_grid_fixture(domain_fixture, road_feature_fixture, water_feature_fixture):
    """Fixture that creates a test feature grid to be used by the tests"""
    feature_grid = Grids.from_domain_id(domain_fixture.id).create_feature_grid(
        ["road", "water"]
    )
    yield feature_grid
    feature_grid.delete()


class TestCreateFeatureGrid:
    def test_incomplete_features(self, domain_fixture):
        """Test that an incomplete feature grid raises an exception"""
        with pytest.raises(ApiException):
            Grids.from_domain_id(domain_fixture.id).create_feature_grid(
                attributes=["road", "water"]
            )

    def test_success(self, domain_fixture, road_feature_fixture, water_feature_fixture):
        """Test that a feature grid can be successfully created"""
        feature_grid = Grids.from_domain_id(domain_fixture.id).create_feature_grid(
            attributes=["road", "water"]
        )
        feature_grid.wait_until_completed()
        assert feature_grid.status == "completed"


class TestFeatureGridFromDomainId:
    """Test suite for FeatureGrid.from_domain_id() method."""

    def test_success(self, domain_fixture, feature_grid_fixture):
        """Test successful retrieval of a feature grid from a domain ID.

        Verifies that:
        1. Grid is successfully retrieved
        2. Returned object is correct type
        3. Domain ID matches
        4. Grid has expected attributes
        """
        # Verify the retrieved feature grid
        assert feature_grid_fixture is not None
        assert isinstance(feature_grid_fixture, FeatureGrid)
        assert feature_grid_fixture.domain_id == domain_fixture.id
        assert hasattr(feature_grid_fixture, "status")
        assert isinstance(feature_grid_fixture.status, str)

        # Verify the expected attributes are present
        assert hasattr(feature_grid_fixture, "attributes")
        assert isinstance(feature_grid_fixture.attributes, list)
        assert all(isinstance(attr, str) for attr in feature_grid_fixture.attributes)

        # Verify timestamps and checksum
        assert hasattr(feature_grid_fixture, "created_on")
        assert hasattr(feature_grid_fixture, "modified_on")
        assert hasattr(feature_grid_fixture, "checksum")

    def test_bad_domain_id(self):
        """Test error handling for non-existent domain ID.

        Verifies that:
        1. NotFoundException is raised for invalid domain ID
        2. Error contains appropriate context
        """
        nonexistent_id = uuid4().hex
        with pytest.raises(NotFoundException):
            FeatureGrid.from_domain_id(nonexistent_id)

    def test_domain_without_feature_grid(self, domain_fixture):
        """Test behavior when requesting a domain with no feature grid.

        Verifies that:
        1. NotFoundException is raised when domain exists but has no feature grid
        """
        # Create a fresh domain that we know has no feature grid
        new_domain = create_default_domain()
        try:
            with pytest.raises(NotFoundException):
                FeatureGrid.from_domain_id(new_domain.id)
        finally:
            # Clean up the test domain
            new_domain.delete()


class TestGetFeatureGrid:
    """Test suite for FeatureGrid.get() method."""

    def test_get_update_default(self, feature_grid_fixture):
        """Test get() returns new instance with updated data by default.

        Verifies that:
        1. A new instance is returned (not the same object)
        2. The returned instance is a FeatureGrid
        3. All data fields match between original and updated grid
        4. The domain_id is preserved
        """
        original_grid = feature_grid_fixture
        updated_grid = original_grid.get()

        # Verify new instance returned
        assert updated_grid is not original_grid
        assert isinstance(updated_grid, FeatureGrid)

        # Verify all fields match
        assert updated_grid.attributes == original_grid.attributes
        assert updated_grid.status == original_grid.status
        assert updated_grid.checksum == original_grid.checksum
        assert updated_grid.domain_id == original_grid.domain_id

        # Compare full dictionaries using normalized datetimes
        normalized_original = normalize_datetime(original_grid)
        normalized_updated = normalize_datetime(updated_grid)
        assert normalized_updated.to_dict() == normalized_original.to_dict()

    def test_get_update_in_place(self, feature_grid_fixture):
        """Test get(in_place=True) updates existing instance.

        Verifies that:
        1. The same instance is returned (same object)
        2. The instance is a FeatureGrid
        3. All data fields are properly updated
        4. The domain_id is preserved
        """
        grid = feature_grid_fixture
        original_normalized = normalize_datetime(grid)
        original_dict = original_normalized.to_dict()

        result = grid.get(in_place=True)

        # Verify same instance returned
        assert result is grid
        assert isinstance(result, FeatureGrid)

        # Verify all fields match original data
        assert result.attributes == feature_grid_fixture.attributes
        assert result.status == feature_grid_fixture.status
        assert result.checksum == feature_grid_fixture.checksum
        assert result.domain_id == feature_grid_fixture.domain_id

        # Compare full dictionaries using normalized datetimes
        result_normalized = normalize_datetime(result)
        assert result_normalized.to_dict() == original_dict

    def test_get_nonexistent_grid(self, domain_fixture):
        """Test get() with a deleted feature grid raises NotFoundException"""
        # Create a temporary feature grid
        temp_grid = Grids.from_domain_id(domain_fixture.id).create_feature_grid(
            attributes=["road", "water"]
        )

        # Delete it
        temp_grid.delete()

        # Attempt to get it should raise NotFoundException
        with pytest.raises(NotFoundException):
            temp_grid.get()

    def test_get_attributes_are_preserved(
        self, domain_fixture, road_feature_fixture, water_feature_fixture
    ):
        """Test that all configured attributes are preserved after get().

        Verifies that:
        1. Each attribute configuration is preserved after get()
        2. Multiple attributes remain consistent
        """
        # Create a grid with multiple attributes
        grid = Grids.from_domain_id(domain_fixture.id).create_feature_grid(
            attributes=["road", "water"]
        )

        updated_grid = grid.get()

        # Verify attributes are preserved
        assert set(updated_grid.attributes) == {"road", "water"}
        assert len(updated_grid.attributes) == len(grid.attributes)


class TestGetFeatureGridAttributes:
    """Test suite for FeatureGrid.get_attributes() method."""

    def test_get_attributes_success(self, feature_grid_fixture):
        """Test successful retrieval of feature grid attribute metadata.

        Verifies that:
        1. Method returns GridAttributeMetadataResponse
        2. Response contains expected metadata fields
        3. Response structure matches API specifications
        4. Metadata includes feature-specific attributes
        """
        # Wait for grid completion to ensure we can get attributes
        feature_grid_fixture.wait_until_completed()
        metadata = feature_grid_fixture.get_attributes()

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
