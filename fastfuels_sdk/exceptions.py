"""
exceptions.py

Custom exceptions and exception handling for the FastFuels SDK.
"""

import json
from http import HTTPStatus
from client_library_a.types import Response
from client_library_a.errors import UnexpectedStatus


class AuthenticationError(Exception):
    """Raised when authentication fails"""

    def __init__(self):
        super().__init__(
            "Authentication failed. "
            "\nPlease ensure that the FASTFUELS_API_KEY environment variable is set with a valid API key."
        )


class ValidationError(Exception):
    """Raised when request validation fails"""

    def __init__(self, content):
        super().__init__(content)


def handle_response_status_code(response: Response, expected_status: int) -> None:
    """
    Check response status and raise appropriate exceptions.

    Args:
        response: Response from API call
        expected_status: Expected HTTP status code for success

    Raises:
        AuthenticationError: If authentication fails (401)
        ValidationError: If request validation fails (422)
        UnexpectedStatus: For other unexpected status codes
    """
    if response.status_code == expected_status:
        return

    try:
        error_detail = json.loads(response.content)["detail"]
    except (json.JSONDecodeError, KeyError):
        error_detail = response.content.decode("utf-8")

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise AuthenticationError()
    elif response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        raise ValidationError(error_detail)
    else:
        raise UnexpectedStatus(response.status_code, error_detail)
