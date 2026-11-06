"""
tests/v2/test_features.py
"""

# Core imports
import json
from types import SimpleNamespace
from http import HTTPStatus
from uuid import uuid4

# Internal imports
from tests import TEST_DATA_DIR
from tests.v2.utils import create_default_layerset_geojson
from fastfuels_sdk.v2.features import (
    Feature,
    concatenate_building_features,
    concatenate_road_features,
    concatenate_water_features,
    create_building_feature_from_geodataframe,
    create_building_feature_from_geojson,
    create_building_feature_from_overture,
    create_crown_feature_from_chm,
    create_layerset_feature_from_geodataframe,
    create_layerset_feature_from_geojson,
    create_road_feature_from_geodataframe,
    create_road_feature_from_geojson,
    create_road_feature_from_osm,
    create_water_feature_from_geodataframe,
    create_water_feature_from_geojson,
    create_water_feature_from_osm,
    get_feature,
    list_features,
)
from fastfuels_sdk.v2.client_library.models import (
    ChmCrownSegmentation,
    FeatureType,
    JobStatus,
)
from fastfuels_sdk.v2.client_library.types import Response
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

# External imports
import pytest
import geopandas as gpd
from shapely.geometry import box

# The test_domain, completed_road_feature, and layerset_feature fixtures are
# session-scoped and shared across modules (tests/v2/conftest.py).
# They are READ-ONLY: tests that mutate or delete create throwaways.


class TestCreateOsmRoadFeature:
    def test_create(self, test_domain):
        feature = create_road_feature_from_osm(test_domain, name="throwaway_road")

        # Feature generation is an asynchronous job
        assert len(feature.id) > 0
        assert feature.domain_id == test_domain.id
        assert feature.type_ == FeatureType.ROAD
        assert feature.status in (JobStatus.PENDING, JobStatus.RUNNING)
        assert feature.source.additional_properties["product"] == "osm"
        feature.delete()

    def test_completed_fixture(self, test_domain, completed_road_feature):
        assert completed_road_feature.status == JobStatus.COMPLETED
        assert completed_road_feature.name == "test_road"
        assert completed_road_feature.tags == ["test"]
        # The georeference is populated once the job completes
        assert completed_road_feature.georeference.crs.startswith("EPSG:")
        assert len(completed_road_feature.georeference.bounds) == 4

    def test_invalid_extent_buffer(self, test_domain):
        with pytest.raises(UnprocessableEntityException):
            create_road_feature_from_osm(test_domain, extent_buffer_m=500)


class TestCreateOsmWaterFeature:
    def test_create(self, test_domain):
        feature = create_water_feature_from_osm(test_domain, name="throwaway_water")

        assert len(feature.id) > 0
        assert feature.domain_id == test_domain.id
        assert feature.type_ == FeatureType.WATER
        assert feature.status in (JobStatus.PENDING, JobStatus.RUNNING)
        feature.delete()


def _building_feature_payload(domain_id="domain-id", status="completed"):
    return {
        "id": "feature-id",
        "domain_id": domain_id,
        "type": "building",
        "status": status,
        "source": {
            "description": "Overture Maps building footprints",
            "product": "overture",
            "extent_buffer_m": 0.0,
            "release": "2026-10-21.0",
        },
        "name": "",
        "description": "",
        "attributions": [
            {
                "dataset": "Overture Maps Foundation",
                "license_name": "ODbL-1.0",
                "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
                "citation": "\u00a9 OpenStreetMap contributors, Overture Maps Foundation",
                "access_url": "https://docs.overturemaps.org/attribution/",
                "accessed_on": "2026-11-05",
            }
        ],
    }


class TestBuildingFeatureParsing:
    def test_building_type_parses(self):
        feature = Feature.from_dict(_building_feature_payload())
        assert isinstance(feature, Feature)
        assert feature.type_ == FeatureType.BUILDING
        assert feature.source["product"] == "overture"
        assert feature.source["release"] == "2026-10-21.0"

    def test_attributions_parse(self):
        feature = Feature.from_dict(_building_feature_payload())
        (attribution,) = feature.attributions
        assert attribution.dataset == "Overture Maps Foundation"
        assert attribution.license_name == "ODbL-1.0"
        assert "OpenStreetMap contributors" in attribution.citation


