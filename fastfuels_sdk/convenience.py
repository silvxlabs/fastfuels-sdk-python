"""
fastfuels_sdk/convenience.py
"""

# Core imports
from __future__ import annotations
from pathlib import Path

# Internal imports
from fastfuels_sdk.exports import Export
from fastfuels_sdk.domains import Domain
from fastfuels_sdk.grids import Grids
from fastfuels_sdk.features import Features
from fastfuels_sdk.inventories import Inventories
from fastfuels_sdk.grids import (
    TopographyGridBuilder,
    SurfaceGridBuilder,
    TreeGridBuilder,
)

# External imports
from geopandas import GeoDataFrame
import copy
from typing import Optional, Dict, Any


def _merge_config(
    default_config: Dict[str, Any], user_config: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Deep merge user configuration with default configuration.

    Args:
        default_config: The base configuration dictionary
        user_config: User-provided overrides (can be None)

    Returns:
        A new dictionary with user config merged into default config
    """
    if user_config is None:
        return copy.deepcopy(default_config)

    # Start with a deep copy of the default config
    result = copy.deepcopy(default_config)

    def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Recursively merge override dict into base dict."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                _deep_merge(base[key], value)
            else:
                # Replace value (handles primitives, lists, and new keys)
                base[key] = copy.deepcopy(value)

    _deep_merge(result, user_config)
    return result


# Default configuration constants extracted from current hardcoded values
DEFAULT_TOPOGRAPHY_CONFIG = {
    "attributes": ["elevation"],
    "elevation": {"source": "3DEP", "interpolationMethod": "linear"},
}

DEFAULT_SURFACE_CONFIG = {
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
        "value": 0.15,
        "featureMasks": ["road", "water"],
    },
}

DEFAULT_TREE_CONFIG = {
    "attributes": ["bulkDensity", "fuelMoisture"],
    "bulkDensity": {"source": "inventory"},
    "fuelMoisture": {"source": "uniform", "value": 100},
}

DEFAULT_FEATURES_CONFIG = {
    "createRoadFeatures": True,
    "createWaterFeatures": True,
    "featureGridAttributes": ["road", "water"],
}

DEFAULT_TREE_INVENTORY_CONFIG = {
    "version": "2022",
    "featureMasks": ["road", "water"],
    "canopyHeightMapSource": "Meta2024",
}


def _configure_topography_builder(domain_id: str, config: Dict[str, Any]):
    """Configure and build a topography grid based on configuration.

    Args:
        domain_id: The domain ID to create the grid for
        config: Topography configuration dictionary

    Returns:
        The built topography grid
    """
    builder = TopographyGridBuilder(domain_id=domain_id)

    # Process elevation configuration
    elevation_config = config.get("elevation", {})
    source = elevation_config.get("source")

    if source == "3DEP":
        interpolation_method = elevation_config.get("interpolationMethod", "cubic")
        builder = builder.with_elevation_from_3dep(
            interpolation_method=interpolation_method
        )
    elif source == "LANDFIRE":
        interpolation_method = elevation_config.get("interpolationMethod", "cubic")
        builder = builder.with_elevation_from_landfire(
            interpolation_method=interpolation_method
        )
    elif source == "uniform":
        value = elevation_config.get("value")
        builder = builder.with_elevation_from_uniform_value(value=value)
    else:
        raise ValueError(f"Unknown elevation source: {source}")

    return builder.build()


def _configure_surface_builder(domain_id: str, config: Dict[str, Any]):
    """Configure and build a surface grid based on configuration.

    Args:
        domain_id: The domain ID to create the grid for
        config: Surface configuration dictionary

    Returns:
        The built surface grid
    """
    builder = SurfaceGridBuilder(domain_id=domain_id)

    # Process fuel load configuration
    if "fuelLoad" in config:
        fuel_load_config = config["fuelLoad"]
        source = fuel_load_config.get("source")

        if source == "LANDFIRE":
            builder = builder.with_fuel_load_from_landfire(
                product=fuel_load_config.get("product", "FBFM40"),
                version=fuel_load_config.get("version", "2022"),
                interpolation_method=fuel_load_config.get(
                    "interpolationMethod", "cubic"
                ),
                curing_live_herbaceous=fuel_load_config.get(
                    "curingLiveHerbaceous", 0.25
                ),
                curing_live_woody=fuel_load_config.get("curingLiveWoody", 0.1),
                groups=fuel_load_config.get("groups", ["oneHour"]),
                feature_masks=fuel_load_config.get("featureMasks", []),
                remove_non_burnable=fuel_load_config.get("removeNonBurnable", []),
            )
        elif source == "uniform":
            builder = builder.with_uniform_fuel_load(
                value=fuel_load_config.get("value"),
                feature_masks=fuel_load_config.get("featureMasks", []),
            )

    # Process fuel depth configuration
    if "fuelDepth" in config:
        fuel_depth_config = config["fuelDepth"]
        source = fuel_depth_config.get("source")

        if source == "LANDFIRE":
            builder = builder.with_fuel_depth_from_landfire(
                product=fuel_depth_config.get("product", "FBFM40"),
                version=fuel_depth_config.get("version", "2022"),
                interpolation_method=fuel_depth_config.get(
                    "interpolationMethod", "cubic"
                ),
                feature_masks=fuel_depth_config.get("featureMasks", []),
                remove_non_burnable=fuel_depth_config.get("removeNonBurnable", []),
            )
        elif source == "uniform":
            builder = builder.with_uniform_fuel_depth(
                value=fuel_depth_config.get("value"),
                feature_masks=fuel_depth_config.get("featureMasks", []),
            )

    # Process fuel moisture configuration
    if "fuelMoisture" in config:
        fuel_moisture_config = config["fuelMoisture"]
        source = fuel_moisture_config.get("source")

        if source == "uniform":
            builder = builder.with_uniform_fuel_moisture(
                value=fuel_moisture_config.get("value"),
                feature_masks=fuel_moisture_config.get("featureMasks", []),
            )

    return builder.build()


def _configure_tree_builder(domain_id: str, config: Dict[str, Any]):
    """Configure and build a tree grid based on configuration.

    Args:
        domain_id: The domain ID to create the grid for
        config: Tree configuration dictionary

    Returns:
        The built tree grid
    """
    builder = TreeGridBuilder(domain_id=domain_id)

    # Process bulk density configuration
    if "bulkDensity" in config:
        bulk_density_config = config["bulkDensity"]
        source = bulk_density_config.get("source")

        if source == "inventory":
            builder = builder.with_bulk_density_from_tree_inventory()
        elif source == "uniform":
            value = bulk_density_config.get("value")
            builder = builder.with_uniform_bulk_density(value=value)

    # Process fuel moisture configuration
    if "fuelMoisture" in config:
        fuel_moisture_config = config["fuelMoisture"]
        source = fuel_moisture_config.get("source")

        if source == "uniform":
            value = fuel_moisture_config.get("value")
            builder = builder.with_uniform_fuel_moisture(value=value)

    return builder.build()


def export_roi(
    roi: GeoDataFrame,
    export_path: Path | str,
    export_format: str = "QUIC-Fire",
    verbose: bool = False,
    topography_config: Optional[Dict[str, Any]] = None,
    surface_config: Optional[Dict[str, Any]] = None,
    tree_config: Optional[Dict[str, Any]] = None,
    features_config: Optional[Dict[str, Any]] = None,
    tree_inventory_config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Export:
    """Convenience function to export a region of interest (ROI) to various formats.

    This function creates all necessary grids and resources to export spatial data
    in formats compatible with fire modeling software. It handles the complete
    workflow from domain creation through final export file generation.

    Parameters
    ----------
    roi : GeoDataFrame
        GeoDataFrame containing the region of interest geometry. Should contain
        polygon geometries defining the spatial extent for the export.
    export_path : Path or str
        File path where the export will be saved. The export is typically saved
        as a ZIP file containing all required data files.
    export_format : str, optional
        Format for the export. Supported formats:
        - "QUIC-Fire" (default): Multi-grid bundle for QUIC-Fire fire modeling
        - "zarr": Multi-grid export in zarr array format
    verbose : bool, optional
        If True, prints progress messages during the export process. Default is False.
    topography_config : dict, optional
        Configuration for topography grid creation. If None, uses default 3DEP
        elevation data with linear interpolation.

        Structure::

            {
                "attributes": ["elevation"],
                "elevation": {
                    "source": "3DEP" | "LANDFIRE" | "uniform",
                    "interpolationMethod": "linear" | "cubic" | "nearest",
                    "value": float  # Required only for uniform source
                }
            }

    surface_config : dict, optional
        Configuration for surface fuel grid creation. If None, uses default LANDFIRE
        FBFM40 (2022) data with standard curing rates and 15% fuel moisture.

        Structure::

            {
                "attributes": ["fuelLoad", "fuelDepth", "fuelMoisture"],
                "fuelLoad": {
                    "source": "LANDFIRE" | "uniform",
                    "product": "FBFM40",  # LANDFIRE product
                    "version": "2022",    # LANDFIRE version
                    "interpolationMethod": "cubic" | "linear" | "nearest",
                    "curingLiveHerbaceous": 0.25,  # 0.0-1.0
                    "curingLiveWoody": 0.1,        # 0.0-1.0
                    "groups": ["oneHour", "tenHour", ...],
                    "featureMasks": ["road", "water"],
                    "removeNonBurnable": ["NB1", "NB2", ...],
                    "value": float  # Required for uniform source
                },
                "fuelDepth": {
                    "source": "LANDFIRE" | "uniform",
                    # Similar structure to fuelLoad
                },
                "fuelMoisture": {
                    "source": "uniform",
                    "value": 0.15,  # Fuel moisture content (0.0-1.0)
                    "featureMasks": ["road", "water"]
                }
            }

    tree_config : dict, optional
        Configuration for tree canopy grid creation. If None, uses tree inventory
        data for bulk density and 100% fuel moisture.

        Structure::

            {
                "attributes": ["bulkDensity", "fuelMoisture"],
                "bulkDensity": {
                    "source": "inventory" | "uniform",
                    "value": float  # Required for uniform source
                },
                "fuelMoisture": {
                    "source": "uniform",
                    "value": 100  # Fuel moisture content
                }
            }

    features_config : dict, optional
        Configuration for geographic features creation. If None, creates both
        road and water features from OpenStreetMap data.

        Structure::

            {
                "createRoadFeatures": True,    # Create road features
                "createWaterFeatures": True,   # Create water features
                "featureGridAttributes": ["road", "water"]  # Grid attributes
            }

    tree_inventory_config : dict, optional
        Configuration for tree inventory creation. If None, uses TreeMap data
        with road and water feature masks.

        Structure::

            {
                "featureMasks": ["road", "water"],  # Features to mask out
                "canopyHeightMapSource": "Meta2024",  # High-resolution canopy height map
                "version": "2022",  # TreeMap version
                "seed": 42,  # Random seed for reproducibility
                "modifications": [  # Tree attribute modifications
                    {
                        "conditions": [{"attribute": "CR", "operator": "gt", "value": 0.1}],
                        "actions": [{"attribute": "CR", "modifier": "multiply", "value": 0.9}]
                    }
                ],
                "treatments": [  # Silvicultural treatments
                    {
                        "method": "proportionalThinning",
                        "targetMetric": "basalArea",
                        "targetValue": 25.0
                    }
                ]
            }

    Returns
    -------
    Export
        The completed export object. The export will have "completed" status,
        and the data will be saved to the specified export_path.

    Examples
    --------
    Basic usage with default settings (QUIC-Fire format):

    >>> import geopandas as gpd
    >>> from fastfuels_sdk import export_roi
    >>> roi = gpd.read_file("my_area.geojson")
    >>> export = export_roi(roi, "quicfire_export.zip")

    Export in zarr format:

    >>> export = export_roi(roi, "data_export.zip", export_format="zarr")

    Customize surface fuel moisture to 5% (dry conditions):

    >>> surface_config = {
    ...     "fuelMoisture": {
    ...         "source": "uniform",
    ...         "value": 0.05,
    ...         "featureMasks": ["road", "water"]
    ...     }
    ... }
    >>> export = export_roi(
    ...     roi, "dry_export.zip",
    ...     surface_config=surface_config
    ... )

    Use LANDFIRE 2023 data and disable water features:

    >>> surface_config = {
    ...     "fuelLoad": {"version": "2023"},
    ...     "fuelDepth": {"version": "2023"}
    ... }
    >>> features_config = {"createWaterFeatures": False}
    >>> export = export_roi(
    ...     roi, "landfire_2023.zip",
    ...     surface_config=surface_config,
    ...     features_config=features_config
    ... )

    Apply tree inventory modifications to reduce crown ratio:

    >>> tree_inventory_config = {
    ...     "modifications": [
    ...         {
    ...             "conditions": [{"attribute": "CR", "operator": "gt", "value": 0.1}],
    ...             "actions": [{"attribute": "CR", "modifier": "multiply", "value": 0.9}]
    ...         }
    ...     ]
    ... }
    >>> export = export_roi(
    ...     roi, "modified_trees.zip",
    ...     tree_inventory_config=tree_inventory_config
    ... )

    Apply silvicultural treatments and remove small trees:

    >>> tree_inventory_config = {
    ...     "modifications": [
    ...         {
    ...             "conditions": [{"attribute": "DIA", "operator": "lt", "value": 10}],
    ...             "actions": [{"attribute": "all", "modifier": "remove"}]
    ...         }
    ...     ],
    ...     "treatments": [
    ...         {
    ...             "method": "proportionalThinning",
    ...             "targetMetric": "basalArea",
    ...             "targetValue": 25.0
    ...         }
    ...     ]
    ... }
    >>> export = export_roi(
    ...     roi, "thinned_forest.zip",
    ...     tree_inventory_config=tree_inventory_config
    ... )

    Notes
    -----
    This function performs the complete export workflow:

    1. Creates a domain from the input ROI geometry
    2. Creates road and water features from OpenStreetMap (if enabled)
    3. Generates topography grid from elevation data
    4. Creates feature grid from road/water features
    5. Builds tree inventory from TreeMap data
    6. Generates surface fuel grid from LANDFIRE data
    7. Creates tree canopy grid from inventory data
    8. Exports all grids in the specified format

    All configuration parameters support partial overrides - only specify the
    values you want to change from the defaults. The function will merge your
    configuration with sensible defaults for all other parameters.

    **Tree Inventory Modifications and Treatments:**

    When both modifications and treatments are specified in tree_inventory_config,
    they are applied in the following order:

    1. **Modifications** are applied first to adjust or remove individual trees
       based on their attributes (height, diameter, crown ratio, species)
    2. **Treatments** are then applied to the modified inventory to achieve
       target stand-level metrics (basal area, density)

    Use modifications when you want to:
    - Adjust specific tree attributes (e.g., multiply heights by 0.9)
    - Remove trees matching certain criteria (e.g., diameter < 10 cm)
    - Apply expression-based conditions (e.g., crown length < 1 m)

    Use treatments when you want to:
    - Apply silvicultural operations (proportional or directional thinning)
    - Achieve target stand metrics (e.g., basal area of 25 m²/ha)
    - Simulate forest management scenarios
    """
    # Validate export format
    supported_formats = ["QUIC-Fire", "zarr"]
    if export_format not in supported_formats:
        raise ValueError(
            f"Unsupported export format: {export_format}. "
            f"Supported formats are: {', '.join(supported_formats)}"
        )

    # Merge user configurations with defaults
    merged_topography_config = _merge_config(
        DEFAULT_TOPOGRAPHY_CONFIG, topography_config
    )
    merged_surface_config = _merge_config(DEFAULT_SURFACE_CONFIG, surface_config)
    merged_tree_config = _merge_config(DEFAULT_TREE_CONFIG, tree_config)
    merged_features_config = _merge_config(DEFAULT_FEATURES_CONFIG, features_config)
    merged_tree_inventory_config = _merge_config(
        DEFAULT_TREE_INVENTORY_CONFIG, tree_inventory_config
    )

    # Create a new domain for the ROI
    if verbose:
        print("Creating domain from region of interest")
    domain = Domain.from_geodataframe(roi)

    # Create road and water features based on configuration
    features = Features.from_domain_id(domain.id)
    road_feature = None
    water_feature = None

    if merged_features_config.get("createRoadFeatures", True):
        if verbose:
            print("Creating road features for the domain")
        road_feature = features.create_road_feature_from_osm()

    if merged_features_config.get("createWaterFeatures", True):
        if verbose:
            print("Creating water features for the domain")
        water_feature = features.create_water_feature_from_osm()

    # Create topography grid using configuration
    if verbose:
        print("Creating topography grid for the domain")
    topography_grid = _configure_topography_builder(domain.id, merged_topography_config)

    # Create feature grid based on what features were created
    feature_attributes = []
    if road_feature:
        road_feature.wait_until_completed(verbose=verbose)
        feature_attributes.append("road")
    if water_feature:
        water_feature.wait_until_completed(verbose=verbose)
        feature_attributes.append("water")

    if feature_attributes:
        if verbose:
            print("Creating feature grid for the domain")
        feature_grid = Grids.from_domain_id(domain.id).create_feature_grid(
            attributes=feature_attributes
        )
    else:
        feature_grid = None

    # Create tree inventory using configuration
    if verbose:
        print("Creating tree inventory for the domain")
    tree_inventory = Inventories.from_domain_id(
        domain.id
    ).create_tree_inventory_from_treemap(
        version=merged_tree_inventory_config.get("version", "2022"),
        seed=merged_tree_inventory_config.get("seed"),
        canopy_height_map_source=merged_tree_inventory_config.get(
            "canopyHeightMapSource"
        ),
        modifications=merged_tree_inventory_config.get("modifications"),
        treatments=merged_tree_inventory_config.get("treatments"),
        feature_masks=merged_tree_inventory_config.get("featureMasks", []),
    )

    # Create surface grid using configuration
    if feature_grid:
        feature_grid.wait_until_completed(verbose=verbose)
    if verbose:
        print("Creating surface grid for the domain")
    surface_grid = _configure_surface_builder(domain.id, merged_surface_config)

    # Create tree grid using configuration
    tree_inventory.wait_until_completed(verbose=verbose)
    if verbose:
        print("Creating tree grid for the domain")
    tree_grid = _configure_tree_builder(domain.id, merged_tree_config)

    # Create Export
    topography_grid.wait_until_completed(verbose=verbose)
    surface_grid.wait_until_completed(verbose=verbose)
    tree_grid.wait_until_completed(verbose=verbose)
    export = Grids.from_domain_id(domain.id).create_export(export_format)
    export.wait_until_completed(verbose=verbose)

    # Export the data to the specified path
    if verbose:
        print(f"Exporting {export_format} data to {export_path}")
    export_path = Path(export_path) if isinstance(export_path, str) else export_path
    export.wait_until_completed(verbose=verbose, in_place=True)
    export.to_file(export_path)

    return export


def export_roi_to_quicfire(
    roi: GeoDataFrame,
    export_path: Path | str,
    verbose: bool = False,
    topography_config: Optional[Dict[str, Any]] = None,
    surface_config: Optional[Dict[str, Any]] = None,
    tree_config: Optional[Dict[str, Any]] = None,
    features_config: Optional[Dict[str, Any]] = None,
    tree_inventory_config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Export:
    """Convenience function to export a region of interest (ROI) to QUIC-Fire.

    This is a convenience wrapper around export_roi() that sets export_format
    to "QUIC-Fire". For more flexible export options including zarr format,
    use export_roi() directly.

    Parameters
    ----------
    roi : GeoDataFrame
        GeoDataFrame containing the region of interest geometry.
    export_path : Path or str
        File path where the QUIC-Fire export will be saved.
    verbose : bool, optional
        If True, prints progress messages during the export process.
    topography_config : dict, optional
        Configuration for topography grid creation. See export_roi() for details.
    surface_config : dict, optional
        Configuration for surface fuel grid creation. See export_roi() for details.
    tree_config : dict, optional
        Configuration for tree canopy grid creation. See export_roi() for details.
    features_config : dict, optional
        Configuration for geographic features creation. See export_roi() for details.
    tree_inventory_config : dict, optional
        Configuration for tree inventory creation. See export_roi() for details.

    Returns
    -------
    Export
        The completed QUIC-Fire export object.

    See Also
    --------
    export_roi : More flexible export function supporting multiple formats.

    Examples
    --------
    >>> import geopandas as gpd
    >>> from fastfuels_sdk import export_roi_to_quicfire
    >>> roi = gpd.read_file("my_area.geojson")
    >>> export = export_roi_to_quicfire(roi, "quicfire_export.zip")
    """
    return export_roi(
        roi=roi,
        export_path=export_path,
        export_format="QUIC-Fire",
        verbose=verbose,
        topography_config=topography_config,
        surface_config=surface_config,
        tree_config=tree_config,
        features_config=features_config,
        tree_inventory_config=tree_inventory_config,
        **kwargs,
    )
