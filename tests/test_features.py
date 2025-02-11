"""
test_features.py
"""

# Core imports
from uuid import uuid4
from datetime import datetime

# Internal imports
from tests.utils import create_default_domain, normalize_datetime
from fastfuels_sdk.features import Features, RoadFeature, WaterFeature
from fastfuels_sdk.client_library.models import RoadFeatureSource, WaterFeatureSource
from fastfuels_sdk.client_library.exceptions import NotFoundException

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
def test_features(test_domain):
    """Fixture that creates a test features object to be used by the tests"""
    features = Features.from_domain_id(test_domain.id)

    # Return the features for use in tests
    yield features
    # Cleanup handled by test_domain fixture


class TestFeaturesFromDomain:
    def test_success(self, test_domain):
        """Test successful retrieval of features from a domain"""
        # Get features using domain
        features = Features.from_domain_id(test_domain.id)

        # Verify basic structure and domain relationship
        assert features is not None
        assert isinstance(features, Features)
        assert features.domain_id == test_domain.id

        # Optionally verify road/water features if present
        if features.road:
            assert features.road.features is not None
        if features.water:
            assert features.water.features is not None

    def test_bad_domain_id(self, test_domain):
        """Test error handling for a non-existent domain ID"""
        bad_test_domain = test_domain.model_copy(deep=True)
        bad_test_domain.id = uuid4().hex
        with pytest.raises(NotFoundException):
            Features.from_domain_id(bad_test_domain.id)


class TestGetFeatures:
    def test_get_update_default(self, test_features):
        """Test get() returns new instance with updated data by default"""
        original_features = test_features
        updated_features = original_features.get()

        # Verify new instance returned
        assert updated_features is not original_features

        # Verify data matches
        assert updated_features.domain_id == original_features.domain_id
        if original_features.road:
            assert updated_features.road is not None
            assert updated_features.road.features == original_features.road.features
        if original_features.water:
            assert updated_features.water is not None
            assert updated_features.water.features == original_features.water.features

    def test_get_update_in_place(self, test_features):
        """Test get(in_place=True) updates existing instance"""
        features = test_features
        result = features.get(in_place=True)

        # Verify same instance returned
        assert result is features

        # Verify instance was updated
        assert isinstance(result, Features)
        assert result.domain_id == test_features.domain_id
        if test_features.road:
            assert result.road is not None
            assert result.road.features == test_features.road.features
        if test_features.water:
            assert result.water is not None
            assert result.water.features == test_features.water.features

    def test_get_nonexistent_domain(self, test_features):
        """Test error handling when domain no longer exists"""
        # Store original domain_id
        original_id = test_features.domain_id

        # Set invalid domain_id
        test_features.domain_id = uuid4().hex

        # Verify exception raised
        with pytest.raises(NotFoundException):
            test_features.get()

        # Restore original domain_id
        test_features.domain_id = original_id


class TestCreateRoadFeature:
    @staticmethod
    def assert_data_validity(road_feature, domain_id):
        """Validates the basic road feature data"""
        assert road_feature is not None
        assert isinstance(road_feature, RoadFeature)
        assert road_feature.domain_id == domain_id
        assert road_feature.status in ["pending", "running", "completed"]
        assert isinstance(road_feature.checksum, str) and len(road_feature.checksum) > 0

    @pytest.mark.parametrize(
        "source",
        ["OSM", ["OSM"], RoadFeatureSource.OSM, [RoadFeatureSource.OSM]],
        ids=["str", "str-list", "enum", "enum-list"],
    )
    def test_create_with_different_source_types(self, test_features, source):
        """Tests road feature creation with different source types"""
        road_feature = test_features.create_road_feature(sources=source)

        self.assert_data_validity(road_feature, test_features.domain_id)
        assert (
            road_feature.sources == [source]
            if isinstance(source, (str, RoadFeatureSource))
            else source
        )
        # Original features object should be unchanged
        assert test_features.road is not road_feature

    def test_create_in_place_true(self, test_features):
        """Test road feature creation with in_place=True"""
        road_feature = test_features.create_road_feature(sources="OSM", in_place=True)

        self.assert_data_validity(road_feature, test_features.domain_id)
        # Features object should be updated
        assert test_features.road is road_feature
        assert test_features.road.status in ["pending", "running", "completed"]

    def test_create_nonexistent_domain(self, test_features):
        """Test error handling for non-existent domain"""
        bad_features = test_features.model_copy(deep=True)
        bad_features.domain_id = uuid4().hex

        with pytest.raises(NotFoundException):
            bad_features.create_road_feature(sources="OSM")


