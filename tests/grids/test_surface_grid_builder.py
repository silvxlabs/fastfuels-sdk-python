"""
test_surface_grid_builder.py
"""

import random
import pytest
from fastfuels_sdk import SurfaceGrid, SurfaceGridBuilder, Features, Grids
from fastfuels_sdk.client_library.models import (
    SurfaceGridAttribute,
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
    builder = SurfaceGridBuilder(domain_id=domain_fixture.id)
    yield builder


@pytest.fixture(scope="module")
def completed_features(domain_fixture):
    """Fixture that creates and waits for completion of road and water features."""
    features = Features.from_domain_id(domain_fixture.id)

    # Create and wait for road features
    road = features.create_road_feature_from_osm()
    road.wait_until_completed()

    # Create and wait for water features
    water = features.create_water_feature_from_osm()
    water.wait_until_completed()

    # Create feature grid with both attributes
    grids = Grids.from_domain_id(domain_fixture.id)
    feature_grid = grids.create_feature_grid(attributes=["road", "water"])
    feature_grid.wait_until_completed()

    yield features

    # Cleanup
    if features.road:
        features.road.delete()
    if features.water:
        features.water.delete()


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
        """Test basic uniform value configuration."""
        method = getattr(builder, self.method_name)
        result = method(self.test_value)

        assert result is builder
        assert self.attribute in builder.attributes
        assert builder.config[self.attribute_snake_case] == {
            "source": "uniform",
            "value": self.test_value,
        }

    def test_uniform_value_with_feature_masks(self, builder, completed_features):
        """Test uniform value with feature masks."""
        method = getattr(builder, self.method_name)
        result = method(value=self.test_value, feature_masks=["road", "water"])

        assert result is builder
        assert self.attribute in builder.attributes
        assert builder.config[self.attribute_snake_case] == {
            "source": "uniform",
            "value": self.test_value,
            "featureMasks": ["road", "water"],
        }

    def test_invalid_feature_masks(self, builder):
        """Test invalid feature masks raise ValueError."""
        method = getattr(builder, self.method_name)
        with pytest.raises(ValueError):
            method(value=self.test_value, feature_masks=["invalid_feature"])


class BaseUniformBySizeClassTest:
    """Base class for testing uniform by size class configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str
    test_values: dict
    test_groups: list[str]

    def test_uniform_by_size_class(self, builder):
        """Test basic uniform by size class configuration."""
        method = getattr(builder, self.method_name)
        result = method(**self.test_values)

        assert result is builder
        assert self.attribute in builder.attributes
        config = builder.config[self.attribute_snake_case]
        self._verify_size_class_config(config)

    def test_uniform_by_size_class_with_feature_masks(
        self, builder, completed_features
    ):
        """Test uniform by size class with feature masks."""
        method = getattr(builder, self.method_name)
        test_values = {**self.test_values, "feature_masks": ["road", "water"]}
        result = method(**test_values)

        assert result is builder
        config = builder.config[self.attribute_snake_case]
        assert config["featureMasks"] == ["road", "water"]
        self._verify_size_class_config(config)

    def _verify_size_class_config(self, config):
        """Helper method to verify size class configuration."""
        assert config["source"] == "uniformBySizeClass"
        assert config["oneHour"] == self.test_values.get("one_hour")
        assert config["tenHour"] == self.test_values.get("ten_hour")
        assert config["hundredHour"] == self.test_values.get("hundred_hour")
        assert config["liveHerbaceous"] == self.test_values.get("live_herbaceous")
        assert config["liveWoody"] == self.test_values.get("live_woody")
        assert config["groups"] == self.test_groups


class BaseLandfireTest:
    """Base class for testing LANDFIRE source configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str
    test_products: list[str] = ["FBFM40"]
    test_versions: list[str] = ["2022"]
    test_interpolations: list[str] = ["nearest", "linear", "cubic", "zipper"]
    test_groups: list[str] = None

    @pytest.mark.parametrize("product", test_products)
    @pytest.mark.parametrize("version", test_versions)
    @pytest.mark.parametrize("interpolation", test_interpolations)
    def test_landfire_source(self, builder, product, version, interpolation):
        """Test basic LANDFIRE source configuration."""
        method = getattr(builder, self.method_name)

        # Only include groups parameter if the class has defined test_groups
        kwargs = {
            "product": product,
            "version": version,
            "interpolation_method": interpolation,
        }
        if self.test_groups is not None:
            kwargs["groups"] = self.test_groups

        result = method(**kwargs)
        self._verify_landfire_config(result, product, version, interpolation)

    def test_landfire_with_feature_masks(self, builder, completed_features):
        """Test LANDFIRE source with feature masks."""
        method = getattr(builder, self.method_name)
        result = method(
            product=self.test_products[0],
            version=self.test_versions[0],
            interpolation_method=self.test_interpolations[0],
            feature_masks=["road", "water"],
        )

        config = result.config[self.attribute_snake_case]
        assert config["featureMasks"] == ["road", "water"]
        self._verify_landfire_config(
            result,
            self.test_products[0],
            self.test_versions[0],
            self.test_interpolations[0],
        )

    def test_landfire_with_non_burnable(self, builder):
        """Test LANDFIRE source with non-burnable fuel models removal."""
        method = getattr(builder, self.method_name)
        result = method(
            product=self.test_products[0],
            version=self.test_versions[0],
            interpolation_method=self.test_interpolations[0],
            remove_non_burnable=["NB1", "NB2"],
        )

        config = result.config[self.attribute_snake_case]
        assert config["removeNonBurnable"] == ["NB1", "NB2"]

    def test_invalid_non_burnable(self, builder):
        """Test invalid non-burnable fuel models raise ValueError."""
        method = getattr(builder, self.method_name)
        with pytest.raises(ValueError):
            method(
                product=self.test_products[0],
                version=self.test_versions[0],
                interpolation_method=self.test_interpolations[0],
                remove_non_burnable=["INVALID"],
            )

    def _verify_landfire_config(self, result, product, version, interpolation):
        """Helper method to verify LANDFIRE configuration."""
        assert result.config[self.attribute_snake_case]["source"] == "LANDFIRE"
        assert result.config[self.attribute_snake_case]["product"] == product
        assert result.config[self.attribute_snake_case]["version"] == version
        assert (
            result.config[self.attribute_snake_case]["interpolationMethod"]
            == interpolation
        )


class TestFuelLoad:
    """Test suite for fuel load configurations."""

    class TestUniform(BaseUniformTest):
        attribute = SurfaceGridAttribute.FUELLOAD
        attribute_snake_case = "fuel_load"
        method_name = "with_uniform_fuel_load"
        test_value = 0.5

    class TestUniformBySizeClass(BaseUniformBySizeClassTest):
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
        test_groups = [
            "oneHour",
            "tenHour",
            "hundredHour",
            "liveHerbaceous",
            "liveWoody",
        ]

    class TestUniformBySizeClassSingleValue(BaseUniformBySizeClassTest):
        attribute = SurfaceGridAttribute.FUELLOAD
        attribute_snake_case = "fuel_load"
        method_name = "with_uniform_fuel_load_by_size_class"
        test_values = {
            "one_hour": 0.1,
        }
        test_groups = ["oneHour"]

    class TestLandfireFBFM40(BaseLandfireTest):
        attribute = SurfaceGridAttribute.FUELLOAD
        attribute_snake_case = "fuel_load"
        method_name = "with_fuel_load_from_landfire"
        test_groups = [
            "oneHour",
            "tenHour",
            "hundredHour",
            "liveHerbaceous",
            "liveWoody",
        ]

    class TestLandfireFCCS(BaseLandfireTest):
        attribute = SurfaceGridAttribute.FUELLOAD
        attribute_snake_case = "fuel_load"
        method_name = "with_fuel_load_from_landfire"
        test_products = ["FCCS"]
        versions = ["2023"]
        test_groups = [
            "oneHour",
            "tenHour",
            "hundredHour",
        ]


class TestFuelDepth:
    """Test suite for fuel depth configurations."""

    class TestUniform(BaseUniformTest):
        attribute = SurfaceGridAttribute.FUELDEPTH
        attribute_snake_case = "fuel_depth"
        method_name = "with_uniform_fuel_depth"
        test_value = 0.3

    class TestLandfireFBFM40(BaseLandfireTest):
        attribute = SurfaceGridAttribute.FUELDEPTH
        attribute_snake_case = "fuel_depth"
        method_name = "with_fuel_depth_from_landfire"

    class TestLandfireFCCS(BaseLandfireTest):
        attribute = SurfaceGridAttribute.FUELDEPTH
        attribute_snake_case = "fuel_depth"
        method_name = "with_fuel_depth_from_landfire"
        test_products = ["FCCS"]
        versions = ["2023"]


class TestFuelMoisture:
    """Test suite for fuel moisture configurations."""

    class TestUniform(BaseUniformTest):
        attribute = SurfaceGridAttribute.FUELMOISTURE
        attribute_snake_case = "fuel_moisture"
        method_name = "with_uniform_fuel_moisture"
        test_value = 15.0

    class TestUniformBySizeClass(BaseUniformBySizeClassTest):
        attribute = SurfaceGridAttribute.FUELMOISTURE
        attribute_snake_case = "fuel_moisture"
        method_name = "with_uniform_fuel_moisture_by_size_class"
        test_values = {
            "one_hour": 10.0,
            "ten_hour": 15.0,
            "hundred_hour": 20.0,
            "live_herbaceous": 75.0,
            "live_woody": 90.0,
        }
        test_groups = [
            "oneHour",
            "tenHour",
            "hundredHour",
            "liveHerbaceous",
            "liveWoody",
        ]

    class TestUniformBySizeClassOneValue(BaseUniformBySizeClassTest):
        attribute = SurfaceGridAttribute.FUELMOISTURE
        attribute_snake_case = "fuel_moisture"
        method_name = "with_uniform_fuel_moisture_by_size_class"
        test_values = {
            "one_hour": 10.0,
        }
        test_groups = ["oneHour"]


class TestFBFM:
    """Test suite for FBFM configurations."""

    class TestUniform(BaseUniformTest):
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
        attribute = SurfaceGridAttribute.FBFM
        attribute_snake_case = "fbfm"
        method_name = "with_fbfm_from_landfire"
        test_interpolations = [
            "nearest",
            "zipper",
        ]  # Note: FBFM only supports nearest and zipper


class TestSAVR:
    """Test suite for SAVR configurations."""

    class TestUniform(BaseUniformTest):
        attribute = SurfaceGridAttribute.SAVR
        attribute_snake_case = "savr"
        method_name = "with_uniform_savr"
        test_value = 2000

    class TestLandfire(BaseLandfireTest):
        attribute = SurfaceGridAttribute.SAVR
        attribute_snake_case = "savr"
        method_name = "with_savr_from_landfire"
        test_groups = [
            "oneHour",
            "tenHour",
            "hundredHour",
            "liveHerbaceous",
            "liveWoody",
        ]


class TestModifications:
    """Test suite for grid modifications."""

    def test_single_modification(self, builder):
        """Test adding a single modification."""
        result = builder.with_modification(
            actions={"attribute": "FBFM", "modifier": "replace", "value": "GR2"},
            conditions={"attribute": "FBFM", "operator": "eq", "value": "GR1"},
        )

        assert result is builder
        assert "modifications" in builder.config
        assert len(builder.config["modifications"]) == 1
        mod = builder.config["modifications"][0]
        assert len(mod["actions"]) == 1
        assert len(mod["conditions"]) == 1

    def test_multiple_modifications(self, builder):
        """Test adding multiple modifications."""
        result = builder.with_modification(
            actions=[
                {"attribute": "FBFM", "modifier": "replace", "value": "GR2"},
                {"attribute": "fuelLoad", "modifier": "multiply", "value": 1.5},
            ],
            conditions=[
                {"attribute": "FBFM", "operator": "eq", "value": "GR1"},
                {"attribute": "fuelLoad", "operator": "gt", "value": 0.5},
            ],
        )

        assert result is builder
        assert "modifications" in builder.config
        assert len(builder.config["modifications"]) == 1
        mod = builder.config["modifications"][0]
        assert len(mod["actions"]) == 2
        assert len(mod["conditions"]) == 2

    def test_multiple_calls(self, builder):
        """Test adding modifications through multiple calls."""
        builder.with_modification(
            actions={"attribute": "FBFM", "modifier": "replace", "value": "GR2"},
            conditions={"attribute": "FBFM", "operator": "eq", "value": "GR1"},
        )
        builder.with_modification(
            actions={"attribute": "fuelLoad", "modifier": "multiply", "value": 1.5},
            conditions={"attribute": "fuelLoad", "operator": "gt", "value": 0.5},
        )

        assert len(builder.config["modifications"]) == 2

    def test_modification_without_conditions(self, builder):
        """Test adding modifications without conditions."""
        result = builder.with_modification(
            actions={"attribute": "fuelLoad", "modifier": "multiply", "value": 1.1}
        )

        assert result is builder
        assert "modifications" in builder.config
        mod = builder.config["modifications"][0]
        assert len(mod["actions"]) == 1
        assert len(mod["conditions"]) == 0


class TestBuilderMethods:
    """Test suite for general builder methods."""

    def test_clear(self, builder):
        """Test clearing builder configuration."""
        builder.with_uniform_fuel_load(0.5)
        builder.with_uniform_fuel_moisture(15.0)
        assert len(builder.attributes) > 0
        assert len(builder.config) > 0

        builder.clear()
        assert len(builder.attributes) == 0
        assert len(builder.config) == 0

    def test_to_dict(self, builder):
        """Test converting builder configuration to dictionary."""
        builder.with_uniform_fuel_load(0.5)
        builder.with_uniform_fuel_moisture(15.0)

        result = builder.to_dict()
        assert result["domain_id"] == builder.domain_id
        assert "attributes" in result
        assert "fuel_load" in result
        assert "fuel_moisture" in result

    def test_build(self, builder):
        """Test building surface grid from configuration."""
        builder.with_uniform_fuel_load(0.5)
        surface_grid = builder.build()

        assert isinstance(surface_grid, SurfaceGrid)
        assert surface_grid.domain_id == builder.domain_id