class TestCreateBuildingFeatureFromOvertureRequest:
    @pytest.fixture
    def captured(self, monkeypatch):
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, body=body.to_dict())
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=Feature.from_dict(
                    _building_feature_payload(domain_id, status="pending")
                ),
            )

        monkeypatch.setattr("fastfuels_sdk.v2.features.ensure_client", lambda: object())
        monkeypatch.setattr(
            "fastfuels_sdk.v2.features.create_overture_building_feature.sync_detailed",
            fake_create,
        )
        return captured

    def test_default_request_body(self, captured):
        feature = create_building_feature_from_overture("domain-id")

        assert isinstance(feature, Feature)
        assert feature.type_ == FeatureType.BUILDING
        assert captured["domain_id"] == "domain-id"
        assert captured["body"] == {
            "type": "building",
            "name": "",
            "description": "",
            "extent_buffer_m": 0.0,
        }

    def test_full_request_body(self, captured):
        create_building_feature_from_overture(
            SimpleNamespace(id="domain-obj"),
            name="buildings",
            description="footprints",
            tags=["wui"],
            extent_buffer_m=25,
        )

        assert captured["domain_id"] == "domain-obj"
        assert captured["body"] == {
            "type": "building",
            "name": "buildings",
            "description": "footprints",
            "tags": ["wui"],
            "extent_buffer_m": 25,
        }


class TestCreateOvertureBuildingFeature:
    def test_create(self, building_domain):
        feature = create_building_feature_from_overture(
            building_domain, name="throwaway_buildings"
        )

        assert len(feature.id) > 0
        assert feature.domain_id == building_domain.id
        assert feature.type_ == FeatureType.BUILDING
        assert feature.status in (JobStatus.PENDING, JobStatus.RUNNING)
        assert feature.source["product"] == "overture"
        feature.delete()

    def test_invalid_extent_buffer(self, building_domain):
        with pytest.raises(UnprocessableEntityException):
            create_building_feature_from_overture(building_domain, extent_buffer_m=500)

    def test_completed_fixture(self, completed_building_feature):
        feature = completed_building_feature
        assert feature.status == JobStatus.COMPLETED
        assert feature.name == "test_buildings"
        assert feature.tags == ["test"]
        # The Overture release that was read is recorded once processed
        assert feature.source["release"]
        assert feature.georeference.crs.startswith("EPSG:")
        assert any(
            "Overture" in attribution.dataset for attribution in feature.attributions
        )

    def test_data_columns(self, completed_building_feature):
        gdf = completed_building_feature.to_geodataframe()

        assert len(gdf) > 0
        assert {"geometry", "height", "height_source", "source_dataset"} <= set(
            gdf.columns
        )
        assert gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"]).all()
        # Every footprint names its source dataset; height (and so its
        # source) may be unknown for some buildings
        assert gdf["source_dataset"].notna().all()
        heights = gdf["height"].dropna()
        assert len(heights) > 0
        assert (heights > 0).all()
        assert gdf.loc[gdf["height"].notna(), "height_source"].notna().all()

    def test_get_and_list(self, building_domain, completed_building_feature):
        # A building feature in a response deserializes (FeatureType.BUILDING)
        feature = get_feature(building_domain, completed_building_feature.id)
        assert feature.type_ == FeatureType.BUILDING

        features = list_features(building_domain)
        assert completed_building_feature.id in [f.id for f in features]

        buildings = list_features(building_domain, feature_type="building")
        assert all(f.type_ == FeatureType.BUILDING for f in buildings)
        assert completed_building_feature.id in [f.id for f in buildings]


def _crown_feature_payload(domain_id="domain-id", status="pending"):
    return {
        "id": "feature-id",
        "domain_id": domain_id,
        "type": "crown",
        "status": status,
        "source": {
            "name": "chm",
            "source_inventory_id": "inventory-id",
            "source_chm_grid_id": "chm-id",
        },
        "name": "",
        "description": "",
    }


