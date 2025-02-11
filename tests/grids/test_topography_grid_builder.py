"""
test_topography_grid_builder.py
"""

import pytest
from fastfuels_sdk import TopographyGrid, TopographyGridBuilder
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
    builder = TopographyGridBuilder(domain_id=domain_fixture.id)
    yield builder


class BaseGridTest:
    """Base class for all grid tests with common initialization tests."""

    def test_initialization(self, builder, domain_fixture):
        """Test basic builder initialization."""
        assert builder.domain_id == domain_fixture.id
        assert builder.attributes == []
        assert builder.config == {}


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

        topography_grid = result.build()
        attribute_dict = getattr(topography_grid, self.attribute_snake_case).to_dict()
        assert isinstance(topography_grid, TopographyGrid)
        assert attribute_dict["source"] == "uniform"
        assert attribute_dict["value"] == self.test_value


class Base3DEPTest:
    """Base class for testing 3DEP source configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str
    test_interpolations: list[str] = ["nearest", "linear", "cubic"]

    @classmethod
    def pytest_generate_tests(cls, metafunc):
        if "interpolation" in metafunc.fixturenames:
            metafunc.parametrize("interpolation", cls.test_interpolations)

    def test_3dep_source(self, builder, interpolation):
        method = getattr(builder, self.method_name)
        try:
            result = method(interpolation_method=interpolation)
        except TypeError:
            result = method()

        self._verify_3dep_config(result, interpolation)

    def test_invalid_interpolation(self, builder):
        method = getattr(builder, self.method_name)
        if self.attribute == "aspect":
            pytest.skip("Aspect only supports nearest neighbor interpolation")
        with pytest.raises(ValueError):
            method(interpolation_method="invalid")
            builder.build()

    def _verify_3dep_config(self, result, interpolation):
        assert result.config[self.attribute_snake_case]["source"] == "3DEP"
        assert (
            result.config[self.attribute_snake_case]["interpolationMethod"]
            == interpolation
        )

        topography_grid = result.build()
        attribute_dict = getattr(topography_grid, self.attribute_snake_case).to_dict()
        assert isinstance(topography_grid, TopographyGrid)
        assert attribute_dict["source"] == "3DEP"
        assert attribute_dict["interpolationMethod"] == interpolation


class BaseLandfireTest:
    """Base class for testing LANDFIRE source configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str
    test_interpolations: list[str] = ["nearest", "linear", "cubic"]

    @classmethod
    def pytest_generate_tests(cls, metafunc):
        if "interpolation" in metafunc.fixturenames:
            metafunc.parametrize("interpolation", cls.test_interpolations)

    def test_landfire_source(self, builder, interpolation):
        method = getattr(builder, self.method_name)
        try:
            result = method(interpolation_method=interpolation)
        except TypeError:
            result = method()

        self._verify_landfire_config(result, interpolation)

    def test_invalid_interpolation(self, builder):
        method = getattr(builder, self.method_name)
        if self.attribute == "aspect":
            pytest.skip("Aspect only supports nearest neighbor interpolation")
        with pytest.raises(ValueError):
            method(interpolation_method="invalid")
            builder.build()

    def _verify_landfire_config(self, result, interpolation):
        assert result.config[self.attribute_snake_case]["source"] == "LANDFIRE"
        assert (
            result.config[self.attribute_snake_case]["interpolationMethod"]
            == interpolation
        )

        topography_grid = result.build()
        attribute_dict = getattr(topography_grid, self.attribute_snake_case).to_dict()
        assert isinstance(topography_grid, TopographyGrid)
        assert attribute_dict["source"] == "LANDFIRE"
        assert attribute_dict["interpolationMethod"] == interpolation


class TestElevation:
    """Test suite for elevation configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform elevation configurations."""

        attribute = "elevation"
        attribute_snake_case = "elevation"
        method_name = "with_elevation_from_uniform_value"
        test_value = 1000.0  # 1000m elevation

    class Test3DEP(Base3DEPTest):
        """Test cases for 3DEP elevation configurations."""

        attribute = "elevation"
        attribute_snake_case = "elevation"
        method_name = "with_elevation_from_3dep"

    class TestLandfire(BaseLandfireTest):
        """Test cases for LANDFIRE elevation configurations."""

        attribute = "elevation"
        attribute_snake_case = "elevation"
        method_name = "with_elevation_from_landfire"


class TestSlope:
    """Test suite for slope configurations."""

    class Test3DEP(Base3DEPTest):
        """Test cases for 3DEP slope configurations."""

        attribute = "slope"
        attribute_snake_case = "slope"
        method_name = "with_slope_from_3dep"

    class TestLandfire(BaseLandfireTest):
        """Test cases for LANDFIRE slope configurations."""

        attribute = "slope"
        attribute_snake_case = "slope"
        method_name = "with_slope_from_landfire"


class TestAspect:
    """Test suite for aspect configurations."""

    class Test3DEP(Base3DEPTest):
        """Test cases for 3DEP aspect configurations."""

        attribute = "aspect"
        attribute_snake_case = "aspect"
        method_name = "with_aspect_from_3dep"
        test_interpolations = ["nearest"]  # Aspect only supports nearest neighbor

    class TestLandfire(BaseLandfireTest):
        """Test cases for LANDFIRE aspect configurations."""

        attribute = "aspect"
        attribute_snake_case = "aspect"
        method_name = "with_aspect_from_landfire"
        test_interpolations = ["nearest"]  # Aspect only supports nearest neighbor


class TestBuilder(BaseGridTest):
    """Test suite for TopographyGridBuilder class."""

    def test_build_with_all_attributes(self, builder):
        """Test building grid with all attributes configured."""
        result = (
            builder.with_elevation_from_3dep()
            .with_slope_from_3dep()
            .with_aspect_from_3dep()
            .build()
        )

        assert isinstance(result, TopographyGrid)
        assert sorted(result.attributes) == sorted(["elevation", "slope", "aspect"])

    def test_clear(self, builder):
        """Test clearing builder configuration."""
        builder.with_elevation_from_3dep()
        assert len(builder.attributes) > 0
        assert len(builder.config) > 0

        builder.clear()
        assert builder.attributes == []
        assert builder.config == {}

    def test_to_dict(self, builder):
        """Test converting builder configuration to dictionary."""
        builder.with_elevation_from_3dep()
        dict_config = builder.to_dict()

        assert dict_config["domain_id"] == builder.domain_id
        assert dict_config["attributes"] == builder.attributes
        assert "elevation" in dict_config
