"""
test_pointclouds.py
"""

# Core imports
from uuid import uuid4
from datetime import datetime

# Internal imports
from tests.utils import create_default_domain_threedep, normalize_datetime
from fastfuels_sdk.pointclouds import PointClouds, AlsPointCloud
from fastfuels_sdk.client_library.exceptions import NotFoundException

# External imports
import pytest


@pytest.fixture(scope="module")
def test_domain():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain_threedep()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    try:
        domain.delete()
    except NotFoundException:
        pass


@pytest.fixture(scope="module")
def test_pointclouds(test_domain):
    """Fixture that creates a test pointclouds object to be used by the tests"""
    pc = PointClouds.from_domain_id(test_domain.id)
    # The pointclouds resource exists implicitly or is empty by default
    yield pc


class TestPointCloudsFromDomain:
    def test_success(self, test_domain):
        """Test successful retrieval of pointclouds from a domain"""
        pc = PointClouds.from_domain_id(test_domain.id)

        # Verify basic structure and domain relationship
        assert pc is not None
        assert isinstance(pc, PointClouds)
        assert pc.domain_id == test_domain.id

        # ALS should be None initially if not created
        # (Assuming the API returns empty/null for als initially)
        # If the API returns an empty object, adjust this assertion.
        if pc.als:
            assert isinstance(pc.als, AlsPointCloud)

    def test_bad_domain_id(self, test_domain):
        """Test error handling for a non-existent domain ID"""
        bad_test_domain = test_domain.model_copy(deep=True)
        bad_test_domain.id = uuid4().hex

        # Depending on API implementation, this might raise NotFound immediately
        # or return a valid object that fails on subsequent calls.
        # Assuming strictly mirrored behavior from Features:
        with pytest.raises(NotFoundException):
            PointClouds.from_domain_id(bad_test_domain.id)


class TestGetPointClouds:
    def test_get_update_default(self, test_pointclouds):
        """Test get() returns new instance with updated data by default"""
        original_pc = test_pointclouds
        updated_pc = original_pc.get()

        # Verify new instance returned
        assert updated_pc is not original_pc
        assert isinstance(updated_pc, PointClouds)

        # Verify data matches
        assert updated_pc.domain_id == original_pc.domain_id
        if original_pc.als:
            assert updated_pc.als is not None
            assert updated_pc.als.checksum == original_pc.als.checksum

    def test_get_update_in_place(self, test_pointclouds):
        """Test get(in_place=True) updates existing instance"""
        pc = test_pointclouds
        result = pc.get(in_place=True)

        # Verify same instance returned
        assert result is pc

        # Verify instance was updated/refreshed
        assert isinstance(result, PointClouds)
        assert result.domain_id == test_pointclouds.domain_id

    def test_get_nonexistent_domain(self, test_pointclouds):
        """Test error handling when domain no longer exists"""
        # Store original domain_id
        original_id = test_pointclouds.domain_id

        # Set invalid domain_id
        test_pointclouds.domain_id = uuid4().hex

        # Verify exception raised
        with pytest.raises(NotFoundException):
            test_pointclouds.get()

        # Restore original domain_id
        test_pointclouds.domain_id = original_id


class TestCreateAlsPointCloud:
    @staticmethod
    def assert_data_validity(als, domain_id):
        """Validates the basic ALS point cloud data"""
        assert als is not None
        assert isinstance(als, AlsPointCloud)
        assert als.domain_id == domain_id
        assert als.status in ["pending", "running", "completed", "failed"]
        # Checksum is typically set upon creation
        assert isinstance(als.checksum, str) and len(als.checksum) > 0

    def test_create_with_3dep_source(self, test_pointclouds):
        """Tests ALS creation with '3DEP' source (public data)"""
        # Use '3DEP' as it likely triggers background job
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])

        self.assert_data_validity(als, test_pointclouds.domain_id)
        assert "3DEP" in als.sources

        # Original parent object should rely on subsequent refresh or be independent
        # unless in_place was used.
        assert test_pointclouds.als is not als

    def test_create_with_file_source(self, test_pointclouds):
        """Tests ALS creation with 'file' source (upload instructions)"""
        als = test_pointclouds.create_als_point_cloud(sources=["file"])

        self.assert_data_validity(als, test_pointclouds.domain_id)
        # Check if "file" is in the sources list (this is a list of strings/enums, so 'in' works here)
        assert "file" in als.sources

        # Verify file upload instructions exist using Dot Notation
        assert als.file is not None
        assert als.file.url is not None
        assert als.file.headers is not None
        # Optional: Verify specific header content if needed
        assert "x-goog-content-length-range" in als.file.headers

    def test_create_in_place_true(self, test_pointclouds):
        """Test ALS creation with in_place=True"""
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"], in_place=True)

        self.assert_data_validity(als, test_pointclouds.domain_id)
        # Parent object should be updated
        assert test_pointclouds.als is als
        assert test_pointclouds.als.status in ["pending", "running", "completed"]

    def test_create_nonexistent_domain(self, test_pointclouds):
        """Test error handling for non-existent domain"""
        bad_pc = test_pointclouds.model_copy(deep=True)
        bad_pc.domain_id = uuid4().hex

        with pytest.raises(NotFoundException):
            bad_pc.create_als_point_cloud(sources=["3DEP"])


