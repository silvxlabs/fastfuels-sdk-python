"""Tests for v2 API error translation."""

import datetime
import json
from http import HTTPStatus

import pytest

from fastfuels_sdk.v2.client_library.models import QuotaExceededDetail
from fastfuels_sdk.v2.client_library.types import Response
from fastfuels_sdk.v2.exceptions import QuotaExceededException, expect


def _quota_response(detail, *, parsed=True, retry_after=None):
    headers = {}
    if retry_after is not None:
        headers["Retry-After"] = str(retry_after)
    return Response(
        status_code=HTTPStatus.TOO_MANY_REQUESTS,
        content=json.dumps({"detail": detail.to_dict()}).encode(),
        headers=headers,
        parsed=detail if parsed else None,
    )


def test_quota_exceeded_exception_exposes_structured_detail():
    detail = QuotaExceededDetail(
        quota="max_active_grids",
        current=25,
        limit=25,
        message="Too many active grid jobs.",
    )

    with pytest.raises(QuotaExceededException) as exc_info:
        expect(_quota_response(detail, retry_after=60), HTTPStatus.CREATED)

    error = exc_info.value
    assert error.status_code == HTTPStatus.TOO_MANY_REQUESTS
    assert error.detail is detail
    assert error.quota == "max_active_grids"
    assert error.current == 25
    assert error.limit == 25
    assert error.window_reset_on is None
    assert error.message == "Too many active grid jobs."
    assert error.reason == "QUOTA_EXCEEDED"
    assert error.retry_after == 60
    assert str(error) == "(429) Too many active grid jobs."


def test_quota_exceeded_exception_parses_raw_response_content():
    reset = datetime.datetime(2026, 8, 10, tzinfo=datetime.timezone.utc)
    detail = QuotaExceededDetail(
        quota="max_weekly_grid_dispatches",
        current=500,
        limit=500,
        window_reset_on=reset,
        message="Weekly grid dispatch quota reached.",
    )

    with pytest.raises(QuotaExceededException) as exc_info:
        expect(_quota_response(detail, parsed=False), HTTPStatus.CREATED)

    error = exc_info.value
    assert error.quota == "max_weekly_grid_dispatches"
    assert error.window_reset_on == reset
    assert error.message == "Weekly grid dispatch quota reached."
    assert error.retry_after is None


def test_generated_quota_parser_accepts_fastapi_detail_envelope():
    detail = QuotaExceededDetail.from_dict(
        {
            "detail": {
                "quota": "max_grids",
                "current": 1000,
                "limit": 1000,
                "message": "Grid quota reached.",
            }
        }
    )

    assert detail.quota == "max_grids"
    assert detail.message == "Grid quota reached."