class TestCreateRoadFeatureFromOSM:
    def test_create_default(self, test_features):
        """Test basic OSM road feature creation"""
        road_feature = test_features.create_road_feature_from_osm()

        assert road_feature is not None
        assert isinstance(road_feature, RoadFeature)
        assert road_feature.status in ["pending", "running", "completed"]
        assert "OSM" in [str(s.value) for s in road_feature.sources]
        # Original features object should be unchanged
        assert test_features.road is not road_feature

    def test_create_in_place(self, test_features):
        """Test OSM road feature creation with in_place=True"""
        road_feature = test_features.create_road_feature_from_osm(in_place=True)

        assert road_feature is not None
        assert isinstance(road_feature, RoadFeature)
        # Features object should be updated
        assert test_features.road is road_feature
        assert test_features.road.status in ["pending", "running", "completed"]

    def test_create_nonexistent_domain(self, test_features):
        """Test error handling for non-existent domain"""
        bad_features = test_features.model_copy(deep=True)
        bad_features.domain_id = uuid4().hex

        with pytest.raises(NotFoundException):
            bad_features.create_road_feature_from_osm()


class TestCreateWaterFeature:
    @staticmethod
    def assert_data_validity(water_feature, domain_id):
        """Validates the basic water feature data"""
        assert water_feature is not None
        assert isinstance(water_feature, WaterFeature)
        assert water_feature.domain_id == domain_id
        assert water_feature.status in ["pending", "running", "completed"]
        assert (
            isinstance(water_feature.checksum, str) and len(water_feature.checksum) > 0
        )

    @pytest.mark.parametrize(
        "source",
        ["OSM", ["OSM"], WaterFeatureSource.OSM, [WaterFeatureSource.OSM]],
        ids=["str", "str-list", "enum", "enum-list"],
    )
    def test_create_with_different_source_types(self, test_features, source):
        """Tests water feature creation with different source types"""
        water_feature = test_features.create_water_feature(sources=source)

        self.assert_data_validity(water_feature, test_features.domain_id)
        assert (
            water_feature.sources == [source]
            if isinstance(source, (str, WaterFeatureSource))
            else source
        )
        # Original features object should be unchanged
        assert test_features.water is not water_feature

    def test_create_in_place_true(self, test_features):
        """Test water feature creation with in_place=True"""
        water_feature = test_features.create_water_feature(sources="OSM", in_place=True)

        self.assert_data_validity(water_feature, test_features.domain_id)
        # Features object should be updated
        assert test_features.water is water_feature
        assert test_features.water.status in ["pending", "running", "completed"]

    def test_create_nonexistent_domain(self, test_features):
        """Test error handling for non-existent domain"""
        bad_features = test_features.model_copy(deep=True)
        bad_features.domain_id = uuid4().hex

        with pytest.raises(NotFoundException):
            bad_features.create_water_feature(sources="OSM")


class TestCreateWaterFeatureFromOSM:
    def test_create_default(self, test_features):
        """Test basic OSM water feature creation"""
        water_feature = test_features.create_water_feature_from_osm()

        assert water_feature is not None
        assert isinstance(water_feature, WaterFeature)
        assert water_feature.status in ["pending", "running", "completed"]
        assert "OSM" in [str(s.value) for s in water_feature.sources]
        # Original features object should be unchanged
        assert test_features.water is not water_feature

    def test_create_in_place(self, test_features):
        """Test OSM water feature creation with in_place=True"""
        water_feature = test_features.create_water_feature_from_osm(in_place=True)

        assert water_feature is not None
        assert isinstance(water_feature, WaterFeature)
        # Features object should be updated
        assert test_features.water is water_feature
        assert test_features.water.status in ["pending", "running", "completed"]

    def test_create_nonexistent_domain(self, test_features):
        """Test error handling for non-existent domain"""
        bad_features = test_features.model_copy(deep=True)
        bad_features.domain_id = uuid4().hex

        with pytest.raises(NotFoundException):
            bad_features.create_water_feature_from_osm()


