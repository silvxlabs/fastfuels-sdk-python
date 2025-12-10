"""
tests/test_convenience_config.py

Tests for the convenience function configuration system.
"""

# Core imports
from __future__ import annotations
from unittest.mock import Mock, patch

# Internal imports
from fastfuels_sdk.convenience import (
    export_roi_to_quicfire,
    DEFAULT_TOPOGRAPHY_CONFIG,
    DEFAULT_SURFACE_CONFIG,
    DEFAULT_TREE_CONFIG,
    DEFAULT_FEATURES_CONFIG,
    DEFAULT_TREE_INVENTORY_CONFIG,
)

# External imports
import geopandas as gpd
import pytest
from shapely.geometry import Polygon


@pytest.fixture
def sample_roi():
    """Create a sample ROI for testing."""
    # Create a simple polygon
    polygon = Polygon(
        [
            [-114.095, 46.832],
            [-114.112, 46.832],
            [-114.112, 46.824],
            [-114.095, 46.824],
            [-114.095, 46.832],
        ]
    )
    return gpd.GeoDataFrame([{"geometry": polygon}], crs="EPSG:4326")


class TestDefaultConfigurations:
    """Test that current hardcoded values are properly extracted as defaults."""

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_current_hardcoded_topography_config(
        self,
        mock_inventories,
        mock_grids,
        mock_tree_builder,
        mock_surface_builder,
        mock_topo_builder,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that current topography configuration is documented."""
        # Setup mocks to avoid actual API calls
        mock_domain.from_geodataframe.return_value.id = "test-domain"
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance

        # Mock builder chain
        mock_topo_instance = Mock()
        mock_topo_builder.return_value = mock_topo_instance
        mock_topo_instance.with_elevation_from_3dep.return_value = mock_topo_instance
        mock_topo_instance.build.return_value = Mock()

        # Mock other builders
        mock_surface_instance = Mock()
        mock_surface_builder.return_value = mock_surface_instance
        mock_surface_instance.with_fuel_load_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_fuel_depth_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_uniform_fuel_moisture.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.build.return_value = Mock()

        mock_tree_instance = Mock()
        mock_tree_builder.return_value = mock_tree_instance
        mock_tree_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_tree_instance
        )
        mock_tree_instance.with_uniform_fuel_moisture.return_value = mock_tree_instance
        mock_tree_instance.build.return_value = Mock()

        # Mock other components
        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export
        mock_grids_instance.create_feature_grid.return_value = Mock()

        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            Mock()
        )

        # Call the function
        export_roi_to_quicfire(sample_roi, "/tmp/test")

        # Verify topography builder was called with current hardcoded values
        mock_topo_instance.with_elevation_from_3dep.assert_called_once_with(
            interpolation_method="linear"
        )

        # Verify surface builder was called with current hardcoded values
        mock_surface_instance.with_fuel_load_from_landfire.assert_called_once_with(
            product="FBFM40",
            version="2022",
            interpolation_method="cubic",
            curing_live_herbaceous=0.25,
            curing_live_woody=0.1,
            groups=["oneHour"],
            feature_masks=["road", "water"],
            remove_non_burnable=["NB1", "NB2"],
        )

        mock_surface_instance.with_fuel_depth_from_landfire.assert_called_once_with(
            product="FBFM40",
            version="2022",
            interpolation_method="cubic",
            feature_masks=["road", "water"],
            remove_non_burnable=["NB1", "NB2"],
        )

        mock_surface_instance.with_uniform_fuel_moisture.assert_called_once_with(
            value=0.15, feature_masks=["road", "water"]
        )

        # Verify tree builder was called with current hardcoded values
        mock_tree_instance.with_uniform_fuel_moisture.assert_called_once_with(value=100)

        # Verify features were created (roads and water)
        assert mock_features_instance.create_road_feature_from_osm.called
        assert mock_features_instance.create_water_feature_from_osm.called

        # Verify tree inventory was created with current masks
        mock_inventories_instance.create_tree_inventory_from_treemap.assert_called_once_with(
            version="2022",
            seed=None,
            canopy_height_map_source="Meta2024",
            modifications=None,
            treatments=None,
            feature_masks=["road", "water"],
        )

    def test_default_configuration_constants(self):
        """Test that default configuration constants match expected structure."""
        # Test topography config
        assert DEFAULT_TOPOGRAPHY_CONFIG["attributes"] == ["elevation"]
        assert DEFAULT_TOPOGRAPHY_CONFIG["elevation"]["source"] == "3DEP"
        assert DEFAULT_TOPOGRAPHY_CONFIG["elevation"]["interpolationMethod"] == "linear"

        # Test surface config
        assert "fuelLoad" in DEFAULT_SURFACE_CONFIG["attributes"]
        assert "fuelDepth" in DEFAULT_SURFACE_CONFIG["attributes"]
        assert "fuelMoisture" in DEFAULT_SURFACE_CONFIG["attributes"]

        assert DEFAULT_SURFACE_CONFIG["fuelLoad"]["source"] == "LANDFIRE"
        assert DEFAULT_SURFACE_CONFIG["fuelLoad"]["product"] == "FBFM40"
        assert DEFAULT_SURFACE_CONFIG["fuelLoad"]["version"] == "2022"
        assert DEFAULT_SURFACE_CONFIG["fuelMoisture"]["value"] == 0.15

        # Test tree config
        assert DEFAULT_TREE_CONFIG["attributes"] == ["bulkDensity", "fuelMoisture"]
        assert DEFAULT_TREE_CONFIG["fuelMoisture"]["value"] == 100

        # Test features config
        assert DEFAULT_FEATURES_CONFIG["createRoadFeatures"] is True
        assert DEFAULT_FEATURES_CONFIG["createWaterFeatures"] is True
        assert DEFAULT_FEATURES_CONFIG["featureGridAttributes"] == ["road", "water"]

        # Test tree inventory config
        assert DEFAULT_TREE_INVENTORY_CONFIG["featureMasks"] == ["road", "water"]
        assert DEFAULT_TREE_INVENTORY_CONFIG["canopyHeightMapSource"] == "Meta2024"


class TestConfigurationMerger:
    """Test the configuration merger utility function."""

    def test_merge_config_with_none_returns_default(self):
        """Test that merging with None returns the default config unchanged."""
        from fastfuels_sdk.convenience import _merge_config

        default_config = {"a": 1, "b": {"c": 2, "d": 3}}
        result = _merge_config(default_config, None)

        assert result == default_config
        assert result is not default_config  # Should be a copy

    def test_merge_config_shallow_override(self):
        """Test merging with shallow overrides."""
        from fastfuels_sdk.convenience import _merge_config

        default_config = {"a": 1, "b": 2}
        user_config = {"b": 99}

        result = _merge_config(default_config, user_config)

        expected = {"a": 1, "b": 99}
        assert result == expected

    def test_merge_config_deep_override(self):
        """Test merging with deep nested overrides."""
        from fastfuels_sdk.convenience import _merge_config

        default_config = {
            "fuelMoisture": {
                "source": "uniform",
                "value": 0.15,
                "featureMasks": ["road", "water"],
            },
            "fuelLoad": {"source": "LANDFIRE", "version": "2022"},
        }

        user_config = {"fuelMoisture": {"value": 0.05}}  # Only override the value

        result = _merge_config(default_config, user_config)

        expected = {
            "fuelMoisture": {
                "source": "uniform",
                "value": 0.05,  # Overridden
                "featureMasks": ["road", "water"],  # Preserved
            },
            "fuelLoad": {"source": "LANDFIRE", "version": "2022"},  # Preserved
        }
        assert result == expected

    def test_merge_config_adds_new_keys(self):
        """Test that merger adds new keys from user config."""
        from fastfuels_sdk.convenience import _merge_config

        default_config = {"a": 1}
        user_config = {"b": 2, "c": {"d": 3}}

        result = _merge_config(default_config, user_config)

        expected = {"a": 1, "b": 2, "c": {"d": 3}}
        assert result == expected

    def test_merge_config_preserves_lists(self):
        """Test that list values are replaced, not merged."""
        from fastfuels_sdk.convenience import _merge_config

        default_config = {
            "attributes": ["a", "b", "c"],
            "featureMasks": ["road", "water"],
        }

        user_config = {
            "attributes": ["x", "y"],
            "featureMasks": ["road"],  # Remove water
        }

        result = _merge_config(default_config, user_config)

        expected = {
            "attributes": ["x", "y"],  # Completely replaced
            "featureMasks": ["road"],  # Completely replaced
        }
        assert result == expected


class TestTopographyConfigProcessor:
    """Test topography configuration processor."""

    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    def test_configure_topography_builder_default(self, mock_builder_class):
        """Test topography builder configuration with default settings."""
        from fastfuels_sdk.convenience import (
            _configure_topography_builder,
            DEFAULT_TOPOGRAPHY_CONFIG,
        )

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance
        mock_builder_instance.with_elevation_from_3dep.return_value = (
            mock_builder_instance
        )
        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        result = _configure_topography_builder("test-domain", DEFAULT_TOPOGRAPHY_CONFIG)

        # Verify builder was created with correct domain
        mock_builder_class.assert_called_once_with(domain_id="test-domain")

        # Verify correct method was called based on config
        mock_builder_instance.with_elevation_from_3dep.assert_called_once_with(
            interpolation_method="linear"
        )

        # Verify build was called
        mock_builder_instance.build.assert_called_once()
        assert result == mock_grid

    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    def test_configure_topography_builder_landfire_source(self, mock_builder_class):
        """Test topography builder with LANDFIRE source."""
        from fastfuels_sdk.convenience import _configure_topography_builder

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance
        mock_builder_instance.with_elevation_from_landfire.return_value = (
            mock_builder_instance
        )
        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        landfire_config = {
            "attributes": ["elevation"],
            "elevation": {"source": "LANDFIRE", "interpolationMethod": "cubic"},
        }

        result = _configure_topography_builder("test-domain", landfire_config)

        mock_builder_instance.with_elevation_from_landfire.assert_called_once_with(
            interpolation_method="cubic"
        )

        assert result == mock_grid

    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    def test_configure_topography_builder_uniform_elevation(self, mock_builder_class):
        """Test topography builder with uniform elevation."""
        from fastfuels_sdk.convenience import _configure_topography_builder

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance
        mock_builder_instance.with_elevation_from_uniform_value.return_value = (
            mock_builder_instance
        )
        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        uniform_config = {
            "attributes": ["elevation"],
            "elevation": {"source": "uniform", "value": 1500.0},
        }

        result = _configure_topography_builder("test-domain", uniform_config)

        mock_builder_instance.with_elevation_from_uniform_value.assert_called_once_with(
            value=1500.0
        )

        assert result == mock_grid


class TestSurfaceConfigProcessor:
    """Test surface configuration processor."""

    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    def test_configure_surface_builder_default(self, mock_builder_class):
        """Test surface builder configuration with default settings."""
        from fastfuels_sdk.convenience import (
            _configure_surface_builder,
            DEFAULT_SURFACE_CONFIG,
        )

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance

        # Setup builder method chain returns
        mock_builder_instance.with_fuel_load_from_landfire.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_fuel_depth_from_landfire.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_uniform_fuel_moisture.return_value = (
            mock_builder_instance
        )

        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        result = _configure_surface_builder("test-domain", DEFAULT_SURFACE_CONFIG)

        # Verify builder was created with correct domain
        mock_builder_class.assert_called_once_with(domain_id="test-domain")

        # Verify fuel load configuration
        mock_builder_instance.with_fuel_load_from_landfire.assert_called_once_with(
            product="FBFM40",
            version="2022",
            interpolation_method="cubic",
            curing_live_herbaceous=0.25,
            curing_live_woody=0.1,
            groups=["oneHour"],
            feature_masks=["road", "water"],
            remove_non_burnable=["NB1", "NB2"],
        )

        # Verify fuel depth configuration
        mock_builder_instance.with_fuel_depth_from_landfire.assert_called_once_with(
            product="FBFM40",
            version="2022",
            interpolation_method="cubic",
            feature_masks=["road", "water"],
            remove_non_burnable=["NB1", "NB2"],
        )

        # Verify fuel moisture configuration
        mock_builder_instance.with_uniform_fuel_moisture.assert_called_once_with(
            value=0.15, feature_masks=["road", "water"]
        )

        # Verify build was called
        mock_builder_instance.build.assert_called_once()
        assert result == mock_grid

    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    def test_configure_surface_builder_custom_fuel_moisture(self, mock_builder_class):
        """Test surface builder with custom fuel moisture value."""
        from fastfuels_sdk.convenience import _configure_surface_builder

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance

        mock_builder_instance.with_fuel_load_from_landfire.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_fuel_depth_from_landfire.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_uniform_fuel_moisture.return_value = (
            mock_builder_instance
        )

        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        # Custom config with 5% fuel moisture
        custom_config = {
            "attributes": ["fuelLoad", "fuelDepth", "fuelMoisture"],
            "fuelLoad": {
                "source": "LANDFIRE",
                "product": "FBFM40",
                "version": "2022",
                "interpolationMethod": "cubic",
                "curingLiveHerbaceous": 0.25,
                "curingLiveWoody": 0.1,
                "groups": ["oneHour"],
                "featureMasks": ["road", "water"],
                "removeNonBurnable": ["NB1", "NB2"],
            },
            "fuelDepth": {
                "source": "LANDFIRE",
                "product": "FBFM40",
                "version": "2022",
                "interpolationMethod": "cubic",
                "featureMasks": ["road", "water"],
                "removeNonBurnable": ["NB1", "NB2"],
            },
            "fuelMoisture": {
                "source": "uniform",
                "value": 0.05,  # 5% instead of default 15%
                "featureMasks": ["road", "water"],
            },
        }

        result = _configure_surface_builder("test-domain", custom_config)

        # Should call with 5% fuel moisture
        mock_builder_instance.with_uniform_fuel_moisture.assert_called_once_with(
            value=0.05, feature_masks=["road", "water"]
        )

        assert result == mock_grid

    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    def test_configure_surface_builder_uniform_fuel_load(self, mock_builder_class):
        """Test surface builder with uniform fuel load."""
        from fastfuels_sdk.convenience import _configure_surface_builder

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance

        mock_builder_instance.with_uniform_fuel_load.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_fuel_depth_from_landfire.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_uniform_fuel_moisture.return_value = (
            mock_builder_instance
        )

        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        uniform_config = {
            "attributes": ["fuelLoad", "fuelDepth", "fuelMoisture"],
            "fuelLoad": {
                "source": "uniform",
                "value": 2.5,
                "featureMasks": ["road", "water"],
            },
            "fuelDepth": {
                "source": "LANDFIRE",
                "product": "FBFM40",
                "version": "2022",
                "interpolationMethod": "cubic",
                "featureMasks": ["road", "water"],
                "removeNonBurnable": ["NB1", "NB2"],
            },
            "fuelMoisture": {
                "source": "uniform",
                "value": 0.15,
                "featureMasks": ["road", "water"],
            },
        }

        result = _configure_surface_builder("test-domain", uniform_config)

        # Should call uniform fuel load method instead of LANDFIRE
        mock_builder_instance.with_uniform_fuel_load.assert_called_once_with(
            value=2.5, feature_masks=["road", "water"]
        )

        assert result == mock_grid


class TestTreeConfigProcessor:
    """Test tree configuration processor."""

    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    def test_configure_tree_builder_default(self, mock_builder_class):
        """Test tree builder configuration with default settings."""
        from fastfuels_sdk.convenience import (
            _configure_tree_builder,
            DEFAULT_TREE_CONFIG,
        )

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance

        # Setup builder method chain returns
        mock_builder_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_uniform_fuel_moisture.return_value = (
            mock_builder_instance
        )

        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        result = _configure_tree_builder("test-domain", DEFAULT_TREE_CONFIG)

        # Verify builder was created with correct domain
        mock_builder_class.assert_called_once_with(domain_id="test-domain")

        # Verify bulk density configuration
        mock_builder_instance.with_bulk_density_from_tree_inventory.assert_called_once()

        # Verify fuel moisture configuration
        mock_builder_instance.with_uniform_fuel_moisture.assert_called_once_with(
            value=100
        )

        # Verify build was called
        mock_builder_instance.build.assert_called_once()
        assert result == mock_grid

    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    def test_configure_tree_builder_custom_fuel_moisture(self, mock_builder_class):
        """Test tree builder with custom fuel moisture value."""
        from fastfuels_sdk.convenience import _configure_tree_builder

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance

        mock_builder_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_uniform_fuel_moisture.return_value = (
            mock_builder_instance
        )

        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        custom_config = {
            "attributes": ["bulkDensity", "fuelMoisture"],
            "bulkDensity": {"source": "inventory"},
            "fuelMoisture": {
                "source": "uniform",
                "value": 80,  # Different from default 100
            },
        }

        result = _configure_tree_builder("test-domain", custom_config)

        # Should call with custom fuel moisture
        mock_builder_instance.with_uniform_fuel_moisture.assert_called_once_with(
            value=80
        )

        assert result == mock_grid

    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    def test_configure_tree_builder_uniform_bulk_density(self, mock_builder_class):
        """Test tree builder with uniform bulk density."""
        from fastfuels_sdk.convenience import _configure_tree_builder

        mock_builder_instance = Mock()
        mock_builder_class.return_value = mock_builder_instance

        mock_builder_instance.with_uniform_bulk_density.return_value = (
            mock_builder_instance
        )
        mock_builder_instance.with_uniform_fuel_moisture.return_value = (
            mock_builder_instance
        )

        mock_grid = Mock()
        mock_builder_instance.build.return_value = mock_grid

        uniform_config = {
            "attributes": ["bulkDensity", "fuelMoisture"],
            "bulkDensity": {"source": "uniform", "value": 0.5},
            "fuelMoisture": {"source": "uniform", "value": 100},
        }

        result = _configure_tree_builder("test-domain", uniform_config)

        # Should call uniform bulk density method instead of inventory
        mock_builder_instance.with_uniform_bulk_density.assert_called_once_with(
            value=0.5
        )

        assert result == mock_grid


class TestIntegratedConfigurationSystem:
    """Test the integrated configuration system with the main function."""

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience._configure_topography_builder")
    @patch("fastfuels_sdk.convenience._configure_surface_builder")
    @patch("fastfuels_sdk.convenience._configure_tree_builder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_export_roi_with_surface_fuel_moisture_config(
        self,
        mock_inventories,
        mock_grids,
        mock_configure_tree,
        mock_configure_surface,
        mock_configure_topography,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that custom surface fuel moisture configuration is used."""
        from fastfuels_sdk.convenience import export_roi_to_quicfire

        # Setup domain mock
        mock_domain.from_geodataframe.return_value.id = "test-domain"

        # Setup features mock
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance
        mock_road_feature = Mock()
        mock_water_feature = Mock()
        mock_features_instance.create_road_feature_from_osm.return_value = (
            mock_road_feature
        )
        mock_features_instance.create_water_feature_from_osm.return_value = (
            mock_water_feature
        )

        # Setup builder processor mocks
        mock_topo_grid = Mock()
        mock_configure_topography.return_value = mock_topo_grid

        mock_surface_grid = Mock()
        mock_configure_surface.return_value = mock_surface_grid

        mock_tree_grid = Mock()
        mock_configure_tree.return_value = mock_tree_grid

        # Setup grids mock
        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_feature_grid = Mock()
        mock_grids_instance.create_feature_grid.return_value = mock_feature_grid
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export

        # Setup inventories mock
        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_tree_inventory = Mock()
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            mock_tree_inventory
        )

        # Custom surface config with 5% fuel moisture
        surface_config = {
            "fuelMoisture": {
                "source": "uniform",
                "value": 0.05,
                "featureMasks": ["road", "water"],
            }
        }

        # Call the function with custom config
        result = export_roi_to_quicfire(
            sample_roi, "/tmp/test", surface_config=surface_config
        )

        # Verify that surface builder was called with merged config
        mock_configure_surface.assert_called_once()
        called_config = mock_configure_surface.call_args[0][1]

        # Should have fuel moisture override but keep other defaults
        assert called_config["fuelMoisture"]["value"] == 0.05
        assert called_config["fuelLoad"]["source"] == "LANDFIRE"  # Default preserved
        assert called_config["fuelLoad"]["version"] == "2022"  # Default preserved

        assert result == mock_export


