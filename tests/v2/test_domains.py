"""
tests/v2/test_domains.py
"""

# Core imports
import json
from uuid import uuid4

# Internal imports
from tests import TEST_DATA_DIR
from tests.v2.utils import create_default_domain
from fastfuels_sdk.v2.domains import Domain, list_domains, reproject_geojson
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

# External imports
import pytest
import geopandas as gpd


@pytest.fixture(scope="module")
def test_domain():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


def feature_names(domain: Domain) -> set:
    """Return the named features in a domain response."""
    return {feature.to_dict()["properties"]["name"] for feature in domain.features}


class TestCreateDomain:
    test_files = ["blue_mtn", "blue_mtn_5070"]
    test_formats = ["geojson", "kml", "shp"]

    domain_name = "test_domain"
    domain_description = "Domain for testing v2 domain operations"
    pad_to_resolution = 2.0

    def assert_valid_domain(
        self,
        domain: Domain,
        input_gdf: gpd.GeoDataFrame,
        expected_crs_name: str = None,
    ):
        """Shared assertions for a freshly created domain."""
        assert len(domain.id) > 0
        assert domain.name == self.domain_name
        assert domain.description == self.domain_description
        assert domain.pad_to_resolution == self.pad_to_resolution

        # v2 responses carry two named features: the working extent and
        # the original input geometry
        assert feature_names(domain) == {"domain", "input"}

        # If the input CRS is projected, the domain preserves it (echoing
        # the CRS name as sent, e.g. "urn:ogc:def:crs:EPSG::5070");
        # otherwise the geometry is projected to the appropriate UTM zone
        if input_gdf.crs.is_projected:
            expected = expected_crs_name or ":".join(input_gdf.crs.to_authority())
            assert domain.crs.properties.name == expected
        else:
            assert domain.crs.properties.name == input_gdf.estimate_utm_crs().srs

    @pytest.mark.parametrize("test_name", test_files)
    @pytest.mark.parametrize("geojson_type", ["Feature", "FeatureCollection"])
    def test_from_geojson(self, test_name, geojson_type):
        # Load test GeoJSON data
        geojson_gdf = gpd.GeoDataFrame.from_file(TEST_DATA_DIR / f"{test_name}.geojson")
        with open(TEST_DATA_DIR / f"{test_name}.geojson") as f:
            geojson = json.load(f)

        if geojson_type == "Feature":
            feature_geojson = geojson["features"][0]
            if "crs" in geojson:
                feature_geojson["crs"] = geojson["crs"]
            geojson = feature_geojson

        # Create a domain using the GeoJSON (a single Feature is wrapped
        # into a FeatureCollection by the SDK)
        domain = Domain.from_geojson(
            geojson,
            name=self.domain_name,
            description=self.domain_description,
            pad_to_resolution=self.pad_to_resolution,
        )
        # A projected domain echoes the CRS name exactly as the file
        # declares it
        file_crs = geojson.get("crs", {}).get("properties", {}).get("name")
        self.assert_valid_domain(domain, geojson_gdf, expected_crs_name=file_crs)
        domain.delete()

    @pytest.mark.parametrize("test_name", test_files)
    def test_from_geodataframe(self, test_name):
        geojson_gdf = gpd.GeoDataFrame.from_file(TEST_DATA_DIR / f"{test_name}.geojson")

        # Create a domain using the GeoDataFrame. The GeoDataFrame CRS is
        # forwarded to the API, so projected inputs (blue_mtn_5070) must
        # come back in their original CRS, not the EPSG:4326 default.
        domain = Domain.from_geodataframe(
            geojson_gdf,
            name=self.domain_name,
            description=self.domain_description,
            pad_to_resolution=self.pad_to_resolution,
        )
        self.assert_valid_domain(domain, geojson_gdf)
        domain.delete()

    @pytest.mark.parametrize("test_format", test_formats)
    def test_from_file(self, test_format):
        geojson_gdf = gpd.GeoDataFrame.from_file(TEST_DATA_DIR / "blue_mtn.geojson")

        domain = Domain.from_file(
            TEST_DATA_DIR / f"blue_mtn.{test_format}",
            name=self.domain_name,
            description=self.domain_description,
            pad_to_resolution=self.pad_to_resolution,
        )
        self.assert_valid_domain(domain, geojson_gdf)
        domain.delete()

    def test_from_geojson_invalid_type(self):
        with pytest.raises(ValueError, match="FeatureCollection"):
            Domain.from_geojson({"type": "Point", "coordinates": [0, 0]})

    def test_tags(self):
        with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
            geojson = json.load(f)
        domain = Domain.from_geojson(geojson, tags=["test", "v2"])
        assert domain.tags == ["test", "v2"]
        domain.delete()


