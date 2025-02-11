"""
test_domains.py
"""

# Core imports
import json
from uuid import uuid4

# Internal imports
from tests import TEST_DATA_DIR
from tests.utils import create_default_domain
from fastfuels_sdk.domains import Domain, list_domains
from fastfuels_sdk.client_library.exceptions import NotFoundException

# External imports
import pytest
import geopandas as gdp
from shapely import to_geojson


@pytest.fixture(scope="module")
def test_domain():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


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
            name=self.domain_name,
            description=f"test {test_name} from {test_format} geodataframe",
            horizontal_resolution=self.horizontal_resolution,
            vertical_resolution=self.vertical_resolution,
        )

        assert len(domain.id) > 0
        assert domain.name == self.domain_name
        assert domain.description == f"test {test_name} from {test_format} geodataframe"
        assert domain.horizontal_resolution == self.horizontal_resolution
        assert domain.vertical_resolution == self.vertical_resolution


class TestCreateDomainFromId:
    def test_success(self, test_domain):
        """Test successful retrieval of a domain"""
        # Get the domain using the ID from our test domain
        retrieved_domain = Domain.from_id(test_domain.id)

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
            Domain.from_id(uuid4().hex)


class TestGetDomain:
    def test_get_update_default(self, test_domain):
        """Test get() returns new instance with updated data by default"""
        original_domain = test_domain
        updated_domain = original_domain.get()

        # Verify new instance returned
        assert updated_domain is not original_domain

        # Verify data matches
        assert updated_domain.id == original_domain.id
        assert updated_domain.name == original_domain.name
        assert updated_domain.features == original_domain.features
        assert (
            updated_domain.horizontal_resolution
            == original_domain.horizontal_resolution
        )

    def test_get_update_in_place(self, test_domain):
        """Test get(in_place=True) updates existing instance"""
        domain = test_domain
        result = domain.get(in_place=True)

        # Verify same instance returned
        assert result is domain

        # Verify instance was updated
        assert isinstance(result, Domain)
        assert result.id == test_domain.id
        assert result.name == test_domain.name
        assert result.features == test_domain.features


class TestUpdateDomainMethod:
    """Test suite for Domain.update() method."""

    def test_update_name(self, test_domain):
        """Test updating just the name."""
        test_domain = test_domain.get()
        new_name = "Updated Test Domain"
        updated = test_domain.update(name=new_name)

        # Verify new instance returned
        assert updated is not test_domain
        # Verify name updated
        assert updated.name == new_name
        # Verify other fields unchanged
        assert updated.id == test_domain.id
        assert updated.description == test_domain.description
        assert updated.tags == test_domain.tags

    def test_update_description(self, test_domain):
        """Test updating just the description."""
        test_domain = test_domain.get()
        new_desc = "Updated test domain description"
        updated = test_domain.update(description=new_desc)

        assert updated is not test_domain
        assert updated.description == new_desc
        assert updated.name == test_domain.name
        assert updated.tags == test_domain.tags

    def test_update_tags(self, test_domain):
        """Test updating just the tags."""
        test_domain = test_domain.get()
        new_tags = ["test", "updated", "2024"]
        updated = test_domain.update(tags=new_tags)

        assert updated is not test_domain
        assert updated.tags == new_tags
        assert updated.name == test_domain.name
        assert updated.description == test_domain.description

    def test_update_multiple_fields(self, test_domain):
        """Test updating multiple fields at once."""
        test_domain = test_domain.get()
        updates = {
            "name": "Multi-Updated Domain",
            "description": "Updated description",
            "tags": ["multiple", "updates"],
        }
        updated = test_domain.update(**updates)

        assert updated is not test_domain
        assert updated.name == updates["name"]
        assert updated.description == updates["description"]
        assert updated.tags == updates["tags"]
        # Verify other fields unchanged
        assert updated.id == test_domain.id
        assert updated.horizontal_resolution == test_domain.horizontal_resolution
        assert updated.vertical_resolution == test_domain.vertical_resolution

    def test_update_in_place(self, test_domain):
        """Test updating in place modifies the existing instance."""
        test_domain = test_domain.get()
        new_name = "In-Place Updated Domain"
        result = test_domain.update(name=new_name, in_place=True)

        # Verify same instance returned and modified
        assert result is test_domain
        assert test_domain.name == new_name
        assert isinstance(result, Domain)

    def test_update_no_changes(self, test_domain):
        """Test update with no field changes returns same data."""
        test_domain = test_domain.get()
        updated = test_domain.update()

        assert updated is not test_domain  # Still new instance
        assert updated.id == test_domain.id
        assert updated.name == test_domain.name
        assert updated.description == test_domain.description
        assert updated.tags == test_domain.tags

    def test_update_no_changes_in_place(self, test_domain):
        """Test update with no changes in place returns same instance unchanged."""
        test_domain = test_domain.get()
        original_dict = test_domain.to_dict()
        result = test_domain.update(in_place=True)

        assert result is test_domain
        assert test_domain.to_dict() == original_dict

    def test_update_clear_fields(self, test_domain):
        """Test updating fields to None or empty values."""
        test_domain = test_domain.get()
        updated = test_domain.update(
            description="", tags=[]  # Empty string  # Empty list
        )

        assert updated.description == ""
        assert updated.tags == []
        # Verify other fields preserved
        assert updated.name == test_domain.name

    def test_update_preserves_immutable_fields(self, test_domain):
        """Test that immutable fields aren't affected by updates."""
        test_domain = test_domain.get()
        original_resolution = test_domain.horizontal_resolution
        original_features = test_domain.features

        updated = test_domain.update(name="New Name")

        assert updated.horizontal_resolution == original_resolution
        assert updated.features == original_features

    @pytest.mark.parametrize(
        "bad_tags",
        [
            "not_a_list",  # String instead of list
            [1, 2, 3],  # Numbers instead of strings
            [None],  # None in list
        ],
    )
    def test_update_invalid_tags(self, test_domain, bad_tags):
        """Test error handling for invalid tag values."""
        with pytest.raises(Exception) as exc_info:
            test_domain.update(tags=bad_tags)  # noqa
        assert "validation error" in str(exc_info.value).lower()

    def test_chained_updates(self, test_domain):
        """Test that updates can be chained when using in_place=True."""
        test_domain = test_domain.get()
        result = (
            test_domain.update(name="First Update", in_place=True)
            .update(description="Second Update", in_place=True)
            .update(tags=["third", "update"], in_place=True)
        )

        assert result is test_domain
        assert test_domain.name == "First Update"
        assert test_domain.description == "Second Update"
        assert test_domain.tags == ["third", "update"]


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
        for domain in created_domains:
            try:
                domain.delete()
            except Exception as e:
                print(f"Warning: Could not delete test domain {domain.id}: {e}")

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


class TestDeleteDomain:
    def test_delete_domain_success(self):
        """Test successful deletion of a domain"""
        domain_to_delete = create_default_domain()
        domain_to_delete.delete()

        # list_domains should not return the domain we just deleted
        domains = list_domains()
        assert domain_to_delete.id not in [d.id for d in domains.domains]  # noqa

        # get_domain should not work with the id of the domain we just deleted
        with pytest.raises(NotFoundException):
            domain_to_delete.get()
