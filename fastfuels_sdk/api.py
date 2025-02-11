"""
fastfuels_sdk/api.py
"""

import os
from typing import Optional

from fastfuels_sdk.client_library.api_client import ApiClient

_client: Optional[ApiClient] = None


def set_api_key(api_key: str) -> None:
    global _client

    config = {
        "header_name": "api-key",
        "header_value": api_key,
    }

    _client = ApiClient(**config)


def get_client() -> ApiClient:
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("FASTFUELS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "FASTFUELS_API_KEY environment variable not set. "
            "Please set this variable with your API key."
        )
    config = {
        "header_name": "api-key",
        "header_value": api_key,
    }

    _client = ApiClient(**config)

    return _client