class TestPreviewDomain:
    def test_preview(self):
        with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
            geojson = json.load(f)

        previewed = Domain.preview(geojson, pad_to_resolution=2.0)

        # A preview is never persisted; its id is the "preview" sentinel
        assert previewed.id == "preview"
        assert feature_names(previewed) == {"domain", "input"}
        assert previewed.pad_to_resolution == 2.0
        assert len(previewed.bbox) >= 4


class TestFromId:
    def test_success(self, test_domain):
        domain = Domain.from_id(test_domain.id)
        assert domain.id == test_domain.id
        assert domain.name == test_domain.name

    def test_not_found(self):
        with pytest.raises(NotFoundException):
            Domain.from_id(uuid4().hex)


class TestGetDomain:
    def test_get_default(self, test_domain):
        domain = test_domain.get()
        assert domain.id == test_domain.id
        assert domain is not test_domain

    def test_get_in_place(self, test_domain):
        domain = test_domain.get(in_place=True)
        assert domain is test_domain


class TestUpdateDomain:
    def test_update_name(self, test_domain):
        updated = test_domain.update(name="updated_name")
        assert updated.name == "updated_name"
        assert updated is not test_domain
        # The remote resource reflects the update
        assert Domain.from_id(test_domain.id).name == "updated_name"

    def test_update_in_place(self, test_domain):
        updated = test_domain.update(description="updated description", in_place=True)
        assert updated is test_domain
        assert test_domain.description == "updated description"

    def test_update_tags(self, test_domain):
        updated = test_domain.update(tags=["updated"], in_place=True)
        assert updated.tags == ["updated"]

    def test_update_no_fields_makes_no_api_call(self, test_domain):
        # No fields provided: returns a copy without touching the API
        copy = test_domain.update()
        assert copy is not test_domain
        assert copy.id == test_domain.id
        assert test_domain.update(in_place=True) is test_domain


class TestGetLattice:
    def test_get_lattice(self, test_domain):
        lattice = test_domain.get_lattice(resolution=2.0)
        assert lattice.resolution == 2.0
        assert lattice.num_buffer_cells == 0
        assert lattice.crs == test_domain.crs.properties.name
        # Affine coefficients [a, b, c, d, e, f] (rasterio convention)
        assert len(lattice.transform) == 6
        assert lattice.transform[0] == 2.0
        assert abs(lattice.transform[4]) == 2.0
        # [height, width] in pixels
        assert len(lattice.shape) == 2
        assert all(dim > 0 for dim in lattice.shape)

    def test_buffer_cells_expand_the_lattice(self, test_domain):
        lattice = test_domain.get_lattice(resolution=2.0)
        buffered = test_domain.get_lattice(resolution=2.0, num_buffer_cells=5)
        assert buffered.shape[0] == lattice.shape[0] + 10
        assert buffered.shape[1] == lattice.shape[1] + 10

    def test_invalid_resolution(self, test_domain):
        with pytest.raises(UnprocessableEntityException):
            test_domain.get_lattice(resolution=-1.0)


class TestListDomains:
    def test_list_domains(self, test_domain):
        domains = list_domains()
        assert test_domain.id in [domain.id for domain in domains]

    def test_sorting(self, test_domain):
        domains = list_domains(sort_by="created_on", sort_order="descending")
        assert len(domains) > 0

    def test_invalid_sort_field(self):
        with pytest.raises(ValueError):
            list_domains(sort_by="not_a_field")


class TestReprojectGeojson:
    def test_reproject(self):
        with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
            geojson = json.load(f)

        projected = reproject_geojson(geojson, target_epsg=5070)

        assert projected["crs"]["properties"]["name"] == "EPSG:5070"
        assert len(projected["features"]) == len(geojson["features"])
        # Coordinates actually moved out of degrees
        original_coord = geojson["features"][0]["geometry"]["coordinates"][0][0]
        projected_coord = projected["features"][0]["geometry"]["coordinates"][0][0]
        assert original_coord != projected_coord

    def test_invalid_target_epsg(self):
        with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
            geojson = json.load(f)
        with pytest.raises(UnprocessableEntityException):
            reproject_geojson(geojson, target_epsg=999999)


class TestToGeodataframe:
    def test_to_geodataframe(self, test_domain):
        gdf = test_domain.to_geodataframe()

        assert len(gdf) == len(test_domain.features)
        assert set(gdf["name"]) == {"domain", "input"}
        assert (gdf["domain_id"] == test_domain.id).all()
        assert ":".join(gdf.crs.to_authority()) == test_domain.crs.properties.name


class TestToJson:
    def test_to_json(self, test_domain):
        domain_dict = json.loads(test_domain.to_json())
        assert domain_dict["id"] == test_domain.id
        assert domain_dict["type"] == "FeatureCollection"


class TestDeleteDomain:
    def test_delete_domain(self):
        domain = create_default_domain()
        domain.delete()

        with pytest.raises(NotFoundException):
            Domain.from_id(domain.id)

        with pytest.raises(NotFoundException):
            domain.delete()