class TestExportRoiFormats:
    """Test the export_roi function with different export formats."""

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_export_roi_default_quicfire_format(
        self,
        mock_inventories,
        mock_grids,
        mock_tree_builder,
        mock_surface_builder,
        mock_topo_builder,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that export_roi defaults to QUIC-Fire format."""
        from fastfuels_sdk.convenience import export_roi

        # Setup mocks
        mock_domain.from_geodataframe.return_value.id = "test-domain"
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance

        # Mock builders
        mock_topo_instance = Mock()
        mock_topo_builder.return_value = mock_topo_instance
        mock_topo_instance.with_elevation_from_3dep.return_value = mock_topo_instance
        mock_topo_instance.build.return_value = Mock()

        mock_surface_instance = Mock()
        mock_surface_builder.return_value = mock_surface_instance
        mock_surface_instance.with_fuel_load_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_fuel_depth_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_uniform_fuel_moisture.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.build.return_value = Mock()

        mock_tree_instance = Mock()
        mock_tree_builder.return_value = mock_tree_instance
        mock_tree_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_tree_instance
        )
        mock_tree_instance.with_uniform_fuel_moisture.return_value = mock_tree_instance
        mock_tree_instance.build.return_value = Mock()

        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export

        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_tree_inventory = Mock()
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            mock_tree_inventory
        )

        # Call export_roi with default format
        result = export_roi(sample_roi, "/tmp/test")

        # Verify create_export was called with "QUIC-Fire"
        mock_grids_instance.create_export.assert_called_once_with("QUIC-Fire")
        assert result == mock_export

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_export_roi_with_zarr_format(
        self,
        mock_inventories,
        mock_grids,
        mock_tree_builder,
        mock_surface_builder,
        mock_topo_builder,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that export_roi works with zarr format."""
        from fastfuels_sdk.convenience import export_roi

        # Setup mocks
        mock_domain.from_geodataframe.return_value.id = "test-domain"
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance

        # Mock builders
        mock_topo_instance = Mock()
        mock_topo_builder.return_value = mock_topo_instance
        mock_topo_instance.with_elevation_from_3dep.return_value = mock_topo_instance
        mock_topo_instance.build.return_value = Mock()

        mock_surface_instance = Mock()
        mock_surface_builder.return_value = mock_surface_instance
        mock_surface_instance.with_fuel_load_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_fuel_depth_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_uniform_fuel_moisture.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.build.return_value = Mock()

        mock_tree_instance = Mock()
        mock_tree_builder.return_value = mock_tree_instance
        mock_tree_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_tree_instance
        )
        mock_tree_instance.with_uniform_fuel_moisture.return_value = mock_tree_instance
        mock_tree_instance.build.return_value = Mock()

        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export

        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_tree_inventory = Mock()
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            mock_tree_inventory
        )

        # Call export_roi with zarr format
        result = export_roi(sample_roi, "/tmp/test", export_format="zarr")

        # Verify create_export was called with "zarr"
        mock_grids_instance.create_export.assert_called_once_with("zarr")
        assert result == mock_export

    def test_export_roi_invalid_format_raises_error(self, sample_roi):
        """Test that export_roi raises ValueError for invalid format."""
        from fastfuels_sdk.convenience import export_roi

        with pytest.raises(ValueError) as excinfo:
            export_roi(sample_roi, "/tmp/test", export_format="invalid-format")

        assert "Unsupported export format: invalid-format" in str(excinfo.value)
        assert "QUIC-Fire" in str(excinfo.value)
        assert "zarr" in str(excinfo.value)

    @patch("fastfuels_sdk.convenience.export_roi")
    def test_export_roi_to_quicfire_is_wrapper(self, mock_export_roi, sample_roi):
        """Test that export_roi_to_quicfire properly wraps export_roi."""
        # Setup mock
        mock_export = Mock()
        mock_export_roi.return_value = mock_export

        # Call export_roi_to_quicfire
        result = export_roi_to_quicfire(
            sample_roi,
            "/tmp/test",
            verbose=True,
            topography_config={"test": "config"},
        )

        # Verify export_roi was called with correct parameters
        mock_export_roi.assert_called_once_with(
            roi=sample_roi,
            export_path="/tmp/test",
            export_format="QUIC-Fire",
            verbose=True,
            topography_config={"test": "config"},
            surface_config=None,
            tree_config=None,
            features_config=None,
            tree_inventory_config=None,
        )
        assert result == mock_export