class TestGetAlsPointCloud:
    def test_default(self, test_pointclouds):
        """Tests fetching ALS data returns new instance by default"""
        # First create an ALS resource
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])

        # Get latest data
        updated = als.get()

        # Verify new instance returned
        assert updated is not None
        assert isinstance(updated, AlsPointCloud)
        assert updated is not als
        assert normalize_datetime(updated) == normalize_datetime(als)

    def test_in_place(self, test_pointclouds):
        """Tests fetching ALS data in place"""
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])
        result = als.get(in_place=True)

        # Verify same instance returned and updated
        assert result is als
        assert isinstance(result, AlsPointCloud)

    def test_get_nonexistent_domain(self, test_pointclouds):
        """Test error handling when domain no longer exists"""
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])

        # Store original domain_id
        original_id = als.domain_id

        # Set invalid domain_id
        als.domain_id = uuid4().hex

        # Verify exception raised
        with pytest.raises(NotFoundException):
            als.get()

        # Restore original domain_id
        als.domain_id = original_id


class TestWaitUntilCompletedAlsPointCloud:
    def test_wait_until_completed_default(self, test_pointclouds):
        """Test waiting for ALS to complete with default settings"""
        # Ensure we use 3DEP so it actually processes (file source waits for upload)
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])

        # Depending on test environment speed, this might finish instantly or take time
        completed = als.wait_until_completed(step=1, timeout=60)

        assert completed is als  # In-place by default
        assert completed.status == "completed"
        assert isinstance(completed.created_on, datetime)

    def test_wait_until_completed_not_in_place(self, test_pointclouds):
        """Test waiting without in-place updates"""
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])
        completed = als.wait_until_completed(in_place=False)

        assert completed is not als  # New instance
        assert completed.status == "completed"
        # Original might still be pending or completed depending on timing,
        # but the key check is that 'completed' is a different object.

    def test_wait_until_completed_timeout(self, test_pointclouds):
        """Test timeout handling"""
        # Create a new job
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])

        # If the job is instant in test env, skip check, otherwise verify timeout
        if als.status != "completed":
            with pytest.raises(TimeoutError):
                als.wait_until_completed(timeout=0.001)  # Extremely short timeout

    def test_wait_until_completed_nonexistent_domain(self, test_pointclouds):
        """Test error handling when domain no longer exists"""
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])
        als.domain_id = uuid4().hex  # Set invalid ID

        with pytest.raises(NotFoundException):
            als.wait_until_completed()


class TestDeleteAlsPointCloud:
    def test_delete_existing_als(self, test_pointclouds):
        """Tests deleting an existing ALS point cloud"""
        # Create ALS
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])

        # Delete it
        als.delete()

        # Verify it was deleted via direct get
        # Note: The API might return 404 for the sub-resource or return null
        # Assuming standard behavior where GET /als returns 404 if deleted
        with pytest.raises(NotFoundException):
            als.get()

        # Parent PointClouds should reflect deletion after refresh
        test_pointclouds.get(in_place=True)
        assert test_pointclouds.als is None

    def test_delete_nonexistent_als(self, test_pointclouds):
        """Test deleting an ALS resource that doesn't exist"""
        als = test_pointclouds.create_als_point_cloud(sources=["3DEP"])
        als.domain_id = uuid4().hex  # Set invalid ID

        with pytest.raises(NotFoundException):
            als.delete()
