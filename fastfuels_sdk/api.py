"""
fastfuels_sdk/api.py
"""

import os
from typing import Optional

from fastfuels_sdk.client_library.api_client import ApiClient
from fastfuels_sdk.client_library.api import (
    DomainsApi,
    InventoriesApi,
    TreeInventoryApi,
    FeaturesApi,
    RoadFeatureApi,
    WaterFeatureApi,
    GridsApi,
    TreeGridApi,
    SurfaceGridApi,
    TopographyGridApi,
    FeatureGridApi,
)

_client: Optional[ApiClient] = None
_domains_api: Optional[DomainsApi] = None
_inventories_api: Optional[InventoriesApi] = None
_tree_inventory_api: Optional[TreeInventoryApi] = None
_features_api: Optional[FeaturesApi] = None
_road_feature_api: Optional[RoadFeatureApi] = None
_water_feature_api: Optional[WaterFeatureApi] = None
_grids_api: Optional[GridsApi] = None
_tree_grid_api: Optional[TreeGridApi] = None
_surface_grid_api: Optional[SurfaceGridApi] = None
_topography_grid_api: Optional[TopographyGridApi] = None
_feature_grid_api: Optional[FeatureGridApi] = None


def set_api_key(api_key: str) -> None:
    """Set the API key for the FastFuels SDK.

    This will invalidate the cached API client and all API instances,
    ensuring that subsequent API calls use the new credentials.

    Args:
        api_key: The API key to use for authentication
    """
    global _client, _domains_api, _inventories_api, _tree_inventory_api
    global _features_api, _road_feature_api, _water_feature_api
    global _grids_api, _tree_grid_api, _surface_grid_api, _topography_grid_api, _feature_grid_api

    _client = None
    _domains_api = None
    _inventories_api = None
    _tree_inventory_api = None
    _features_api = None
    _road_feature_api = None
    _water_feature_api = None
    _grids_api = None
    _tree_grid_api = None
    _surface_grid_api = None
    _topography_grid_api = None
    _feature_grid_api = None

    os.environ["FASTFUELS_API_KEY"] = api_key


def get_client() -> Optional[ApiClient]:
    """Get the current API client, creating one if necessary.

    This function will attempt to get the API client from:
    1. The existing _client instance if set_api_key() was called
    2. The FASTFUELS_API_KEY environment variable

    Returns:
        The ApiClient instance, or None if no API key is configured
    """
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("FASTFUELS_API_KEY")
    if not api_key:
        return None

    config = {
        "header_name": "api-key",
        "header_value": api_key,
    }

    _client = ApiClient(**config)

    return _client


def ensure_client() -> ApiClient:
    """Ensure an API client is configured and return it.

    This function will raise a RuntimeError with a helpful message if no
    API key has been configured.

    Returns:
        The ApiClient instance

    Raises:
        RuntimeError: If no API key is configured
    """
    client = get_client()
    if client is None:
        raise RuntimeError(
            "FastFuels API key not configured. Please either:\n"
            "  1. Set the FASTFUELS_API_KEY environment variable, or\n"
            "  2. Call fastfuels_sdk.api.set_api_key('your-api-key') before making API calls"
        )
    return client


def get_domains_api() -> DomainsApi:
    """Get the cached DomainsApi instance, creating it if necessary.

    Returns:
        The DomainsApi instance
    """
    global _domains_api
    if _domains_api is None:
        _domains_api = DomainsApi(ensure_client())
    return _domains_api


def get_inventories_api() -> InventoriesApi:
    """Get the cached InventoriesApi instance, creating it if necessary.

    Returns:
        The InventoriesApi instance
    """
    global _inventories_api
    if _inventories_api is None:
        _inventories_api = InventoriesApi(ensure_client())
    return _inventories_api


def get_tree_inventory_api() -> TreeInventoryApi:
    """Get the cached TreeInventoryApi instance, creating it if necessary.

    Returns:
        The TreeInventoryApi instance
    """
    global _tree_inventory_api
    if _tree_inventory_api is None:
        _tree_inventory_api = TreeInventoryApi(ensure_client())
    return _tree_inventory_api


def get_features_api() -> FeaturesApi:
    """Get the cached FeaturesApi instance, creating it if necessary.

    Returns:
        The FeaturesApi instance
    """
    global _features_api
    if _features_api is None:
        _features_api = FeaturesApi(ensure_client())
    return _features_api


def get_road_feature_api() -> RoadFeatureApi:
    """Get the cached RoadFeatureApi instance, creating it if necessary.

    Returns:
        The RoadFeatureApi instance
    """
    global _road_feature_api
    if _road_feature_api is None:
        _road_feature_api = RoadFeatureApi(ensure_client())
    return _road_feature_api


def get_water_feature_api() -> WaterFeatureApi:
    """Get the cached WaterFeatureApi instance, creating it if necessary.

    Returns:
        The WaterFeatureApi instance
    """
    global _water_feature_api
    if _water_feature_api is None:
        _water_feature_api = WaterFeatureApi(ensure_client())
    return _water_feature_api


def get_grids_api() -> GridsApi:
    """Get the cached GridsApi instance, creating it if necessary.

    Returns:
        The GridsApi instance
    """
    global _grids_api
    if _grids_api is None:
        _grids_api = GridsApi(ensure_client())
    return _grids_api


def get_tree_grid_api() -> TreeGridApi:
    """Get the cached TreeGridApi instance, creating it if necessary.

    Returns:
        The TreeGridApi instance
    """
    global _tree_grid_api
    if _tree_grid_api is None:
        _tree_grid_api = TreeGridApi(ensure_client())
    return _tree_grid_api


def get_surface_grid_api() -> SurfaceGridApi:
    """Get the cached SurfaceGridApi instance, creating it if necessary.

    Returns:
        The SurfaceGridApi instance
    """
    global _surface_grid_api
    if _surface_grid_api is None:
        _surface_grid_api = SurfaceGridApi(ensure_client())
    return _surface_grid_api


def get_topography_grid_api() -> TopographyGridApi:
    """Get the cached TopographyGridApi instance, creating it if necessary.

    Returns:
        The TopographyGridApi instance
    """
    global _topography_grid_api
    if _topography_grid_api is None:
        _topography_grid_api = TopographyGridApi(ensure_client())
    return _topography_grid_api


def get_feature_grid_api() -> FeatureGridApi:
    """Get the cached FeatureGridApi instance, creating it if necessary.

    Returns:
        The FeatureGridApi instance
    """
    global _feature_grid_api
    if _feature_grid_api is None:
        _feature_grid_api = FeatureGridApi(ensure_client())
    return _feature_grid_api
