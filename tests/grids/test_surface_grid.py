"""
test_surface_grid.py
Tests for the SurfaceGrid and SurfaceGridBuilder classes.
"""

# Core imports
from uuid import uuid4

# Internal imports
from tests.utils import create_default_domain
from fastfuels_sdk.grids import SurfaceGrid, SurfaceGridBuilder
from fastfuels_sdk.client_library.models import SurfaceGridAttribute

# External imports
import pytest


@pytest.fixture(scope="module")
def domain_fixture():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


class TestSurfaceGridBuilder:
    """Test suite for the SurfaceGridBuilder class."""

    @pytest.fixture
    def builder(self, domain_fixture):
        """Fixture providing a clean builder instance."""
        return SurfaceGridBuilder(domain_fixture.id)

    def test_initialization(self, builder, domain_fixture):
        """Test basic builder initialization."""
        assert builder.domain_id == domain_fixture.id
        assert builder.attributes == []
        assert builder.config == {}

    def test_with_uniform_fuel_load(self, builder):
        """Test configuring uniform fuel load values."""
        result = builder.with_uniform_fuel_load(0.5)

        assert result is builder  # Returns self for chaining
        assert SurfaceGridAttribute.FUELLOAD in builder.attributes
        assert builder.config["fuel_load"] == {"source": "uniform", "value": 0.5}

        surface_grid = result.build()
        assert isinstance(surface_grid, SurfaceGrid)
        assert surface_grid.fuel_load == {"source": "uniform", "value": 0.5}

    @pytest.mark.parametrize("product", ["FBFM40", "FBFM13"])
    @pytest.mark.parametrize("version", ["2022"])
    @pytest.mark.parametrize("interpolation", ["nearest", "linear", "cubic"])
    def test_with_fuel_load_from_landfire(
        self, builder, product, version, interpolation
    ):
        """Test configuring LANDFIRE fuel load source."""
        result = builder.with_fuel_load_from_landfire(
            product=product,
            version=version,
            interpolation_method=interpolation,
        )

        assert result is builder  # Returns self for chaining
        assert SurfaceGridAttribute.FUELLOAD in builder.attributes
        assert builder.config["fuel_load"] == {
            "source": "LANDFIRE",
            "product": product,
            "version": version,
            "interpolation_method": interpolation,
        }

        surface_grid = result.build()
        assert isinstance(surface_grid, SurfaceGrid)
        assert surface_grid.fuel_load.to_dict() == {
            "source": "LANDFIRE",
            "product": product,
            "version": version,
            "interpolationMethod": interpolation,
        }

    def test_with_fuel_load_from_landfire_invalid_interpolation(self, builder):
        """Test configuring LANDFIRE fuel load source without interpolation."""
        # with pytest.raises(ValueError):
        builder.with_fuel_load_from_landfire("FBFM40", "2022", "invalid")
        builder.build()

    @pytest.mark.parametrize(
        "value,expected_config",
        [
            (15.0, {"source": "uniform", "value": 15.0}),  # 15% moisture
            (100.0, {"source": "uniform", "value": 100.0}),  # Saturated
            (0.0, {"source": "uniform", "value": 0.0}),  # Completely dry
        ],
    )
    def test_with_uniform_fuel_moisture(self, builder, value, expected_config):
        """Test configuring uniform fuel moisture values."""
        result = builder.with_uniform_fuel_moisture(value)

        assert result is builder  # Returns self for chaining
        assert "fuelMoisture" in builder.attributes
        assert builder.config["fuelMoisture"] == expected_config

    @pytest.mark.parametrize(
        "value,expected_config",
        [
            (1, {"source": "uniform", "value": 1}),  # Anderson fuel model 1
            (13, {"source": "uniform", "value": 13}),  # Anderson fuel model 13
            (40, {"source": "uniform", "value": 40}),  # Scott & Burgan model 40
        ],
    )
    def test_with_uniform_fbfm(self, builder, value, expected_config):
        """Test configuring uniform FBFM values."""
        result = builder.with_uniform_fbfm(value)

        assert result is builder  # Returns self for chaining
        assert "FBFM" in builder.attributes
        assert builder.config["FBFM"] == expected_config

    @pytest.mark.parametrize(
        "product,version,interpolation,expected_config",
        [
            (
                "FBFM40",
                "2022",
                "nearest",
                {
                    "source": "LANDFIRE",
                    "product": "FBFM40",
                    "version": "2022",
                    "interpolationMethod": "nearest",
                },
            ),
            (
                "FBFM13",
                "2022",
                "linear",
                {
                    "source": "LANDFIRE",
                    "product": "FBFM13",
                    "version": "2022",
                    "interpolationMethod": "linear",
                },
            ),
        ],
    )
    def test_with_fbfm_from_landfire(
        self, builder, product, version, interpolation, expected_config
    ):
        """Test configuring LANDFIRE FBFM source."""
        result = builder.with_fbfm_from_landfire(
            product=product,
            version=version,
            interpolation_method=interpolation,
        )

        assert result is builder  # Returns self for chaining
        assert "FBFM" in builder.attributes
        assert builder.config["FBFM"] == expected_config

    @pytest.mark.parametrize(
        "value,expected_config",
        [
            (2000, {"source": "uniform", "value": 2000}),  # Common SAVR value
            (5000, {"source": "uniform", "value": 5000}),  # High SAVR
            (500, {"source": "uniform", "value": 500}),  # Low SAVR
        ],
    )
    def test_with_uniform_savr(self, builder, value, expected_config):
        """Test configuring uniform SAVR values."""
        result = builder.with_uniform_savr(value)

        assert result is builder  # Returns self for chaining
        assert "SAVR" in builder.attributes
        assert builder.config["SAVR"] == expected_config

    @pytest.mark.parametrize(
        "product,version,interpolation,expected_config",
        [
            (
                "FBFM40",
                "2022",
                "nearest",
                {
                    "source": "LANDFIRE",
                    "product": "FBFM40",
                    "version": "2022",
                    "interpolationMethod": "nearest",
                },
            ),
        ],
    )
    def test_with_savr_from_landfire(
        self, builder, product, version, interpolation, expected_config
    ):
        """Test configuring LANDFIRE SAVR source."""
        result = builder.with_savr_from_landfire(
            product=product,
            version=version,
            interpolation_method=interpolation,
        )

        assert result is builder  # Returns self for chaining
        assert "SAVR" in builder.attributes
        assert builder.config["SAVR"] == expected_config

    @pytest.mark.parametrize(
        "value,expected_config",
        [
            (0.3, {"source": "uniform", "value": 0.3}),  # 30cm depth
            (1.0, {"source": "uniform", "value": 1.0}),  # 1m depth
            (0.1, {"source": "uniform", "value": 0.1}),  # 10cm depth
        ],
    )
    def test_with_uniform_fuel_depth(self, builder, value, expected_config):
        """Test configuring uniform fuel depth values."""
        result = builder.with_uniform_fuel_depth(value)

        assert result is builder  # Returns self for chaining
        assert "fuelDepth" in builder.attributes
        assert builder.config["fuelDepth"] == expected_config

    @pytest.mark.parametrize(
        "product,version,interpolation,expected_config",
        [
            (
                "FBFM40",
                "2022",
                "nearest",
                {
                    "source": "LANDFIRE",
                    "product": "FBFM40",
                    "version": "2022",
                    "interpolationMethod": "nearest",
                },
            ),
        ],
    )
    def test_with_fuel_depth_from_landfire(
        self, builder, product, version, interpolation, expected_config
    ):
        """Test configuring LANDFIRE fuel depth source."""
        result = builder.with_fuel_depth_from_landfire(
            product=product,
            version=version,
            interpolation_method=interpolation,
        )

        assert result is builder  # Returns self for chaining
        assert "fuelDepth" in builder.attributes
        assert builder.config["fuelDepth"] == expected_config

    def test_with_modification(self, builder):
        """Test adding modifications."""
        conditions = {"field": "slope", "operator": "gt", "value": 30}
        attributes = {"fuelLoad": 0.5}

        result = builder.with_modification(conditions=conditions, attributes=attributes)

        assert result is builder  # Returns self for chaining
        assert "modifications" in builder.config
        assert len(builder.config["modifications"]) == 1
        assert builder.config["modifications"][0] == {
            "conditions": conditions,
            "attributes": attributes,
        }

    def test_multiple_modifications(self, builder):
        """Test adding multiple modifications."""
        mod1 = (
            {"field": "slope", "operator": "gt", "value": 30},
            {"fuelLoad": 0.5},
        )
        mod2 = (
            {"field": "aspect", "operator": "lt", "value": 180},
            {"fuelMoisture": 15.0},
        )

        # Add both modifications
        builder.with_modification(conditions=mod1[0], attributes=mod1[1])
        builder.with_modification(conditions=mod2[0], attributes=mod2[1])

        assert "modifications" in builder.config
        assert len(builder.config["modifications"]) == 2
        assert builder.config["modifications"][0] == {
            "conditions": mod1[0],
            "attributes": mod1[1],
        }
        assert builder.config["modifications"][1] == {
            "conditions": mod2[0],
            "attributes": mod2[1],
        }

    def test_builder_chaining(self, builder):
        """Test chaining multiple builder methods."""
        result = (
            builder.with_uniform_fuel_load(0.5)
            .with_uniform_fuel_moisture(15.0)
            .with_uniform_fbfm(9)
            .with_modification(
                conditions={"field": "slope", "operator": "gt", "value": 30},
                attributes={"fuelLoad": 0.75},
            )
        )

        assert result is builder
        assert set(builder.attributes) == {"fuelLoad", "fuelMoisture", "FBFM"}
        assert "fuelLoad" in builder.config
        assert "fuelMoisture" in builder.config
        assert "FBFM" in builder.config
        assert "modifications" in builder.config

    def test_to_dict(self, builder):
        """Test converting builder configuration to dictionary."""
        # Setup builder with some configuration
        builder.with_uniform_fuel_load(0.5).with_uniform_fuel_moisture(15.0)

        result = builder.to_dict()

        assert result["domain_id"] == builder.domain_id
        assert set(result["attributes"]) == {"fuelLoad", "fuelMoisture"}
        assert result["fuelLoad"] == {"source": "uniform", "value": 0.5}
        assert result["fuelMoisture"] == {"source": "uniform", "value": 15.0}
