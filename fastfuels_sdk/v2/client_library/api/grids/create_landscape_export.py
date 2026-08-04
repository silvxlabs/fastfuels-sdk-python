from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export import Export
from ...models.http_validation_error import HTTPValidationError
from ...models.landscape_export_request import LandscapeExportRequest
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: LandscapeExportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/exports/landscape".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Export | HTTPValidationError | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = Export.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = QuotaExceededDetail.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Export | HTTPValidationError | QuotaExceededDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    body: LandscapeExportRequest,
) -> Response[Export | HTTPValidationError | QuotaExceededDetail]:
    """Export terrain + fuel + canopy grids to a landscape GeoTIFF

     Assemble terrain, surface fuel model, and canopy grids into an
    8-band LANDFIRE-style landscape GeoTIFF for operational fire behavior
    tools (FlamMap, IFTDSS, WFDSS).

    The output `landscape.tif` carries the standard LANDFIRE band order —
    elevation, slope, aspect, fuel model, canopy cover, canopy height,
    canopy base height, canopy bulk density — with LANDFIRE's int16 scaled
    encodings, embedded CRS, and per-band name/unit metadata. This is the
    format LANDFIRE distributes and IFTDSS accepts for upload.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (LandscapeExportRequest): Request body for creating a landscape export.

            Eight required roles produce an 8-band landscape GeoTIFF in LANDFIRE band
            order: elevation, slope, aspect, fuel model, canopy cover, canopy height,
            canopy base height, canopy bulk density. This is the shape modern fire
            behavior tools consume — IFTDSS requires all eight bands for upload.

            The landscape lattice is defined by the `alignment` field — either the
            Domain bounding box tiled at `resolution` (default 30 m, LANDFIRE-native),
            or the lattice of an existing grid. Every role grid must be lattice-aligned
            to the landscape and cover its full extent; otherwise the request is
            rejected with 422. The exporter only crops oversized roles by integer
            slicing — it never resamples or reprojects. To change a grid's resolution
            or anchor, use `POST /v2/domains/{domain_id}/grids/{grid_id}/resample`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    body: LandscapeExportRequest,
) -> Export | HTTPValidationError | QuotaExceededDetail | None:
    """Export terrain + fuel + canopy grids to a landscape GeoTIFF

     Assemble terrain, surface fuel model, and canopy grids into an
    8-band LANDFIRE-style landscape GeoTIFF for operational fire behavior
    tools (FlamMap, IFTDSS, WFDSS).

    The output `landscape.tif` carries the standard LANDFIRE band order —
    elevation, slope, aspect, fuel model, canopy cover, canopy height,
    canopy base height, canopy bulk density — with LANDFIRE's int16 scaled
    encodings, embedded CRS, and per-band name/unit metadata. This is the
    format LANDFIRE distributes and IFTDSS accepts for upload.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (LandscapeExportRequest): Request body for creating a landscape export.

            Eight required roles produce an 8-band landscape GeoTIFF in LANDFIRE band
            order: elevation, slope, aspect, fuel model, canopy cover, canopy height,
            canopy base height, canopy bulk density. This is the shape modern fire
            behavior tools consume — IFTDSS requires all eight bands for upload.

            The landscape lattice is defined by the `alignment` field — either the
            Domain bounding box tiled at `resolution` (default 30 m, LANDFIRE-native),
            or the lattice of an existing grid. Every role grid must be lattice-aligned
            to the landscape and cover its full extent; otherwise the request is
            rejected with 422. The exporter only crops oversized roles by integer
            slicing — it never resamples or reprojects. To change a grid's resolution
            or anchor, use `POST /v2/domains/{domain_id}/grids/{grid_id}/resample`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError | QuotaExceededDetail
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    body: LandscapeExportRequest,
) -> Response[Export | HTTPValidationError | QuotaExceededDetail]:
    """Export terrain + fuel + canopy grids to a landscape GeoTIFF

     Assemble terrain, surface fuel model, and canopy grids into an
    8-band LANDFIRE-style landscape GeoTIFF for operational fire behavior
    tools (FlamMap, IFTDSS, WFDSS).

    The output `landscape.tif` carries the standard LANDFIRE band order —
    elevation, slope, aspect, fuel model, canopy cover, canopy height,
    canopy base height, canopy bulk density — with LANDFIRE's int16 scaled
    encodings, embedded CRS, and per-band name/unit metadata. This is the
    format LANDFIRE distributes and IFTDSS accepts for upload.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (LandscapeExportRequest): Request body for creating a landscape export.

            Eight required roles produce an 8-band landscape GeoTIFF in LANDFIRE band
            order: elevation, slope, aspect, fuel model, canopy cover, canopy height,
            canopy base height, canopy bulk density. This is the shape modern fire
            behavior tools consume — IFTDSS requires all eight bands for upload.

            The landscape lattice is defined by the `alignment` field — either the
            Domain bounding box tiled at `resolution` (default 30 m, LANDFIRE-native),
            or the lattice of an existing grid. Every role grid must be lattice-aligned
            to the landscape and cover its full extent; otherwise the request is
            rejected with 422. The exporter only crops oversized roles by integer
            slicing — it never resamples or reprojects. To change a grid's resolution
            or anchor, use `POST /v2/domains/{domain_id}/grids/{grid_id}/resample`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    body: LandscapeExportRequest,
) -> Export | HTTPValidationError | QuotaExceededDetail | None:
    """Export terrain + fuel + canopy grids to a landscape GeoTIFF

     Assemble terrain, surface fuel model, and canopy grids into an
    8-band LANDFIRE-style landscape GeoTIFF for operational fire behavior
    tools (FlamMap, IFTDSS, WFDSS).

    The output `landscape.tif` carries the standard LANDFIRE band order —
    elevation, slope, aspect, fuel model, canopy cover, canopy height,
    canopy base height, canopy bulk density — with LANDFIRE's int16 scaled
    encodings, embedded CRS, and per-band name/unit metadata. This is the
    format LANDFIRE distributes and IFTDSS accepts for upload.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (LandscapeExportRequest): Request body for creating a landscape export.

            Eight required roles produce an 8-band landscape GeoTIFF in LANDFIRE band
            order: elevation, slope, aspect, fuel model, canopy cover, canopy height,
            canopy base height, canopy bulk density. This is the shape modern fire
            behavior tools consume — IFTDSS requires all eight bands for upload.

            The landscape lattice is defined by the `alignment` field — either the
            Domain bounding box tiled at `resolution` (default 30 m, LANDFIRE-native),
            or the lattice of an existing grid. Every role grid must be lattice-aligned
            to the landscape and cover its full extent; otherwise the request is
            rejected with 422. The exporter only crops oversized roles by integer
            slicing — it never resamples or reprojects. To change a grid's resolution
            or anchor, use `POST /v2/domains/{domain_id}/grids/{grid_id}/resample`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