class TestCreateCrownFeatureFromChmRequest:
    @pytest.fixture
    def captured(self, monkeypatch):
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, body=body.to_dict())
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=Feature.from_dict(_crown_feature_payload(domain_id)),
            )

        monkeypatch.setattr("fastfuels_sdk.v2.features.ensure_client", lambda: object())
        monkeypatch.setattr(
            "fastfuels_sdk.v2.features.create_chm_crown_feature.sync_detailed",
            fake_create,
        )
        return captured

    def test_minimal_request_body(self, captured):
        feature = create_crown_feature_from_chm("domain-id", "inventory-id", "chm-id")

        assert isinstance(feature, Feature)
        assert feature.type_ == FeatureType.CROWN
        assert captured["domain_id"] == "domain-id"
        assert captured["body"] == {
            "source_inventory_id": "inventory-id",
            "source_chm_grid_id": "chm-id",
            "type": "crown",
            "name": "",
            "description": "",
        }

    def test_accepts_resource_objects(self, captured):
        domain = type("D", (), {"id": "domain-id"})()
        inventory = type("I", (), {"id": "inventory-id"})()
        grid = type("G", (), {"id": "chm-id"})()

        create_crown_feature_from_chm(domain, inventory, grid, tags=["t"])

        assert captured["domain_id"] == "domain-id"
        assert captured["body"]["source_inventory_id"] == "inventory-id"
        assert captured["body"]["source_chm_grid_id"] == "chm-id"
        assert captured["body"]["tags"] == ["t"]

    def test_segmentation_mapping_sends_only_given_fields(self, captured):
        create_crown_feature_from_chm(
            "domain-id",
            "inventory-id",
            "chm-id",
            crown_segmentation={"max_crown_radius": 6.0, "method": "dalponte2016"},
        )

        assert captured["body"]["crown_segmentation"] == {
            "method": "dalponte2016",
            "max_crown_radius": 6.0,
        }

    def test_segmentation_model(self, captured):
        create_crown_feature_from_chm(
            "domain-id",
            "inventory-id",
            "chm-id",
            crown_segmentation=ChmCrownSegmentation(max_height=None),
        )

        segmentation = captured["body"]["crown_segmentation"]
        assert segmentation["max_height"] is None
        assert segmentation["max_crown_radius"] == 10.0

    def test_rejects_other_segmentation_types(self, captured):
        with pytest.raises(ValueError, match="ChmCrownSegmentation"):
            create_crown_feature_from_chm(
                "domain-id", "inventory-id", "chm-id", crown_segmentation=True
            )
        assert captured == {}


class TestCrownFeatureParsing:
    def test_crown_type_parses(self):
        feature = Feature.from_dict(_crown_feature_payload(status="completed"))
        assert feature.type_ == FeatureType.CROWN
        assert feature.source["source_chm_grid_id"] == "chm-id"


class TestCreateCrownFeatureFromChm:
    def test_completed_fixture(self, test_domain, completed_crown_feature):
        assert completed_crown_feature.domain_id == test_domain.id
        assert completed_crown_feature.type_ == FeatureType.CROWN
        assert completed_crown_feature.status == JobStatus.COMPLETED

    def test_data_has_tree_id_and_geometry(self, completed_crown_feature):
        gdf = completed_crown_feature.to_geodataframe()
        assert len(gdf) > 0
        assert "tree_id" in gdf.columns
        assert gdf.geometry.geom_type.isin(["Polygon"]).all()
        assert gdf["tree_id"].is_unique

    def test_get_and_list(self, test_domain, completed_crown_feature):
        feature = get_feature(test_domain, completed_crown_feature.id)
        assert feature.type_ == FeatureType.CROWN

        features = list_features(test_domain, feature_type="crown")
        assert completed_crown_feature.id in [f.id for f in features]
        assert all(f.type_ == FeatureType.CROWN for f in features)

    def test_inventory_from_other_source_rejected(
        self, test_domain, completed_tree_inventory, completed_fine_chm_grid
    ):
        # A PIM-expanded inventory was not detected from the CHM grid
        with pytest.raises(UnprocessableEntityException, match="not detected"):
            create_crown_feature_from_chm(
                test_domain, completed_tree_inventory, completed_fine_chm_grid
            )

    def test_missing_inventory(self, test_domain, completed_fine_chm_grid):
        with pytest.raises(NotFoundException):
            create_crown_feature_from_chm(
                test_domain, uuid4().hex, completed_fine_chm_grid
            )


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

        feature = create_layerset_feature_from_geojson(test_domain, feature_geojson)
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
            create_layerset_feature_from_geojson(test_domain, geojson)

    def test_invalid_geojson_type(self, test_domain):
        with pytest.raises(ValueError, match="FeatureCollection"):
            create_layerset_feature_from_geojson(
                test_domain, {"type": "Point", "coordinates": [0, 0]}
            )


