"""
test_surface_grid.py
Tests for the SurfaceGrid and SurfaceGridBuilder classes.
"""

import re
import random
from uuid import uuid4

import pytest
from fastfuels_sdk.grids import SurfaceGrid, SurfaceGridBuilder
from fastfuels_sdk.client_library.models import (
    SurfaceGridAttribute,
    SurfaceGridLandfireSource,
    FBFM40,
)
from tests.utils import create_default_domain


@pytest.fixture(scope="module")
def domain_fixture():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()
    yield domain
    domain.delete()


@pytest.fixture
def builder(domain_fixture):
    """Fixture providing a clean builder instance."""
    builder = SurfaceGridBuilder(domain_fixture.id)
    yield builder.clear()


class BaseGridTest:
    """Base class for all grid tests with common initialization tests."""

    def test_initialization(self, builder, domain_fixture):
        """Test basic builder initialization."""
        assert builder.domain_id == domain_fixture.id
        assert builder.attributes == []
        assert builder.config == {}

    # def test_with_modifications_no_condition(self, builder):
    #     """Test adding modifications without conditions."""
    #     builder.with_modification(
    #         actions={"attribute": "fuelLoad", "modifier": "multiply", "value": 1.1}
    #     )
    #     builder.build()
    #
    # def test_modifications_with_conditions(self, builder):
    #     """Test adding modifications with conditions."""
    #     builder.with_modification(
    #         actions={"attribute": "fuelLoad", "modifier": "multiply", "value": 1.1},
    #         conditions={"attribute": "FBFM", "operator": "eq", "value": "GR1"},
    #     )
    #     builder.build()


class BaseUniformTest:
    """Base class for testing uniform value configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str
    test_value: float

    def test_uniform_value(self, builder):
        method = getattr(builder, self.method_name)
        result = method(self.test_value)

        assert result is builder
        assert self.attribute in builder.attributes
        assert builder.config[self.attribute_snake_case] == {
            "source": "uniform",
            "value": self.test_value,
        }

        surface_grid = result.build()
        attribute_dict = getattr(surface_grid, self.attribute_snake_case).to_dict()
        assert isinstance(surface_grid, SurfaceGrid)
        assert attribute_dict["source"] == "uniform"
        assert attribute_dict["value"] == self.test_value


class BaseUniformBySizeClassTest:
    """Base class for testing uniform by size class configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str
    test_values: dict

    def test_uniform_by_size_class(self, builder):
        method = getattr(builder, self.method_name)
        result = method(**self.test_values)

        assert result is builder
        assert self.attribute in builder.attributes
        config = builder.config[self.attribute_snake_case]
        assert config["source"] == "uniformBySizeClass"
        assert config["oneHour"] == self.test_values["one_hour"]
        assert config["tenHour"] == self.test_values["ten_hour"]
        assert config["hundredHour"] == self.test_values["hundred_hour"]
        assert config["liveHerbaceous"] == self.test_values["live_herbaceous"]
        assert config["liveWoody"] == self.test_values["live_woody"]

        surface_grid = result.build()
        attribute_dict = getattr(surface_grid, self.attribute_snake_case).to_dict()
        self._verify_size_class_values(attribute_dict)

    def _verify_size_class_values(self, attribute_dict):
        assert attribute_dict["source"] == "uniformBySizeClass"
        assert attribute_dict["oneHour"] == self.test_values["one_hour"]
        assert attribute_dict["tenHour"] == self.test_values["ten_hour"]
        assert attribute_dict["hundredHour"] == self.test_values["hundred_hour"]
        assert attribute_dict["liveHerbaceous"] == self.test_values["live_herbaceous"]
        assert attribute_dict["liveWoody"] == self.test_values["live_woody"]


