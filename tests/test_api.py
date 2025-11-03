"""
Tests for API initialization and lazy loading.

These tests verify that:
1. The SDK can be imported without FASTFUELS_API_KEY env var (Issue #112)
2. The set_api_key() function properly updates all API clients (Issue #98)
"""

import os
import pytest


@pytest.fixture(autouse=True)
def cleanup_api_state():
    """Fixture to clean up API state after each test."""
    # Store original state
    original_env_key = os.environ.get("FASTFUELS_API_KEY")

    yield

    # Restore original environment variable
    if original_env_key:
        os.environ["FASTFUELS_API_KEY"] = original_env_key
        # Reset the client to use the original key
        from fastfuels_sdk import api

        api._client = None
        # Trigger recreation with original key
        api.get_client()
    else:
        os.environ.pop("FASTFUELS_API_KEY", None)
        from fastfuels_sdk import api

        api._client = None


def test_import_without_env_var():
    """Test that the SDK can be imported without FASTFUELS_API_KEY set.

    This addresses Issue #112: Package import fails if fastfuels key not set as an environment variable.

    The SDK should allow imports without requiring the API key to be set upfront.
    Users should be able to set the API key programmatically after import.
    """
    # Save current env var state
    original_key = os.environ.pop("FASTFUELS_API_KEY", None)

    try:
        # These imports should not raise RuntimeError
        from fastfuels_sdk import api
        from fastfuels_sdk import Domain
        from fastfuels_sdk import Inventories
        from fastfuels_sdk import Features
        from fastfuels_sdk import Grids
        from fastfuels_sdk import Export

        # Import should succeed
        assert api is not None
        assert Domain is not None
        assert Inventories is not None
        assert Features is not None
        assert Grids is not None
        assert Export is not None

    finally:
        # Restore env var
        if original_key:
            os.environ["FASTFUELS_API_KEY"] = original_key


def test_api_call_without_key_raises_error():
    """Test that API calls without setting a key raise helpful error."""
    # Save current env var state
    original_key = os.environ.pop("FASTFUELS_API_KEY", None)

    try:
        from fastfuels_sdk import api

        # Clear any cached client and API instances
        api._client = None
        api._domains_api = None

        # Attempting to use the API without a key should raise RuntimeError
        with pytest.raises(RuntimeError) as exc_info:
            api.get_domains_api()

        # Check that error message is helpful
        error_msg = str(exc_info.value)
        assert "API key not configured" in error_msg
        assert "set_api_key" in error_msg or "FASTFUELS_API_KEY" in error_msg

    finally:
        # Restore env var
        if original_key:
            os.environ["FASTFUELS_API_KEY"] = original_key


def test_set_api_key_updates_client():
    """Test that set_api_key() creates a new client and invalidates caches.

    This addresses Issue #98: Fix set_api_key function not updating the api key.

    When set_api_key() is called, it should:
    1. Create a new client with the new API key
    2. Invalidate all cached API instances
    3. Ensure subsequent API calls use the new key
    """
    from fastfuels_sdk import api

    # Set initial API key
    api.set_api_key("test-key-1")

    # Get initial client
    client1 = api.get_client()
    assert client1 is not None
    assert client1.default_headers["api-key"] == "test-key-1"

    # Create a domain API instance with first key
    domain_api1 = api.get_domains_api()
    assert domain_api1 is not None

    # Set new API key
    api.set_api_key("test-key-2")

    # Get new client - should be different
    client2 = api.get_client()
    assert client2 is not None
    assert client2 is not client1  # Should be a new instance
    assert client2.default_headers["api-key"] == "test-key-2"

    # Verify cached domain API was invalidated
    assert api._domains_api is None

    # Get new domain API - should use new client
    domain_api2 = api.get_domains_api()
    assert domain_api2 is not None
    assert domain_api2 is not domain_api1  # Should be a new instance
    assert domain_api2.api_client.default_headers["api-key"] == "test-key-2"


def test_invalidation_affects_all_modules():
    """Test that set_api_key() invalidates cached APIs in all modules."""
    from fastfuels_sdk import api

    # Set initial API key and trigger lazy loading of all API instances
    api.set_api_key("test-key-initial")

    api.get_domains_api()
    api.get_inventories_api()
    api.get_tree_inventory_api()
    api.get_features_api()
    api.get_road_feature_api()
    api.get_water_feature_api()
    api.get_grids_api()
    api.get_tree_grid_api()
    api.get_surface_grid_api()
    api.get_topography_grid_api()
    api.get_feature_grid_api()

    # Verify all API instances have been cached
    assert api._domains_api is not None
    assert api._inventories_api is not None
    assert api._tree_inventory_api is not None
    assert api._features_api is not None
    assert api._road_feature_api is not None
    assert api._water_feature_api is not None
    assert api._grids_api is not None
    assert api._tree_grid_api is not None
    assert api._surface_grid_api is not None
    assert api._topography_grid_api is not None
    assert api._feature_grid_api is not None

    # Set new API key
    api.set_api_key("test-key-new")

    # Verify all cached instances were invalidated
    assert api._domains_api is None
    assert api._inventories_api is None
    assert api._tree_inventory_api is None
    assert api._features_api is None
    assert api._road_feature_api is None
    assert api._water_feature_api is None
    assert api._grids_api is None
    assert api._tree_grid_api is None
    assert api._surface_grid_api is None
    assert api._topography_grid_api is None
    assert api._feature_grid_api is None


def test_programmatic_api_key_setting():
    """Test the use case from Issue #112: setting API key programmatically."""
    # This is the use case that was broken before the fix

    # Remove env var to simulate user without env var set
    original_key = os.environ.pop("FASTFUELS_API_KEY", None)

    try:
        # Import should work without env var
        from fastfuels_sdk import api  # noqa: F401
        from fastfuels_sdk import Domain  # noqa: F401

        # Set API key programmatically
        api.set_api_key("my-programmatic-key")

        # Verify client was created with correct key
        client = api.get_client()
        assert client is not None
        assert client.default_headers["api-key"] == "my-programmatic-key"

    finally:
        # Restore env var
        if original_key:
            os.environ["FASTFUELS_API_KEY"] = original_key


def test_env_var_takes_effect_on_first_use():
    """Test that FASTFUELS_API_KEY env var is used on first API call."""
    # Set env var
    os.environ["FASTFUELS_API_KEY"] = "env-var-key"

    try:
        from fastfuels_sdk import api

        # Clear any cached client
        api._client = None

        # First call should use env var
        client = api.get_client()
        assert client is not None
        assert client.default_headers["api-key"] == "env-var-key"

    finally:
        # Clean up
        os.environ.pop("FASTFUELS_API_KEY", None)


def test_set_api_key_overrides_env_var():
    """Test that set_api_key() overrides FASTFUELS_API_KEY env var."""
    # Set env var
    os.environ["FASTFUELS_API_KEY"] = "env-var-key"

    try:
        from fastfuels_sdk import api

        # Clear any cached client
        api._client = None

        # First use env var
        client1 = api.get_client()
        assert client1.default_headers["api-key"] == "env-var-key"

        # Override with set_api_key
        api.set_api_key("override-key")

        # Should now use override key
        client2 = api.get_client()
        assert client2.default_headers["api-key"] == "override-key"

    finally:
        # Clean up
        os.environ.pop("FASTFUELS_API_KEY", None)
