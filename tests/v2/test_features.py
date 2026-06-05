"""
tests/v2/test_features.py
"""

# Core imports
import json
from uuid import uuid4

# Internal imports
from tests import TEST_DATA_DIR
from tests.v2.utils import create_default_layerset_geojson
from fastfuels_sdk.v2.features import Feature, list_features
from fastfuels_sdk.v2.client_library.models import FeatureType, JobStatus
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

# External imports
import pytest
import geopandas as gpd

# The test_domain, road_feature, and layerset_feature fixtures are
# session-scoped and shared across modules (tests/v2/conftest.py).
# They are READ-ONLY: tests that mutate or delete create throwaways.


class TestCreateOsmRoadFeature:
    def test_create(self, test_domain):
        feature = Feature.create_osm_road(test_domain.id, name="throwaway_road")

        # Feature generation is an asynchronous job
        assert len(feature.id) > 0
        assert feature.domain_id == test_domain.id
        assert feature.type_ == FeatureType.ROAD
        assert feature.status in (JobStatus.PENDING, JobStatus.RUNNING)
        assert feature.source.additional_properties["product"] == "osm"
        feature.delete()

    def test_completed_fixture(self, test_domain, road_feature):
        assert road_feature.status == JobStatus.COMPLETED
        assert road_feature.name == "test_road"
        assert road_feature.tags == ["test"]
        # The georeference is populated once the job completes
        assert road_feature.georeference.crs.startswith("EPSG:")
        assert len(road_feature.georeference.bounds) == 4

    def test_invalid_extent_buffer(self, test_domain):
        with pytest.raises(UnprocessableEntityException):
            Feature.create_osm_road(test_domain.id, extent_buffer_m=500)


class TestCreateOsmWaterFeature:
    def test_create(self, test_domain):
        feature = Feature.create_osm_water(test_domain.id, name="throwaway_water")

        assert len(feature.id) > 0
        assert feature.domain_id == test_domain.id
        assert feature.type_ == FeatureType.WATER
        assert feature.status in (JobStatus.PENDING, JobStatus.RUNNING)
        feature.delete()


class TestCreateLayerset:
    def test_create(self, test_domain, layerset_feature):
        # Layerset uploads are synchronous: the feature is already complete
        assert layerset_feature.domain_id == test_domain.id
        assert layerset_feature.type_ == FeatureType.LAYERSET
        assert layerset_feature.status == JobStatus.COMPLETED
        assert layerset_feature.name == "test_layerset"

    def test_single_feature_is_wrapped(self, test_domain):
        layerset_geojson = create_default_layerset_geojson()
        feature_geojson = layerset_geojson["features"][0]
        feature_geojson["crs"] = layerset_geojson["crs"]

        feature = Feature.create_layerset(test_domain.id, feature_geojson)
        assert feature.status == JobStatus.COMPLETED
        feature.delete()

    def test_geographic_crs_rejected(self, test_domain):
        # Layersets require a projected CRS; blue_mtn is EPSG:4326
        with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
            geojson = json.load(f)
        for feature in geojson["features"]:
            feature["properties"] = create_default_layerset_geojson()["features"][0][
                "properties"
            ]

        with pytest.raises(UnprocessableEntityException, match="geographic"):
            Feature.create_layerset(test_domain.id, geojson)

    def test_invalid_geojson_type(self, test_domain):
        with pytest.raises(ValueError, match="FeatureCollection"):
            Feature.create_layerset(
                test_domain.id, {"type": "Point", "coordinates": [0, 0]}
            )


class TestCreateLayersetFromGeodataframe:
    def test_create(self, test_domain):
        # The GeoDataFrame carries the projected CRS and the fuelbed
        # property columns; both are forwarded to the API
        gdf = gpd.read_file(json.dumps(create_default_layerset_geojson()))
        assert gdf.crs.is_projected

        feature = Feature.create_layerset_from_geodataframe(
            test_domain.id, gdf, name="gdf_layerset"
        )
        assert feature.type_ == FeatureType.LAYERSET
        assert feature.status == JobStatus.COMPLETED
        assert feature.get_data_metadata().total_features == len(gdf)
        feature.delete()


class TestFromId:
    def test_success(self, test_domain, road_feature):
        feature = Feature.from_id(test_domain.id, road_feature.id)
        assert feature.id == road_feature.id
        assert feature.domain_id == test_domain.id
        assert feature.type_ == FeatureType.ROAD

    def test_not_found(self, test_domain):
        with pytest.raises(NotFoundException):
            Feature.from_id(test_domain.id, uuid4().hex)


class TestGetFeature:
    def test_get_default(self, road_feature):
        feature = road_feature.get()
        assert feature.id == road_feature.id
        assert feature is not road_feature

    def test_get_in_place(self, road_feature):
        feature = road_feature.get(in_place=True)
        assert feature is road_feature


class TestWaitUntilCompleted:
    def test_timeout(self, test_domain):
        feature = Feature.create_osm_water(test_domain.id)
        with pytest.raises(TimeoutError):
            feature.wait_until_completed(timeout=0)
        feature.delete()


