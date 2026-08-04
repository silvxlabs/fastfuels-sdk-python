"""
fastfuels_sdk/v2/api.py

Client configuration for the FastFuels v2 API: API key management and the
shared HTTP client used by the wrapper modules.
"""

import os
from typing import Optional

# DEFAULT_BASE_URL is recorded by generate_client.sh alongside the generated
# client (openapi-python-client embeds no server URL). It is the Cloud Run
# deployment for now — a stable domain should front it before GA (tracked in
# #176); until then FASTFUELS_API_V2_URL overrides it without an SDK upgrade.
from fastfuels_sdk.v2.client_library.base_url import DEFAULT_BASE_URL
from fastfuels_sdk.v2.client_library.api.users import get_me, get_me_usage
from fastfuels_sdk.v2.client_library.client import AuthenticatedClient
from fastfuels_sdk.v2.client_library.models import Quotas, Usage
from fastfuels_sdk.v2.exceptions import expect

_client: Optional[AuthenticatedClient] = None


def set_api_key(api_key: str) -> None:
    """Set the API key for the FastFuels v2 SDK.

    This invalidates the cached client, ensuring that subsequent API calls
    use the new credentials.

    Parameters
    ----------
    api_key : str
        The API key to use for authentication.
    """
    global _client
    _client = None
    os.environ["FASTFUELS_API_KEY"] = api_key


def get_client() -> Optional[AuthenticatedClient]:
    """Get the current API client, creating one if necessary.

    The API key is read from:

    1. The cached client, if :func:`set_api_key` was called
    2. The ``FASTFUELS_API_KEY`` environment variable

    Returns
    -------
    Optional[AuthenticatedClient]
        The client instance, or None if no API key is configured.
    """
    global _client

    if _client is not None:
        return _client

    # v1 and v2 are separate deployments with separate keys, but both read
    # FASTFUELS_API_KEY: running both versions in one process with different
    # keys is not a supported use case, so a single variable suffices.
    api_key = os.getenv("FASTFUELS_API_KEY")
    if not api_key:
        return None

    _client = AuthenticatedClient(
        base_url=os.getenv("FASTFUELS_API_V2_URL", DEFAULT_BASE_URL),
        token=api_key,
        prefix="",  # raw key, not "Bearer <key>"
        auth_header_name="api-key",
        # Error translation happens in one place — exceptions.expect() on
        # sync_detailed() responses — so the generated client must hand back
        # undocumented statuses (e.g. 404) instead of raising its own
        # UnexpectedStatus.
        raise_on_unexpected_status=False,
    )

    return _client


def ensure_client() -> AuthenticatedClient:
    """Ensure an API client is configured and return it.

    Returns
    -------
    AuthenticatedClient
        The client instance.

    Raises
    ------
    RuntimeError
        If no API key is configured.
    """
    client = get_client()
    if client is None:
        raise RuntimeError(
            "FastFuels API key not configured. Please either:\n"
            "  1. Set the FASTFUELS_API_KEY environment variable, or\n"
            "  2. Call fastfuels_sdk.v2.api.set_api_key('your-api-key') "
            "before making API calls"
        )
    return client


def get_quotas() -> Quotas:
    """Return the authenticated owner's resolved quotas.

    Returns
    -------
    Quotas
        Count, concurrency, storage, dispatch, and retention limits for the
        owner authenticated by the current API key.

    Raises
    ------
    RuntimeError
        If no API key is configured.
    ApiException
        If the API request fails.
    """
    owner = expect(get_me.sync_detailed(client=ensure_client()))
    return owner.quotas


def get_usage() -> Usage:
    """Return the authenticated owner's current usage and limits.

    Returns
    -------
    Usage
        Usage for job resources, count-only resources, storage, and the
        owner's resource-retention policy.

    Raises
    ------
    RuntimeError
        If no API key is configured.
    ApiException
        If the API request fails.
    """
    return expect(get_me_usage.sync_detailed(client=ensure_client()))
