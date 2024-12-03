"""
test_domains.py
"""

import json
import time
from uuid import uuid4
from pathlib import Path

from tests import TEST_DATA_DIR
from fastfuels_sdk.domains import Domain, list_domains, get_domain
from fastfuels_sdk.client_library.exceptions import NotFoundException

import pytest
import geopandas as gdp


@pytest.fixture(scope="module")
def test_domain():
    """Fixture that creates a test domain to be used by the tests"""
    # Load test GeoJSON data
    with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
        geojson = json.load(f)

    # Create a domain using the GeoJSON
    domain = Domain.from_geojson(
        geojson,
        name="test_domain",
        description="Domain for testing domain operations",
        horizontal_resolution=1.0,
        vertical_resolution=1.0,
    )

    # Return the domain for use in tests
    yield domain

    # Cleanup could be added here if needed
    # Note: Currently there's no delete_domain functionality


class TestCreateDomain:
    test_files = ["blue_mtn", "blue_mtn_5070"]
    test_format = ["geojson", "kml", "shp"]

    domain_name = "test_domain"
    domain_description = "Domain for testing domain operations"
    horizontal_resolution = 1.0
    vertical_resolution = 1.0

    @pytest.mark.parametrize("test_name", test_files)
    @pytest.mark.parametrize("geojson_type", ["Feature", "FeatureCollection"])
    def test_from_geojson(self, test_name, geojson_type):
        # Load test GeoJSON data
        geojson_gdf = gdp.GeoDataFrame.from_file(TEST_DATA_DIR / f"{test_name}.geojson")
        with open(TEST_DATA_DIR / f"{test_name}.geojson") as f:
            geojson = json.load(f)

        if geojson_type == "Feature":
            feature_geojson = geojson["features"][0]
            if "crs" in geojson:
                feature_geojson["crs"] = geojson["crs"]
            geojson = feature_geojson

        # Create a domain using the GeoJSON
        domain = Domain.from_geojson(
            geojson,
            name=self.domain_name,
            description=self.domain_description,
            horizontal_resolution=self.horizontal_resolution,
            vertical_resolution=self.vertical_resolution,
        )

        # Assert that the domain has the expected attributes
        assert len(domain.id) > 0
        assert domain.name == self.domain_name
        assert domain.description == self.domain_description
        assert domain.horizontal_resolution == self.horizontal_resolution
        assert domain.vertical_resolution == self.vertical_resolution

        # If the geojson has a CRS, and the CRS is projected, assert that the domain has the same CRS
        if geojson_gdf.crs.is_projected:
            assert domain.crs.properties.name == geojson["crs"]["properties"]["name"]
        # Otherwise the domain should have been projected to UTM
        else:
            utm_crs_epsg = geojson_gdf.estimate_utm_crs().srs
            assert domain.crs.properties.name == utm_crs_epsg

        # Assert that the domain has the expected number of features
        assert len(domain.features) == 2  # Has "input" and "domain" features
        assert "input" in [f.properties["name"] for f in domain.features]
        assert "domain" in [f.properties["name"] for f in domain.features]

        geojson_gdf_proj = geojson_gdf.to_crs(domain.crs.properties.name)
        geojson_polygon_dict = json.loads(to_geojson(geojson_gdf_proj.geometry[0]))

        # Assert that the input feature is the same as the input feature in the geojson (after accounting for differing CRS)
        input_feature = domain.features[1]
        input_feature_geometry = input_feature.geometry.to_dict()
        assert input_feature_geometry == geojson_polygon_dict

        # Assert that the geojson is inside the domain (after accounting for differing CRS)
        domain_feature = domain.features[0]
        domain_feature_gdf = gdp.GeoDataFrame.from_features(
            [domain_feature.to_dict()], crs=domain.crs.properties.name
        )
        assert geojson_gdf_proj.within(domain_feature_gdf.geometry[0]).all()

    def test_from_geojson_bad_geojson(self):
        geojson = {"type": "FeatureCollection", "features": []}
        with pytest.raises(ValueError):
            Domain.from_geojson(
                geojson,
                name="test",
                description="test",
                horizontal_resolution=1.0,
                vertical_resolution=1.0,
            )

    @pytest.mark.parametrize("test_format", test_format)
    @pytest.mark.parametrize("test_name", ["blue_mtn"])
    def test_from_geodataframe(self, test_name, test_format):
        fpath = TEST_DATA_DIR / f"{test_name}.{test_format}"
        geodataframe = gdp.GeoDataFrame.from_file(fpath)
        domain = Domain.from_geodataframe(
            geodataframe,
            name=f"test {test_name}",
            description=f"test {test_name} from {test_format} geodataframe",
            horizontal_resolution=1.0,
            vertical_resolution=1.0,
        )

        assert len(domain.id) > 0
        assert domain.name == f"test {test_name}"
        assert domain.description == f"test {test_name} from {test_format} geodataframe"
        assert domain.horizontal_resolution == 1.0
        assert domain.vertical_resolution == 1.0