class TestCreateLayersetFromGeodataframe:
    def test_create(self, test_domain):
        # The GeoDataFrame carries the projected CRS and the fuelbed
        # property columns; both are forwarded to the API
        gdf = gpd.read_file(json.dumps(create_default_layerset_geojson()))
        assert gdf.crs.is_projected

        feature = create_layerset_feature_from_geodataframe(
            test_domain, gdf, name="gdf_layerset"
        )
        assert feature.type_ == FeatureType.LAYERSET
        assert feature.status == JobStatus.COMPLETED
        assert feature.get_data_metadata().total_features == len(gdf)
        feature.delete()


# (feature type, upload from GeoJSON, upload from GeoDataFrame, concatenate)
UPLOADABLE_TYPES = [
    pytest.param(
        FeatureType.ROAD,
        create_road_feature_from_geojson,
        create_road_feature_from_geodataframe,
        concatenate_road_features,
        id="road",
    ),
    pytest.param(
        FeatureType.WATER,
        create_water_feature_from_geojson,
        create_water_feature_from_geodataframe,
        concatenate_water_features,
        id="water",
    ),
    pytest.param(
        FeatureType.BUILDING,
        create_building_feature_from_geojson,
        create_building_feature_from_geodataframe,
        concatenate_building_features,
        id="building",
    ),
]


@pytest.fixture(scope="module")
def domain_polygons(test_domain):
    """Two polygons inside the test domain, in the domain's CRS, with a
    ``label`` property column.
    """
    domain_gdf = test_domain.to_geodataframe()
    minx, miny, maxx, maxy = domain_gdf.total_bounds
    midx, midy = (minx + maxx) / 2, (miny + maxy) / 2
    return gpd.GeoDataFrame(
        {"label": ["southwest", "northeast"]},
        geometry=[
            box(minx + 10, miny + 10, midx - 10, midy - 10),
            box(midx + 10, midy + 10, maxx - 10, maxy - 10),
        ],
        crs=domain_gdf.crs,
    )


def _uploaded_feature_payload(feature_type, product, domain_id="domain-id"):
    return {
        "id": "feature-id",
        "domain_id": domain_id,
        "type": feature_type,
        "status": "completed",
        "source": {"product": product},
        "name": "",
        "description": "",
    }


class TestUploadAndConcatenateRequests:
    @pytest.fixture
    def captured(self, monkeypatch):
        captured = {}

        def fake_endpoint(feature_type, product):
            def fake(domain_id, *, client, body):
                captured.update(domain_id=domain_id, body=body.to_dict())
                return Response(
                    status_code=HTTPStatus.CREATED,
                    content=b"",
                    headers={},
                    parsed=Feature.from_dict(
                        _uploaded_feature_payload(feature_type, product, domain_id)
                    ),
                )

            return fake

        monkeypatch.setattr("fastfuels_sdk.v2.features.ensure_client", lambda: object())
        monkeypatch.setattr(
            "fastfuels_sdk.v2.features.create_geojson_water_feature.sync_detailed",
            fake_endpoint("water", "geojson"),
        )
        monkeypatch.setattr(
            "fastfuels_sdk.v2.features.concatenate_road_features_endpoint.sync_detailed",
            fake_endpoint("road", "concatenate"),
        )
        return captured

    def test_geodataframe_crs_sent_as_crs_member(self, captured):
        gdf = gpd.GeoDataFrame(
            {"depth": [1.5]}, geometry=[box(0, 0, 10, 10)], crs="EPSG:32611"
        )
        create_water_feature_from_geodataframe(
            "domain-id", gdf, name="lakes", tags=["t"], extent_buffer_m=5
        )

        body = captured["body"]
        assert body["crs"] == {"type": "name", "properties": {"name": "EPSG:32611"}}
        assert body["name"] == "lakes"
        assert body["tags"] == ["t"]
        assert body["extent_buffer_m"] == 5
        assert body["features"][0]["properties"] == {"depth": 1.5}

    def test_concatenate_accepts_features_and_ids(self, captured):
        first = Feature.from_dict(_uploaded_feature_payload("road", "geojson"))
        first.id = "first-id"

        feature = concatenate_road_features(
            SimpleNamespace(id="domain-obj"), [first, "second-id"]
        )

        assert feature.type_ == FeatureType.ROAD
        assert captured["domain_id"] == "domain-obj"
        assert captured["body"] == {
            "source_feature_ids": ["first-id", "second-id"],
            "name": "",
            "description": "",
        }

    def test_non_polygon_geometry_rejected(self, captured):
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                    "properties": None,
                }
            ],
        }
        with pytest.raises(ValueError):
            create_water_feature_from_geojson("domain-id", geojson)
        assert captured == {}


