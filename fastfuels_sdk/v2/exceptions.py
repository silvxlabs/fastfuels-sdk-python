"""
fastfuels_sdk/v2/exceptions.py

Typed exceptions for the FastFuels v2 SDK.

Every API error surfaces as a subclass of :class:`ApiException` carrying
the HTTP status code and the error detail reported by the API.
"""

import json
from collections.abc import Mapping
from http import HTTPStatus
from typing import Any, NoReturn

from fastfuels_sdk.v2.client_library.models import (
    HTTPValidationError,
    QuotaExceededDetail,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Response

# Implementation note: the generated client (openapi-python-client) does
# not raise per-status exceptions — documented error responses are
# *returned* as parsed models and undocumented statuses are only surfaced
# through the raw ``Response`` object. The wrapper modules therefore call
# the generated ``sync_detailed()`` endpoints (the shared client is created
# with ``raise_on_unexpected_status=False``) and funnel every ``Response``
# through ``expect()``, the single choke point where errors become
# exceptions.

# The v2 API raises some 422s with a plain-string ``detail`` (e.g. invalid
# EPSG codes), while the OpenAPI spec types ``detail`` as a list of
# validation errors. The generated parser crashes on the string form
# *inside* sync_detailed(), before the wrapper can translate the response,
# so wrap it to tolerate undocumented body shapes; the actual detail is
# re-read from ``response.content`` in ``raise_for_response()``.
_generated_from_dict = HTTPValidationError.from_dict.__func__
_generated_quota_from_dict = QuotaExceededDetail.from_dict.__func__


def _tolerant_from_dict(cls, src_dict):
    try:
        return _generated_from_dict(cls, src_dict)
    except (TypeError, ValueError):
        model = cls()
        if isinstance(src_dict, Mapping):
            model.additional_properties = dict(src_dict)
        return model


HTTPValidationError.from_dict = classmethod(_tolerant_from_dict)


def _quota_from_dict(cls, src_dict):
    """Unwrap FastAPI's ``detail`` envelope before generated parsing."""
    if isinstance(src_dict, Mapping) and isinstance(src_dict.get("detail"), Mapping):
        src_dict = src_dict["detail"]
    return _generated_quota_from_dict(cls, src_dict)


QuotaExceededDetail.from_dict = classmethod(_quota_from_dict)


class ApiException(Exception):
    """Base exception for FastFuels v2 API errors.

    Attributes
    ----------
    status_code : int
        The HTTP status code returned by the API.
    detail : Any
        The error detail extracted from the response body (FastAPI's
        ``detail`` field when present, otherwise the raw response text).
    """

    def __init__(self, status_code: int, detail: Any = None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"({status_code}) {detail}")


class BadRequestException(ApiException):
    """Raised when the API returns 400 Bad Request."""


class UnauthorizedException(ApiException):
    """Raised when the API returns 401 Unauthorized (invalid API key)."""


class ForbiddenException(ApiException):
    """Raised when the API returns 403 Forbidden."""


class NotFoundException(ApiException):
    """Raised when the API returns 404 Not Found.

    The v2 API returns 404 both for missing resources and for ownership
    mismatches, to avoid leaking information about resource existence.
    """


class UnprocessableEntityException(ApiException):
    """Raised when the API returns 422 Unprocessable Entity.

    The ``detail`` attribute carries FastAPI's validation error detail:
    either a human-readable message or a list of per-field errors.
    """


class QuotaExceededException(ApiException):
    """Raised when the API returns 429 Too Many Requests.

    Attributes
    ----------
    quota : str or None
        The quota field that was exceeded.
    current : int or None
        The owner's current usage for the quota.
    limit : int or None
        The quota limit that was reached.
    window_reset_on : datetime.datetime or None
        When a windowed quota resets, if applicable.
    message : str or None
        A human-readable explanation and suggested next steps.
    reason : str or None
        The machine-readable error reason.
    retry_after : int or None
        Seconds the API recommends waiting before retrying. Present only for
        active-job quota rejections.
    """

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        retry_after: int | None = None,
    ):
        self.quota = None
        self.current = None
        self.limit = None
        self.window_reset_on = None
        self.message = None
        self.reason = None
        self.retry_after = retry_after

        if isinstance(detail, QuotaExceededDetail):
            self.quota = detail.quota
            self.current = detail.current
            self.limit = detail.limit
            if detail.window_reset_on is not UNSET:
                self.window_reset_on = detail.window_reset_on
            self.message = detail.message
            if detail.reason is not UNSET:
                self.reason = detail.reason

        self.status_code = status_code
        self.detail = detail
        Exception.__init__(self, f"({status_code}) {self.message or detail}")