class TestGetRoadFeature:
    def test_default(self, test_features):
        """Tests fetching road feature data returns new instance by default"""
        # First create a road feature
        road_feature = test_features.create_road_feature(sources="OSM")

        # Get latest data
        updated = road_feature.get()

        # Verify new instance returned
        assert updated is not None
        assert isinstance(updated, RoadFeature)
        assert updated is not road_feature
        assert normalize_datetime(updated) == normalize_datetime(road_feature)

    def test_in_place(self, test_features):
        """Tests fetching road feature data in place"""
        road_feature = test_features.create_road_feature(sources="OSM")
        result = road_feature.get(in_place=True)

        # Verify same instance returned and updated
        assert result is road_feature
        assert isinstance(result, RoadFeature)

    def test_in_place_with_assignment(self, test_features):
        """Tests fetching road feature data in place with assignment"""
        road_feature = test_features.create_road_feature(sources="OSM")
        new_road_feature = road_feature.get(in_place=True)

        assert new_road_feature is road_feature
        assert new_road_feature == road_feature

    def test_get_nonexistent_domain(self, test_features):
        """Test error handling when domain no longer exists"""
        road_feature = test_features.create_road_feature(sources="OSM")

        # Store original domain_id
        original_id = road_feature.domain_id

        # Set invalid domain_id
        road_feature.domain_id = uuid4().hex

        # Verify exception raised
        with pytest.raises(NotFoundException):
            road_feature.get()

        # Restore original domain_id
        road_feature.domain_id = original_id


class TestWaitUntilCompletedRoadFeature:
    def test_wait_until_completed_default(self, test_features):
        """Test waiting for road feature to complete with default settings"""
        road_feature = test_features.create_road_feature(sources="OSM")
        completed = road_feature.wait_until_completed()

        assert completed is road_feature  # In-place by default
        assert completed.status == "completed"
        assert isinstance(completed.created_on, datetime)
        assert isinstance(completed.modified_on, datetime)
        assert isinstance(completed.checksum, str)

    def test_wait_until_completed_not_in_place(self, test_features):
        """Test waiting without in-place updates"""
        road_feature = test_features.create_road_feature(sources="OSM")
        completed = road_feature.wait_until_completed(in_place=False)

        assert completed is not road_feature  # New instance
        assert completed.status == "completed"
        assert road_feature.status in [
            "pending",
            "running",
            "completed",
        ]  # Original unchanged

    def test_wait_until_completed_timeout(self, test_features):
        """Test timeout handling"""
        road_feature = test_features.create_road_feature(sources="OSM")

        with pytest.raises(TimeoutError):
            road_feature.wait_until_completed(timeout=0.1)  # Very short timeout

    def test_wait_until_completed_nonexistent_domain(self, test_features):
        """Test error handling when domain no longer exists"""
        road_feature = test_features.create_road_feature(sources="OSM")
        road_feature.domain_id = uuid4().hex  # Set invalid ID

        with pytest.raises(NotFoundException):
            road_feature.wait_until_completed()


class TestDeleteRoadFeature:
    def test_delete_existing_feature(self, test_features):
        """Tests deleting an existing road feature"""
        # Create road feature
        road_feature = test_features.create_road_feature(sources="OSM")

        # Delete it
        road_feature.delete()

        # Verify it was deleted
        with pytest.raises(NotFoundException, match="Reason: Not Found"):
            road_feature.get()

        # Features should be updated to reflect deletion
        test_features.get(in_place=True)
        assert test_features.road is None

    def test_delete_nonexistent_feature(self, test_features):
        """Test deleting a road feature that doesn't exist"""
        road_feature = test_features.create_road_feature(sources="OSM")
        road_feature.domain_id = uuid4().hex  # Set invalid ID

        with pytest.raises(NotFoundException):
            road_feature.delete()