class BaseLandfireTest:
    """Base class for testing LANDFIRE source configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str
    test_products: list[str] = ["FBFM40"]
    test_versions: list[str] = ["2022"]
    test_interpolations: list[str] = ["nearest", "linear", "cubic", "zipper"]

    def test_landfire_source(self, builder, product, version, interpolation):
        method = getattr(builder, self.method_name)
        result = method(
            product=product, version=version, interpolation_method=interpolation
        )

        self._verify_landfire_config(result, product, version, interpolation)

    @classmethod
    def pytest_generate_tests(cls, metafunc):
        if "product" in metafunc.fixturenames:
            metafunc.parametrize("product", cls.test_products)
        if "version" in metafunc.fixturenames:
            metafunc.parametrize("version", cls.test_versions)
        if "interpolation" in metafunc.fixturenames:
            metafunc.parametrize("interpolation", cls.test_interpolations)

    def test_invalid_product(self, builder):
        method = getattr(builder, self.method_name)
        with pytest.raises(ValueError):
            method("invalid", self.test_versions[0], self.test_interpolations[0])
            builder.build()

    def test_invalid_version(self, builder):
        method = getattr(builder, self.method_name)
        with pytest.raises(ValueError):
            method(self.test_products[0], "invalid", self.test_interpolations[0])
            builder.build()

    def test_invalid_interpolation(self, builder):
        method = getattr(builder, self.method_name)
        with pytest.raises(ValueError):
            method(self.test_products[0], self.test_versions[0], "invalid")
            builder.build()

    def _verify_landfire_config(self, result, product, version, interpolation):
        assert result.config[self.attribute_snake_case]["source"] == "LANDFIRE"
        assert result.config[self.attribute_snake_case]["product"] == product
        assert result.config[self.attribute_snake_case]["version"] == version
        assert (
            result.config[self.attribute_snake_case]["interpolationMethod"]
            == interpolation
        )

        surface_grid = result.build()
        attribute_dict = getattr(surface_grid, self.attribute_snake_case).to_dict()
        assert isinstance(surface_grid, SurfaceGrid)
        assert attribute_dict["source"] == "LANDFIRE"
        assert attribute_dict["product"] == product
        assert attribute_dict["version"] == version
        assert attribute_dict["interpolationMethod"] == interpolation


class TestFuelLoad:
    """Test suite for fuel load configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform fuel load configurations."""

        attribute = SurfaceGridAttribute.FUELLOAD
        attribute_snake_case = "fuel_load"
        method_name = "with_uniform_fuel_load"
        test_value = 0.5

    class TestUniformBySizeClass(BaseUniformBySizeClassTest):
        """Test cases for uniform by size class fuel load configurations."""

        attribute = SurfaceGridAttribute.FUELLOAD
        attribute_snake_case = "fuel_load"
        method_name = "with_uniform_fuel_load_by_size_class"
        test_values = {
            "one_hour": 0.1,
            "ten_hour": 0.2,
            "hundred_hour": 0.3,
            "live_herbaceous": 0.4,
            "live_woody": 0.5,
        }

    class TestLandfire(BaseLandfireTest):
        """Test cases for LANDFIRE fuel load configurations."""

        attribute = SurfaceGridAttribute.FUELLOAD
        attribute_snake_case = "fuel_load"
        method_name = "with_fuel_load_from_landfire"
        test_products = ["FBFM40"]
        test_versions = ["2022"]
        test_interpolations = ["nearest", "linear", "cubic", "zipper"]


class TestFuelDepth:
    """Test suite for fuel depth configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform fuel depth configurations."""

        attribute = SurfaceGridAttribute.FUELDEPTH
        attribute_snake_case = "fuel_depth"
        method_name = "with_uniform_fuel_depth"
        test_value = 0.5

    class TestLandfire(BaseLandfireTest):
        """Test cases for LANDFIRE fuel depth configurations."""

        attribute = SurfaceGridAttribute.FUELDEPTH
        attribute_snake_case = "fuel_depth"
        method_name = "with_fuel_depth_from_landfire"
        test_products = ["FBFM40"]
        test_versions = ["2022"]
        test_interpolations = ["nearest", "linear", "cubic", "zipper"]


class TestFuelMoisture:
    """Test suite for fuel moisture configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform fuel moisture configurations."""

        attribute = SurfaceGridAttribute.FUELMOISTURE
        attribute_snake_case = "fuel_moisture"
        method_name = "with_uniform_fuel_moisture"
        test_value = 15.0

    class TestUniformBySizeClass(BaseUniformBySizeClassTest):
        """Test cases for uniform by size class fuel moisture configurations."""

        attribute = SurfaceGridAttribute.FUELMOISTURE
        attribute_snake_case = "fuel_moisture"
        method_name = "with_uniform_fuel_moisture_by_size_class"
        test_values = {
            "one_hour": 0.1,
            "ten_hour": 0.2,
            "hundred_hour": 0.3,
            "live_herbaceous": 0.4,
            "live_woody": 0.5,
        }


class TestFBFM:
    """Test suite for FBFM configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform FBFM configurations."""

        attribute = SurfaceGridAttribute.FBFM
        attribute_snake_case = "fbfm"
        method_name = "with_uniform_fbfm"
        test_value = random.choice(list(FBFM40)).value  # Random FBFM40 value

        @pytest.mark.parametrize("model", ["100", "GR10000", "invalid"])
        def test_invalid_fbfm_model(self, builder, model):
            """Test configuring uniform FBFM with invalid model."""
            with pytest.raises(ValueError):
                builder.with_uniform_fbfm(model)
                builder.build()

    class TestLandfire(BaseLandfireTest):
        """Test cases for LANDFIRE FBFM configurations."""

        attribute = SurfaceGridAttribute.FBFM
        attribute_snake_case = "fbfm"
        method_name = "with_fbfm_from_landfire"
        test_products = ["FBFM40"]
        test_versions = ["2022"]
        test_interpolations = [
            "nearest",
            "zipper",
        ]  # Note: FBFM only supports nearest and zipper


class TestSAVR:
    """Test suite for SAVR configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform SAVR configurations."""

        attribute = SurfaceGridAttribute.SAVR
        attribute_snake_case = "savr"
        method_name = "with_uniform_savr"
        test_value = 2000

    # class TestUniformBySizeClass(BaseUniformBySizeClassTest):
    #     """Test cases for uniform by size class SAVR configurations."""
    #
    #     attribute = SurfaceGridAttribute.SAVR
    #     attribute_snake_case = "savr"
    #     method_name = "with_uniform_savr_by_size_class"
    #     test_values = {
    #         "one_hour": 3000,
    #         "ten_hour": 2000,
    #         "hundred_hour": 1000,
    #         "live_herbaceous": 9000,
    #         "live_woody": 500,
    #     }

    class TestLandfire(BaseLandfireTest):
        """Test cases for LANDFIRE SAVR configurations."""

        attribute = SurfaceGridAttribute.SAVR
        attribute_snake_case = "savr"
        method_name = "with_savr_from_landfire"
        test_products = ["FBFM40"]
        test_versions = ["2022"]
        test_interpolations = ["nearest", "linear", "cubic", "zipper"]