"""Tests for v2 client configuration and owner-scoped API helpers."""

from http import HTTPStatus

import fastfuels_sdk.v2 as ff
import fastfuels_sdk.v2.api as api
from fastfuels_sdk.v2.client_library.models import (
    CountUsage,
    JobResourceUsage,
    Quotas,
    Usage,
    UsageCount,
    UsageLifecycle,
    UsageStorage,
    UserMeResponse,
    UserMeResponseKind,
)
from fastfuels_sdk.v2.client_library.types import Response


def _response(parsed):
    return Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=parsed,
    )


def test_get_quotas_returns_authenticated_owner_quotas(monkeypatch):
    client = object()
    quotas = Quotas(max_active_grids=3)
    owner = UserMeResponse(
        id="owner-id",
        kind=UserMeResponseKind.USER,
        tier="standard",
        quotas=quotas,
    )
    monkeypatch.setattr(api, "ensure_client", lambda: client)
    monkeypatch.setattr(
        api.get_me,
        "sync_detailed",
        lambda *, client: _response(owner),
    )

    assert ff.get_quotas() is quotas


def test_get_usage_returns_authenticated_owner_usage(monkeypatch):
    client = object()
    count = UsageCount(usage=1, limit=10)
    storage = UsageStorage(usage_bytes=1024, limit_bytes=2048)
    job_usage = JobResourceUsage(active=count, total=count, storage=storage)
    count_usage = CountUsage(total=count)
    usage = Usage(
        grids=job_usage,
        exports=job_usage,
        inventories=job_usage,
        features=job_usage,
        pointclouds=job_usage,
        domains=count_usage,
        applications=count_usage,
        api_keys=count_usage,
        lifecycle=UsageLifecycle(
            resource_ttl_days=180,
            failed_resource_ttl_days=14,
        ),
    )
    monkeypatch.setattr(api, "ensure_client", lambda: client)
    monkeypatch.setattr(
        api.get_me_usage,
        "sync_detailed",
        lambda *, client: _response(usage),
    )

    assert ff.get_usage() is usage