class ServiceException(ApiException):
    """Raised when the API returns a 5xx server error."""


_STATUS_TO_EXCEPTION = {
    HTTPStatus.BAD_REQUEST: BadRequestException,
    HTTPStatus.UNAUTHORIZED: UnauthorizedException,
    HTTPStatus.FORBIDDEN: ForbiddenException,
    HTTPStatus.NOT_FOUND: NotFoundException,
    HTTPStatus.TOO_MANY_REQUESTS: QuotaExceededException,
    HTTPStatus.UNPROCESSABLE_ENTITY: UnprocessableEntityException,
}


def _extract_detail(response: Response) -> Any:
    """Pull FastAPI's ``detail`` field out of an error response body."""
    try:
        return json.loads(response.content)["detail"]
    except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
        return (
            response.content.decode(errors="ignore")
            or HTTPStatus(response.status_code).phrase
        )


def _extract_quota_detail(response: Response) -> Any:
    """Return a typed quota detail, falling back to the generic detail."""
    if isinstance(response.parsed, QuotaExceededDetail):
        return response.parsed

    try:
        payload = json.loads(response.content)
        if isinstance(payload, Mapping) and isinstance(payload.get("detail"), Mapping):
            payload = payload["detail"]
        if isinstance(payload, Mapping):
            return QuotaExceededDetail.from_dict(payload)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        pass

    return _extract_detail(response)


def _extract_retry_after(response: Response) -> int | None:
    """Return the delta-seconds value from ``Retry-After``, when present."""
    value = response.headers.get("Retry-After")
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None


def raise_for_response(response: Response) -> NoReturn:
    """Translate an error ``Response`` into a typed SDK exception.

    Parameters
    ----------
    response : Response
        A response from a generated ``sync_detailed()`` endpoint call.

    Raises
    ------
    BadRequestException
        If the response status is 400.
    UnauthorizedException
        If the response status is 401.
    ForbiddenException
        If the response status is 403.
    NotFoundException
        If the response status is 404.
    QuotaExceededException
        If the response status is 429.
    UnprocessableEntityException
        If the response status is 422.
    ServiceException
        If the response status is 5xx.
    ApiException
        For any other unexpected status.
    """
    status_code = int(response.status_code)
    exception_class = _STATUS_TO_EXCEPTION.get(response.status_code)
    if exception_class is None:
        exception_class = ServiceException if status_code >= 500 else ApiException
    detail = (
        _extract_quota_detail(response)
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS
        else _extract_detail(response)
    )
    if exception_class is QuotaExceededException:
        raise exception_class(
            status_code,
            detail,
            retry_after=_extract_retry_after(response),
        )
    raise exception_class(status_code, detail)


def expect(response: Response, expected_status: HTTPStatus = HTTPStatus.OK) -> Any:
    """Return a response's parsed body, raising typed exceptions on error.

    Parameters
    ----------
    response : Response
        A response from a generated ``sync_detailed()`` endpoint call.
    expected_status : HTTPStatus, optional
        The success status documented for the endpoint (default 200 OK;
        pass ``HTTPStatus.NO_CONTENT`` for deletes).

    Returns
    -------
    Any
        ``response.parsed`` — the generated success model (``None`` for
        204 No Content).

    Raises
    ------
    ApiException
        A subclass matching the response status (see
        :func:`raise_for_response`) when it differs from
        ``expected_status``.
    """
    if response.status_code == expected_status:
        return response.parsed
    raise_for_response(response)