class TestCreateFeatureFromGeojson:
    @pytest.mark.parametrize(
        "feature_type, from_geojson, from_geodataframe, concatenate", UPLOADABLE_TYPES
    )
    def test_create(
        self,
        test_domain,
        domain_polygons,
        feature_type,
        from_geojson,
        from_geodataframe,
        concatenate,
    ):
        # WGS84 coordinates with no crs member: the API reads them as
        # EPSG:4326 and reprojects them to the domain CRS
        geojson = json.loads(domain_polygons.to_crs(4326).to_json())
        geojson.pop("crs", None)

        feature = from_geojson(
            test_domain, geojson, name="uploaded", tags=["upload-test"]
        )

        # Uploads are synchronous: the feature is already complete
        assert feature.domain_id == test_domain.id
        assert feature.type_ == feature_type
        assert feature.status == JobStatus.COMPLETED
        assert feature.name == "uploaded"
        assert feature.tags == ["upload-test"]
        assert feature.source["product"] == "geojson"

        gdf = feature.to_geodataframe()
        assert len(gdf) == 2
        assert sorted(gdf["label"]) == ["northeast", "southwest"]
        assert gdf.crs == domain_polygons.crs
        feature.delete()

    def test_clipped_to_buffered_domain(self, test_domain, domain_polygons):
        minx, miny, maxx, maxy = test_domain.to_geodataframe().total_bounds
        crossing = gpd.GeoDataFrame(
            geometry=[box(minx - 500, miny - 500, maxx + 500, maxy + 500)],
            crs=domain_polygons.crs,
        )
        # An explicit crs member in the domain's projected CRS
        geojson = json.loads(crossing.to_json())
        geojson["crs"] = {
            "type": "name",
            "properties": {"name": ":".join(crossing.crs.to_authority())},
        }

        feature = create_road_feature_from_geojson(
            test_domain, geojson, extent_buffer_m=20
        )

        assert feature.source["extent_buffer_m"] == 20
        bounds = feature.to_geodataframe().total_bounds
        assert bounds.tolist() == pytest.approx(
            [minx - 20, miny - 20, maxx + 20, maxy + 20]
        )
        feature.delete()

    def test_no_intersection_rejected(self, test_domain):
        far_away = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)], crs="EPSG:4326")
        with pytest.raises(UnprocessableEntityException, match="intersect"):
            create_water_feature_from_geodataframe(test_domain, far_away)

    def test_invalid_extent_buffer(self, test_domain, domain_polygons):
        with pytest.raises(UnprocessableEntityException):
            create_building_feature_from_geodataframe(
                test_domain, domain_polygons, extent_buffer_m=500
            )


class TestCreateFeatureFromGeodataframe:
    @pytest.mark.parametrize(
        "feature_type, from_geojson, from_geodataframe, concatenate", UPLOADABLE_TYPES
    )
    def test_create(
        self,
        test_domain,
        domain_polygons,
        feature_type,
        from_geojson,
        from_geodataframe,
        concatenate,
    ):
        # The GeoDataFrame's (projected) CRS is forwarded to the API
        feature = from_geodataframe(test_domain, domain_polygons, name="gdf_upload")

        assert feature.type_ == feature_type
        assert feature.status == JobStatus.COMPLETED
        assert feature.get_data_metadata().total_features == len(domain_polygons)
        feature.delete()


