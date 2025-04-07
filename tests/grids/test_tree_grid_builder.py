"""
test_tree_grid_builder.py
"""

from __future__ import annotations
import pytest
from fastfuels_sdk import TreeGrid, TreeGridBuilder, Inventories
from tests.utils import create_default_domain


@pytest.fixture(scope="module")
def domain_fixture():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()
    yield domain
    domain.delete()


@pytest.fixture(scope="module")
def tree_inventory_fixture(domain_fixture):
    """Fixture that creates a test tree inventory to be used by the tests"""
    tree_inventory = Inventories.from_domain_id(
        domain_id=domain_fixture.id
    ).create_tree_inventory_from_treemap()

    tree_inventory.wait_until_completed()

    yield tree_inventory


@pytest.fixture
def builder(domain_fixture, tree_inventory_fixture):
    """Fixture providing a clean builder instance."""
    builder = TreeGridBuilder(domain_id=domain_fixture.id)
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
    test_value: float | str

    def test_uniform_value(self, builder):
        method = getattr(builder, self.method_name)
        result = method(self.test_value)

        assert result is builder
        assert self.attribute in builder.attributes

        # Check the uniform value was correctly configured
        assert builder.config[self.attribute_snake_case] == {
            "source": "uniform",
            "value": self.test_value,
        }

        tree_grid = result.build()
        attribute_dict = getattr(tree_grid, self.attribute_snake_case).to_dict()
        assert isinstance(tree_grid, TreeGrid)
        assert attribute_dict["source"] == "uniform"
        assert attribute_dict["value"] == self.test_value


class BaseInventoryTest:
    """Base class for testing inventory source configurations."""

    attribute: str
    attribute_snake_case: str
    method_name: str

    def test_inventory_source(self, builder):
        method = getattr(builder, self.method_name)
        result = method()

        assert result is builder
        assert self.attribute in builder.attributes

        # Check that the inventory source was correctly configured
        assert builder.config[self.attribute_snake_case] == {"source": "TreeInventory"}

        tree_grid = result.build()
        attribute_dict = getattr(tree_grid, self.attribute_snake_case).to_dict()
        assert isinstance(tree_grid, TreeGrid)
        assert attribute_dict["source"] == "TreeInventory"


class TestBulkDensity:
    """Test suite for bulk density configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform bulk density configurations."""

        attribute = "bulkDensity"
        attribute_snake_case = "bulk_density"
        method_name = "with_uniform_bulk_density"
        test_value = 0.5  # kg/m³

    class TestInventory(BaseInventoryTest):
        """Test cases for inventory bulk density configurations."""

        attribute = "bulkDensity"
        attribute_snake_case = "bulk_density"
        method_name = "with_bulk_density_from_tree_inventory"


class TestSAVR:
    """Test suite for surface area to volume ratio (SAVR) configurations."""

    class TestInventory(BaseInventoryTest):
        """Test cases for inventory SAVR configurations."""

        attribute = "SAVR"
        attribute_snake_case = "savr"
        method_name = "with_savr_from_tree_inventory"


class TestSPCD:
    """Test suite for Species Code (SPCD) configurations."""

    class TestInventory(BaseInventoryTest):
        """Test cases for inventory SPCD configurations."""

        attribute = "SPCD"
        attribute_snake_case = "spcd"
        method_name = "with_spcd_from_tree_inventory"


class TestFuelMoisture:
    """Test suite for fuel moisture configurations."""

    class TestUniform(BaseUniformTest):
        """Test cases for uniform fuel moisture configurations."""

        attribute = "fuelMoisture"
        attribute_snake_case = "fuel_moisture"
        method_name = "with_uniform_fuel_moisture"
        test_value = 15.0  # 15% moisture


class TestBuilder(BaseGridTest):
    """Test suite for TreeGridBuilder class."""

    def test_build_with_all_attributes(self, builder):
        """Test building grid with all attributes configured."""
        result = (
            builder.with_bulk_density_from_tree_inventory()
            .with_spcd_from_tree_inventory()
            .with_uniform_fuel_moisture(15.0)
            .build()
        )

        assert isinstance(result, TreeGrid)
        assert sorted(result.attributes) == sorted(
            ["bulkDensity", "SPCD", "fuelMoisture"]
        )

    def test_clear(self, builder):
        """Test clearing builder configuration."""
        builder.with_bulk_density_from_tree_inventory()
        assert len(builder.attributes) > 0
        assert len(builder.config) > 0

        builder.clear()
        assert builder.attributes == []
        assert builder.config == {}

    def test_to_dict(self, builder):
        """Test converting builder configuration to dictionary."""
        builder.with_bulk_density_from_tree_inventory()
        dict_config = builder.to_dict()

        assert dict_config["domain_id"] == builder.domain_id
        assert dict_config["attributes"] == builder.attributes
        assert "bulk_density" in dict_config