class TestTreeInventoryModificationsAndTreatments:
    """Test that modifications and treatments are properly passed through to tree inventory."""

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_modifications_passed_to_tree_inventory(
        self,
        mock_inventories,
        mock_grids,
        mock_tree_builder,
        mock_surface_builder,
        mock_topo_builder,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that modifications config is passed to create_tree_inventory_from_treemap."""
        # Setup basic mocks
        mock_domain.from_geodataframe.return_value.id = "test-domain"
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance

        # Mock builders
        mock_topo_instance = Mock()
        mock_topo_builder.return_value = mock_topo_instance
        mock_topo_instance.with_elevation_from_3dep.return_value = mock_topo_instance
        mock_topo_instance.build.return_value = Mock()

        mock_surface_instance = Mock()
        mock_surface_builder.return_value = mock_surface_instance
        mock_surface_instance.with_fuel_load_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_fuel_depth_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_uniform_fuel_moisture.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.build.return_value = Mock()

        mock_tree_instance = Mock()
        mock_tree_builder.return_value = mock_tree_instance
        mock_tree_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_tree_instance
        )
        mock_tree_instance.with_uniform_fuel_moisture.return_value = mock_tree_instance
        mock_tree_instance.build.return_value = Mock()

        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export
        mock_grids_instance.create_feature_grid.return_value = Mock()

        # Setup inventories mock
        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_tree_inventory = Mock()
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            mock_tree_inventory
        )

        # Define modifications configuration
        modifications_config = [
            {
                "conditions": [{"attribute": "CR", "operator": "gt", "value": 0.1}],
                "actions": [{"attribute": "CR", "modifier": "multiply", "value": 0.9}],
            }
        ]

        tree_inventory_config = {"modifications": modifications_config}

        # Call export_roi with modifications
        result = export_roi_to_quicfire(
            sample_roi, "/tmp/test", tree_inventory_config=tree_inventory_config
        )

        # Verify create_tree_inventory_from_treemap was called with modifications
        mock_inventories_instance.create_tree_inventory_from_treemap.assert_called_once()
        call_kwargs = (
            mock_inventories_instance.create_tree_inventory_from_treemap.call_args[1]
        )

        assert "modifications" in call_kwargs
        assert call_kwargs["modifications"] == modifications_config
        assert result == mock_export

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_treatments_passed_to_tree_inventory(
        self,
        mock_inventories,
        mock_grids,
        mock_tree_builder,
        mock_surface_builder,
        mock_topo_builder,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that treatments config is passed to create_tree_inventory_from_treemap."""
        # Setup basic mocks (same as above)
        mock_domain.from_geodataframe.return_value.id = "test-domain"
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance

        mock_topo_instance = Mock()
        mock_topo_builder.return_value = mock_topo_instance
        mock_topo_instance.with_elevation_from_3dep.return_value = mock_topo_instance
        mock_topo_instance.build.return_value = Mock()

        mock_surface_instance = Mock()
        mock_surface_builder.return_value = mock_surface_instance
        mock_surface_instance.with_fuel_load_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_fuel_depth_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_uniform_fuel_moisture.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.build.return_value = Mock()

        mock_tree_instance = Mock()
        mock_tree_builder.return_value = mock_tree_instance
        mock_tree_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_tree_instance
        )
        mock_tree_instance.with_uniform_fuel_moisture.return_value = mock_tree_instance
        mock_tree_instance.build.return_value = Mock()

        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export
        mock_grids_instance.create_feature_grid.return_value = Mock()

        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_tree_inventory = Mock()
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            mock_tree_inventory
        )

        # Define treatments configuration
        treatments_config = [
            {
                "method": "proportionalThinning",
                "targetMetric": "basalArea",
                "targetValue": 25.0,
            }
        ]

        tree_inventory_config = {"treatments": treatments_config}

        # Call export_roi with treatments
        result = export_roi_to_quicfire(
            sample_roi, "/tmp/test", tree_inventory_config=tree_inventory_config
        )

        # Verify create_tree_inventory_from_treemap was called with treatments
        mock_inventories_instance.create_tree_inventory_from_treemap.assert_called_once()
        call_kwargs = (
            mock_inventories_instance.create_tree_inventory_from_treemap.call_args[1]
        )

        assert "treatments" in call_kwargs
        assert call_kwargs["treatments"] == treatments_config
        assert result == mock_export

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_modifications_and_treatments_together(
        self,
        mock_inventories,
        mock_grids,
        mock_tree_builder,
        mock_surface_builder,
        mock_topo_builder,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that both modifications and treatments can be used together."""
        # Setup basic mocks
        mock_domain.from_geodataframe.return_value.id = "test-domain"
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance

        mock_topo_instance = Mock()
        mock_topo_builder.return_value = mock_topo_instance
        mock_topo_instance.with_elevation_from_3dep.return_value = mock_topo_instance
        mock_topo_instance.build.return_value = Mock()

        mock_surface_instance = Mock()
        mock_surface_builder.return_value = mock_surface_instance
        mock_surface_instance.with_fuel_load_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_fuel_depth_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_uniform_fuel_moisture.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.build.return_value = Mock()

        mock_tree_instance = Mock()
        mock_tree_builder.return_value = mock_tree_instance
        mock_tree_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_tree_instance
        )
        mock_tree_instance.with_uniform_fuel_moisture.return_value = mock_tree_instance
        mock_tree_instance.build.return_value = Mock()

        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export
        mock_grids_instance.create_feature_grid.return_value = Mock()

        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_tree_inventory = Mock()
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            mock_tree_inventory
        )

        # Define both modifications and treatments
        modifications_config = [
            {
                "conditions": [{"attribute": "DIA", "operator": "lt", "value": 10}],
                "actions": [{"modifier": "remove"}],
            }
        ]

        treatments_config = [
            {
                "method": "proportionalThinning",
                "targetMetric": "basalArea",
                "targetValue": 25.0,
            }
        ]

        tree_inventory_config = {
            "modifications": modifications_config,
            "treatments": treatments_config,
            "seed": 42,
        }

        # Call export_roi with both modifications and treatments
        result = export_roi_to_quicfire(
            sample_roi, "/tmp/test", tree_inventory_config=tree_inventory_config
        )

        # Verify create_tree_inventory_from_treemap was called with both
        mock_inventories_instance.create_tree_inventory_from_treemap.assert_called_once()
        call_kwargs = (
            mock_inventories_instance.create_tree_inventory_from_treemap.call_args[1]
        )

        assert "modifications" in call_kwargs
        assert call_kwargs["modifications"] == modifications_config
        assert "treatments" in call_kwargs
        assert call_kwargs["treatments"] == treatments_config
        assert "seed" in call_kwargs
        assert call_kwargs["seed"] == 42
        assert result == mock_export

    @patch("fastfuels_sdk.convenience.Domain")
    @patch("fastfuels_sdk.convenience.Features")
    @patch("fastfuels_sdk.convenience.TopographyGridBuilder")
    @patch("fastfuels_sdk.convenience.SurfaceGridBuilder")
    @patch("fastfuels_sdk.convenience.TreeGridBuilder")
    @patch("fastfuels_sdk.convenience.Grids")
    @patch("fastfuels_sdk.convenience.Inventories")
    def test_no_modifications_or_treatments_by_default(
        self,
        mock_inventories,
        mock_grids,
        mock_tree_builder,
        mock_surface_builder,
        mock_topo_builder,
        mock_features,
        mock_domain,
        sample_roi,
    ):
        """Test that modifications and treatments are None by default."""
        # Setup basic mocks
        mock_domain.from_geodataframe.return_value.id = "test-domain"
        mock_features_instance = Mock()
        mock_features.from_domain_id.return_value = mock_features_instance

        mock_topo_instance = Mock()
        mock_topo_builder.return_value = mock_topo_instance
        mock_topo_instance.with_elevation_from_3dep.return_value = mock_topo_instance
        mock_topo_instance.build.return_value = Mock()

        mock_surface_instance = Mock()
        mock_surface_builder.return_value = mock_surface_instance
        mock_surface_instance.with_fuel_load_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_fuel_depth_from_landfire.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.with_uniform_fuel_moisture.return_value = (
            mock_surface_instance
        )
        mock_surface_instance.build.return_value = Mock()

        mock_tree_instance = Mock()
        mock_tree_builder.return_value = mock_tree_instance
        mock_tree_instance.with_bulk_density_from_tree_inventory.return_value = (
            mock_tree_instance
        )
        mock_tree_instance.with_uniform_fuel_moisture.return_value = mock_tree_instance
        mock_tree_instance.build.return_value = Mock()

        mock_grids_instance = Mock()
        mock_grids.from_domain_id.return_value = mock_grids_instance
        mock_export = Mock()
        mock_export.status = "completed"
        mock_grids_instance.create_export.return_value = mock_export
        mock_grids_instance.create_feature_grid.return_value = Mock()

        mock_inventories_instance = Mock()
        mock_inventories.from_domain_id.return_value = mock_inventories_instance
        mock_tree_inventory = Mock()
        mock_inventories_instance.create_tree_inventory_from_treemap.return_value = (
            mock_tree_inventory
        )

        # Call export_roi without tree_inventory_config
        result = export_roi_to_quicfire(sample_roi, "/tmp/test")

        # Verify create_tree_inventory_from_treemap was called with None for modifications and treatments
        mock_inventories_instance.create_tree_inventory_from_treemap.assert_called_once()
        call_kwargs = (
            mock_inventories_instance.create_tree_inventory_from_treemap.call_args[1]
        )

        assert "modifications" in call_kwargs
        assert call_kwargs["modifications"] is None
        assert "treatments" in call_kwargs
        assert call_kwargs["treatments"] is None
        assert result == mock_export