class TestConcatenateFeatures:
    @pytest.mark.parametrize(
        "feature_type, from_geojson, from_geodataframe, concatenate", UPLOADABLE_TYPES
    )
    def test_concatenate(
        self,
        test_domain,
        domain_polygons,
        feature_type,
        from_geojson,
        from_geodataframe,
        concatenate,
    ):
        first = from_geodataframe(test_domain, domain_polygons)
        second = from_geodataframe(test_domain, domain_polygons.iloc[:1])

        # Feature objects and id strings can be mixed
        combined = concatenate(
            test_domain, [first, second.id], name="combined", tags=["concat-test"]
        )

        assert combined.type_ == feature_type
        assert combined.status == JobStatus.COMPLETED
        assert combined.name == "combined"
        assert combined.source["product"] == "concatenate"
        assert combined.source["source_feature_ids"] == [first.id, second.id]

        # Rows are the inputs' rows appended in order, tagged with their input
        gdf = combined.to_geodataframe()
        assert len(gdf) == 3
        assert gdf["source_feature_id"].tolist() == [first.id, first.id, second.id]
        assert gdf["label"].tolist() == ["southwest", "northeast", "southwest"]

        for feature in (combined, first, second):
            feature.delete()

    def test_type_mismatch_rejected(self, test_domain, domain_polygons):
        road = create_road_feature_from_geodataframe(test_domain, domain_polygons)
        building = create_building_feature_from_geodataframe(
            test_domain, domain_polygons
        )

        with pytest.raises(UnprocessableEntityException, match="not a building"):
            concatenate_building_features(test_domain, [road.id, building])

        road.delete()
        building.delete()

    def test_single_feature_rejected(self, test_domain, domain_polygons):
        road = create_road_feature_from_geodataframe(test_domain, domain_polygons)
        with pytest.raises(UnprocessableEntityException):
            concatenate_road_features(test_domain, [road])
        road.delete()


class TestFromId:
    def test_success(self, test_domain, layerset_feature):
        feature = Feature.from_id(test_domain.id, layerset_feature.id)
        assert feature.id == layerset_feature.id
        assert feature.domain_id == test_domain.id
        assert feature.type_ == FeatureType.LAYERSET

    def test_not_found(self, test_domain):
        with pytest.raises(NotFoundException):
            Feature.from_id(test_domain.id, uuid4().hex)


class TestRefreshFeature:
    def test_refresh_returns_self(self, layerset_feature):
        # refresh() updates in place and returns the same object (chains)
        refreshed = layerset_feature.refresh()
        assert refreshed is layerset_feature
        assert refreshed.id == layerset_feature.id

    def test_get_feature_returns_new_instance(self, test_domain, layerset_feature):
        # The "fetch a fresh, separate copy" use case is get_feature(...)
        feature = get_feature(test_domain, layerset_feature.id)
        assert feature.id == layerset_feature.id
        assert feature is not layerset_feature


class TestWait:
    def test_timeout(self, test_domain):
        feature = create_water_feature_from_osm(test_domain)
        with pytest.raises(TimeoutError):
            feature.wait(timeout=0)
        feature.delete()


class TestGetDataMetadata:
    def test_metadata(self, completed_road_feature):
        metadata = completed_road_feature.get_data_metadata()

        assert metadata.total_features > 0
        assert metadata.partition_count >= 1
        assert len(metadata.partitions) == metadata.partition_count
        assert (
            sum(partition.num_features for partition in metadata.partitions)
            == metadata.total_features
        )

    def test_not_completed(self, test_domain):
        # Data is only available once the job is complete
        feature = create_road_feature_from_osm(test_domain)
        with pytest.raises(UnprocessableEntityException, match="status"):
            feature.get_data_metadata()
        feature.delete()


class TestGetDataPartition:
    def test_partition(self, completed_road_feature):
        metadata = completed_road_feature.get_data_metadata()
        partition = completed_road_feature.get_data_partition(0)

        assert partition["type"] == "FeatureCollection"
        assert len(partition["features"]) == metadata.partitions[0].num_features
        assert "crs" in partition

    def test_partition_out_of_range(self, completed_road_feature):
        metadata = completed_road_feature.get_data_metadata()
        with pytest.raises(UnprocessableEntityException, match="out of range"):
            completed_road_feature.get_data_partition(metadata.partition_count)