class TestGetWaterFeature:
    def test_default(self, test_features):
        """Tests fetching water feature data returns new instance by default"""
        # First create a water feature
        water_feature = test_features.create_water_feature(sources="OSM")

        # Get latest data
        updated = water_feature.get()

        # Verify new instance returned
        assert updated is not None
        assert isinstance(updated, WaterFeature)
        assert updated is not water_feature
        assert normalize_datetime(updated) == normalize_datetime(water_feature)

    def test_in_place(self, test_features):
        """Tests fetching water feature data in place"""
        water_feature = test_features.create_water_feature(sources="OSM")
        result = water_feature.get(in_place=True)

        # Verify same instance returned and updated
        assert result is water_feature
        assert isinstance(result, WaterFeature)

    def test_in_place_with_assignment(self, test_features):
        """Tests fetching water feature data in place with assignment"""
        water_feature = test_features.create_water_feature(sources="OSM")
        new_water_feature = water_feature.get(in_place=True)

        assert new_water_feature is water_feature
        assert new_water_feature == water_feature

    def test_get_nonexistent_domain(self, test_features):
        """Test error handling when domain no longer exists"""
        water_feature = test_features.create_water_feature(sources="OSM")

        # Store original domain_id
        original_id = water_feature.domain_id

        # Set invalid domain_id
        water_feature.domain_id = uuid4().hex

        # Verify exception raised
        with pytest.raises(NotFoundException):
            water_feature.get()

        # Restore original domain_id
        water_feature.domain_id = original_id


class TestWaitUntilCompletedWaterFeature:
    def test_wait_until_completed_default(self, test_features):
        """Test waiting for water feature to complete with default settings"""
        water_feature = test_features.create_water_feature(sources="OSM")
        completed = water_feature.wait_until_completed()

        assert completed is water_feature  # In-place by default
        assert completed.status == "completed"
        assert isinstance(completed.created_on, datetime)
        assert isinstance(completed.modified_on, datetime)
        assert isinstance(completed.checksum, str)

    def test_wait_until_completed_not_in_place(self, test_features):
        """Test waiting without in-place updates"""
        water_feature = test_features.create_water_feature(sources="OSM")
        completed = water_feature.wait_until_completed(in_place=False)

        assert completed is not water_feature  # New instance
        assert completed.status == "completed"
        assert water_feature.status in [
            "pending",
            "running",
            "completed",
        ]  # Original unchanged

    def test_wait_until_completed_timeout(self, test_features):
        """Test timeout handling"""
        water_feature = test_features.create_water_feature(sources="OSM")

        with pytest.raises(TimeoutError):
            water_feature.wait_until_completed(timeout=0.1)  # Very short timeout

    def test_wait_until_completed_nonexistent_domain(self, test_features):
        """Test error handling when domain no longer exists"""
        water_feature = test_features.create_water_feature(sources="OSM")
        water_feature.domain_id = uuid4().hex  # Set invalid ID

        with pytest.raises(NotFoundException):
            water_feature.wait_until_completed()


class TestDeleteWaterFeature:
    def test_delete_existing_feature(self, test_features):
        """Tests deleting an existing water feature"""
        # Create water feature
        water_feature = test_features.create_water_feature(sources="OSM")

        # Delete it
        water_feature.delete()

        # Verify it was deleted
        with pytest.raises(NotFoundException, match="Reason: Not Found"):
            water_feature.get()

        # Features should be updated to reflect deletion
        test_features.get(in_place=True)
        assert test_features.water is None

    def test_delete_nonexistent_feature(self, test_features):
        """Test deleting a water feature that doesn't exist"""
        water_feature = test_features.create_water_feature(sources="OSM")
        water_feature.domain_id = uuid4().hex  # Set invalid ID

        with pytest.raises(NotFoundException):
            water_feature.delete()