class TestListDomains:
    @pytest.fixture(scope="class", autouse=True)
    def ensure_multiple_domains(self):
        """Fixture to ensure at least two domains exist before running tests.

        This fixture runs once per test class and ensures we have at least
        two domains for sorting tests. It yields control to the tests after
        creating domains if needed.
        """
        # Check current domain count
        response = list_domains()
        created_domains = []

        # If we don't have at least 2 domains, create them
        if len(response.domains) < 2:
            # Load test GeoJSON data
            with open(TEST_DATA_DIR / "blue_mtn.geojson") as f:
                geojson = json.load(f)

            # Create two domains with different names to ensure sortability
            domains = [
                Domain.from_geojson(
                    geojson,
                    name="A Test Domain",
                    description="First test domain for sorting tests",
                    horizontal_resolution=1.0,
                    vertical_resolution=1.0,
                ),
                Domain.from_geojson(
                    geojson,
                    name="B Test Domain",
                    description="Second test domain for sorting tests",
                    horizontal_resolution=1.0,
                    vertical_resolution=1.0,
                ),
            ]
            created_domains.extend(domains)

        # Yield control to the tests
        yield

        # Cleanup: Delete any domains we created
        # Note: Uncomment when delete_domain functionality is implemented
        # for domain in created_domains:
        #     try:
        #         delete_domain(domain.id)
        #     except Exception as e:
        #         print(f"Warning: Could not delete test domain {domain.id}: {e}")

    def test_list_domains_basic(self):
        """Test the structure and content of list_domains response."""
        response = list_domains()

        # Test response attributes
        assert hasattr(response, "domains"), "Response missing domains attribute"
        assert hasattr(
            response, "current_page"
        ), "Response missing current_page attribute"
        assert hasattr(response, "page_size"), "Response missing page_size attribute"
        assert hasattr(
            response, "total_items"
        ), "Response missing total_items attribute"

        # Test response content
        assert len(response.domains) > 0, "Response contains no domains"
        assert isinstance(
            response.domains[0], Domain
        ), "Response domains not of type Domain"
        assert response.total_items >= len(
            response.domains
        ), "Total items less than returned domains"
        assert response.page_size > 0, "Page size must be positive"

    @pytest.mark.parametrize(
        "page,size,expected_count",
        [
            (0, 2, 2),  # First page, 2 items
            (1, 2, None),  # Second page, up to 2 items
            (0, 1000, None),  # Maximum page size
        ],
    )
    def test_list_domains_pagination(self, page, size, expected_count):
        """Test pagination with various page sizes and numbers."""
        response = list_domains(page=page, size=size)

        # Verify pagination metadata
        assert (
            response.current_page == page
        ), f"Expected page {page}, got {response.current_page}"
        assert (
            response.page_size == size
        ), f"Expected size {size}, got {response.page_size}"

        # Verify domain count if expected_count specified
        if expected_count is not None:
            assert (
                len(response.domains) == expected_count
            ), f"Expected {expected_count} domains, got {len(response.domains)}"

    @pytest.mark.parametrize(
        "sort_by,sort_order,field_getter",
        [
            ("name", "ascending", lambda x: x.name),
            ("name", "descending", lambda x: x.name),
            ("createdOn", "ascending", lambda x: x.created_on),
            ("createdOn", "descending", lambda x: x.created_on),
            ("modifiedOn", "ascending", lambda x: x.modified_on),
            ("modifiedOn", "descending", lambda x: x.modified_on),
        ],
    )
    def test_list_domains_sorting(self, sort_by, sort_order, field_getter):
        """Test sorting functionality of list_domains with different sort fields and orders."""
        response = list_domains(sort_by=sort_by, sort_order=sort_order)
        assert len(response.domains) >= 2, "Test requires at least 2 domains"

        # Get values of the sorted field from first two domains
        first_value = field_getter(response.domains[0])
        second_value = field_getter(response.domains[1])

        # For ascending order, first should be <= second
        if sort_order == "ascending":
            assert first_value <= second_value, (
                f"Expected {first_value} <= {second_value} for "
                f"{sort_by} in {sort_order} order"
            )

        # For descending order, first should be >= second
        else:
            assert first_value >= second_value, (
                f"Expected {first_value} >= {second_value} for "
                f"{sort_by} in {sort_order} order"
            )

    @pytest.mark.parametrize(
        "invalid_input,expected_error",
        [
            (dict(page=-1), "validation error"),  # Invalid page
            (dict(size=1001), "validation error"),  # Size too large
            (dict(size=0), "validation error"),  # Size too small
            (
                dict(sort_by="invalid"),
                "'invalid' is not a valid DomainSortField",
            ),  # Invalid sort field
            (
                dict(sort_order="invalid"),
                "'invalid' is not a valid DomainSortOrder",
            ),  # Invalid sort order
        ],
    )
    def test_list_domains_invalid_parameters(self, invalid_input, expected_error):
        """Test error handling for invalid parameters."""
        with pytest.raises(Exception) as exc_info:
            list_domains(**invalid_input)
        assert expected_error.lower() in str(exc_info.value).lower()

    def test_list_domains_empty_results(self):
        """Test pagination beyond available results."""
        response = list_domains(page=9999)
        assert len(response.domains) == 0, "Expected empty results for high page number"
        assert response.current_page == 9999, "Page number not preserved"
        assert response.total_items is not None, "Total items should still be returned"
        assert response.current_page == 9999


class TestGetDomain:
    def test_get_domain_success(self, test_domain):
        """Test successful retrieval of a domain"""
        # Get the domain using the ID from our test domain
        retrieved_domain = get_domain(test_domain.id)

        # Verify the retrieved domain matches our test domain
        assert retrieved_domain.id == test_domain.id
        assert retrieved_domain.name == test_domain.name
        assert retrieved_domain.description == test_domain.description
        assert (
            retrieved_domain.horizontal_resolution == test_domain.horizontal_resolution
        )
        assert retrieved_domain.vertical_resolution == test_domain.vertical_resolution
        assert retrieved_domain.type == test_domain.type

        # Check the features are present
        assert len(retrieved_domain.features) == len(test_domain.features)

        # Verify CRS information
        assert retrieved_domain.crs.type == test_domain.crs.type
        assert retrieved_domain.crs.properties.name == test_domain.crs.properties.name

    def test_bad_id(self):
        """Test error handling for a non-existent domain ID"""
        with pytest.raises(NotFoundException):
            get_domain(uuid4().hex)