class TestGetDataMetadata:
    def test_metadata(self, road_feature):
        metadata = road_feature.get_data_metadata()

        assert metadata.total_features > 0
        assert metadata.partition_count >= 1
        assert len(metadata.partitions) == metadata.partition_count
        assert (
            sum(partition.num_features for partition in metadata.partitions)
            == metadata.total_features
        )

    def test_not_completed(self, test_domain):
        # Data is only available once the job is complete
        feature = Feature.create_osm_road(test_domain.id)
        with pytest.raises(UnprocessableEntityException, match="status"):
            feature.get_data_metadata()
        feature.delete()


class TestGetDataPartition:
    def test_partition(self, road_feature):
        metadata = road_feature.get_data_metadata()
        partition = road_feature.get_data_partition(0)

        assert partition["type"] == "FeatureCollection"
        assert len(partition["features"]) == metadata.partitions[0].num_features
        assert "crs" in partition

    def test_partition_out_of_range(self, road_feature):
        metadata = road_feature.get_data_metadata()
        with pytest.raises(UnprocessableEntityException, match="out of range"):
            road_feature.get_data_partition(metadata.partition_count)


class TestGetData:
    def test_get_data(self, road_feature):
        metadata = road_feature.get_data_metadata()
        data = road_feature.get_data()

        assert data["type"] == "FeatureCollection"
        assert len(data["features"]) == metadata.total_features
        assert "crs" in data


class TestToGeodataframe:
    def test_to_geodataframe(self, road_feature):
        metadata = road_feature.get_data_metadata()
        gdf = road_feature.to_geodataframe()

        assert len(gdf) == metadata.total_features
        # The data comes back in the projected CRS reported by the
        # feature's georeference
        assert ":".join(gdf.crs.to_authority()) == road_feature.georeference.crs


class TestListFeatures:
    def test_list_in_domain(self, test_domain, road_feature, layerset_feature):
        features = list_features(test_domain.id)
        feature_ids = [feature.id for feature in features]
        assert road_feature.id in feature_ids
        assert layerset_feature.id in feature_ids

    def test_list_cross_domain(self, road_feature):
        # No domain_id: list features across all the user's domains
        features = list_features()
        assert road_feature.id in [feature.id for feature in features]

    def test_filter_by_type(self, test_domain, road_feature, layerset_feature):
        features = list_features(test_domain.id, feature_type="road")
        feature_ids = [feature.id for feature in features]
        assert all(feature.type_ == FeatureType.ROAD for feature in features)
        assert road_feature.id in feature_ids
        assert layerset_feature.id not in feature_ids

    def test_filter_by_product(self, test_domain, road_feature, layerset_feature):
        features = list_features(test_domain.id, product="osm")
        feature_ids = [feature.id for feature in features]
        assert road_feature.id in feature_ids
        assert layerset_feature.id not in feature_ids

    def test_filter_by_tag(self, test_domain, layerset_feature):
        features = list_features(test_domain.id, tag="layerset-test")
        assert [feature.id for feature in features] == [layerset_feature.id]

    @pytest.mark.xfail(
        reason="v2 API returns 500 for feature sort_by combinations; "
        "see FastFuels-API-v2#321",
    )
    def test_sorting(self, test_domain, road_feature):
        features = list_features(
            test_domain.id, sort_by="created_on", sort_order="descending"
        )
        assert len(features) > 0

    def test_invalid_sort_field(self):
        with pytest.raises(ValueError):
            list_features(sort_by="not_a_field")

    def test_invalid_feature_type(self):
        with pytest.raises(ValueError):
            list_features(feature_type="not_a_type")


class TestUpdateFeature:
    @pytest.fixture(scope="class")
    def update_feature(self, test_domain):
        """A throwaway feature to mutate (the shared fixtures are read-only)."""
        feature = Feature.create_layerset(
            test_domain.id, create_default_layerset_geojson(), name="update_target"
        )
        yield feature
        feature.delete()

    def test_update_name(self, test_domain, update_feature):
        updated = update_feature.update(name="updated_name")
        assert updated.name == "updated_name"
        assert updated is not update_feature
        # The remote resource reflects the update
        assert Feature.from_id(test_domain.id, update_feature.id).name == "updated_name"

    def test_update_in_place(self, update_feature):
        updated = update_feature.update(
            description="updated description", in_place=True
        )
        assert updated is update_feature
        assert update_feature.description == "updated description"

    def test_update_tags(self, update_feature):
        updated = update_feature.update(tags=["updated"], in_place=True)
        assert updated.tags == ["updated"]

    def test_update_no_fields_makes_no_api_call(self, update_feature):
        # No fields provided: returns a copy without touching the API
        copy = update_feature.update()
        assert copy is not update_feature
        assert copy.id == update_feature.id
        assert update_feature.update(in_place=True) is update_feature


class TestToJson:
    def test_to_json(self, road_feature):
        feature_dict = json.loads(road_feature.to_json())
        assert feature_dict["id"] == road_feature.id
        assert feature_dict["domain_id"] == road_feature.domain_id
        assert feature_dict["type"] == "road"


class TestDeleteFeature:
    def test_delete_feature(self, test_domain):
        feature = Feature.create_osm_water(test_domain.id)
        feature.delete()

        with pytest.raises(NotFoundException):
            Feature.from_id(test_domain.id, feature.id)

        with pytest.raises(NotFoundException):
            feature.delete()