class TestGetData:
    def test_get_data(self, completed_road_feature):
        metadata = completed_road_feature.get_data_metadata()
        data = completed_road_feature.get_data()

        assert data["type"] == "FeatureCollection"
        assert len(data["features"]) == metadata.total_features
        assert "crs" in data


class TestToGeodataframe:
    def test_to_geodataframe(self, completed_road_feature):
        metadata = completed_road_feature.get_data_metadata()
        gdf = completed_road_feature.to_geodataframe()

        assert len(gdf) == metadata.total_features
        # The data comes back in the projected CRS reported by the
        # feature's georeference
        assert (
            ":".join(gdf.crs.to_authority()) == completed_road_feature.georeference.crs
        )


class TestListFeatures:
    def test_list_in_domain(
        self, test_domain, completed_road_feature, layerset_feature
    ):
        features = list_features(test_domain)
        feature_ids = [feature.id for feature in features]
        assert completed_road_feature.id in feature_ids
        assert layerset_feature.id in feature_ids

    def test_list_cross_domain(self, layerset_feature):
        # No domain: list features across all the user's domains. The SDK
        # returns one page at a time, so search subsequent pages when the
        # account has more than the default page size of 100 features.
        for page in range(100):
            features = list_features(
                page=page,
                size=100,
                sort_by="created_on",
                sort_order="descending",
            )
            if layerset_feature.id in [feature.id for feature in features]:
                return
            if len(features) < 100:
                break

        pytest.fail(
            f"Feature {layerset_feature.id} was not found in the "
            "cross-domain feature pages."
        )

    def test_filter_by_type(
        self, test_domain, completed_road_feature, layerset_feature
    ):
        features = list_features(test_domain, feature_type="road")
        feature_ids = [feature.id for feature in features]
        assert all(feature.type_ == FeatureType.ROAD for feature in features)
        assert completed_road_feature.id in feature_ids
        assert layerset_feature.id not in feature_ids

    def test_filter_by_product(
        self, test_domain, completed_road_feature, layerset_feature
    ):
        features = list_features(test_domain, product="osm")
        feature_ids = [feature.id for feature in features]
        assert completed_road_feature.id in feature_ids
        assert layerset_feature.id not in feature_ids

    def test_filter_by_tag(self, test_domain, layerset_feature):
        features = list_features(test_domain, tag="layerset-test")
        assert [feature.id for feature in features] == [layerset_feature.id]

    def test_sorting(self, test_domain, layerset_feature):
        features = list_features(
            test_domain, sort_by="created_on", sort_order="descending"
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
        feature = create_layerset_feature_from_geojson(
            test_domain, create_default_layerset_geojson(), name="update_target"
        )
        yield feature
        feature.delete()

    def test_update_name(self, test_domain, update_feature):
        # update() mutates in place and returns self (chains)
        updated = update_feature.update(name="updated_name")
        assert updated is update_feature
        assert update_feature.name == "updated_name"
        # The remote resource reflects the update
        assert get_feature(test_domain, update_feature.id).name == "updated_name"

    def test_update_description(self, update_feature):
        updated = update_feature.update(description="updated description")
        assert updated is update_feature
        assert update_feature.description == "updated description"

    def test_update_tags(self, update_feature):
        update_feature.update(tags=["updated"])
        assert update_feature.tags == ["updated"]

    def test_update_no_fields_makes_no_api_call(self, update_feature):
        # No fields provided: returns self without touching the API
        assert update_feature.update() is update_feature


class TestToJson:
    def test_to_json(self, layerset_feature):
        feature_dict = json.loads(layerset_feature.to_json())
        assert feature_dict["id"] == layerset_feature.id
        assert feature_dict["domain_id"] == layerset_feature.domain_id
        assert feature_dict["type"] == "layerset"


class TestDeleteFeature:
    def test_delete_feature(self, test_domain):
        feature = create_water_feature_from_osm(test_domain)
        feature.delete()

        with pytest.raises(NotFoundException):
            Feature.from_id(test_domain.id, feature.id)

        with pytest.raises(NotFoundException):
            feature.delete()
