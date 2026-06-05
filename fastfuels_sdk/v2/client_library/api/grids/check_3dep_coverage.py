from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.three_dep_coverage_response import ThreeDepCoverageResponse
from ...models.three_dep_resolution import ThreeDepResolution
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    *,
    resolution: ThreeDepResolution | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_resolution: int | Unset = UNSET
    if not isinstance(resolution, Unset):
        json_resolution = resolution.value

    params["resolution"] = json_resolution

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/grids/topography/3dep/coverage".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ThreeDepCoverageResponse | None:
    if response.status_code == 200:
        response_200 = ThreeDepCoverageResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ThreeDepCoverageResponse]:
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
    resolution: ThreeDepResolution | Unset = UNSET,
) -> Response[HTTPValidationError | ThreeDepCoverageResponse]:
    """Check 3DEP tile coverage for a domain

     # Check 3DEP Tile Coverage

    Immediate pre-flight check that reports which 3DEP tiles are available
    for the domain at the requested resolution. Use this before creating a
    3DEP grid to avoid waiting for async processing only to discover a
    coverage gap — especially useful for 1m (S1M) data where coverage is
    regional.

    ## Query Parameters

    - **resolution**: Resolution in meters: 1, 10, or 30. Default: 1.

    ## Response

    Returns tile availability, count, URLs, and (for 1m) acquisition dates.

    Args:
        domain_id (str):
        resolution (ThreeDepResolution | Unset): Available resolutions for 3DEP data (meters).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ThreeDepCoverageResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        resolution=resolution,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    resolution: ThreeDepResolution | Unset = UNSET,
) -> HTTPValidationError | ThreeDepCoverageResponse | None:
    """Check 3DEP tile coverage for a domain

     # Check 3DEP Tile Coverage

    Immediate pre-flight check that reports which 3DEP tiles are available
    for the domain at the requested resolution. Use this before creating a
    3DEP grid to avoid waiting for async processing only to discover a
    coverage gap — especially useful for 1m (S1M) data where coverage is
    regional.

    ## Query Parameters

    - **resolution**: Resolution in meters: 1, 10, or 30. Default: 1.

    ## Response

    Returns tile availability, count, URLs, and (for 1m) acquisition dates.

    Args:
        domain_id (str):
        resolution (ThreeDepResolution | Unset): Available resolutions for 3DEP data (meters).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ThreeDepCoverageResponse
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        resolution=resolution,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    resolution: ThreeDepResolution | Unset = UNSET,
) -> Response[HTTPValidationError | ThreeDepCoverageResponse]:
    """Check 3DEP tile coverage for a domain

     # Check 3DEP Tile Coverage

    Immediate pre-flight check that reports which 3DEP tiles are available
    for the domain at the requested resolution. Use this before creating a
    3DEP grid to avoid waiting for async processing only to discover a
    coverage gap — especially useful for 1m (S1M) data where coverage is
    regional.

    ## Query Parameters

    - **resolution**: Resolution in meters: 1, 10, or 30. Default: 1.

    ## Response

    Returns tile availability, count, URLs, and (for 1m) acquisition dates.

    Args:
        domain_id (str):
        resolution (ThreeDepResolution | Unset): Available resolutions for 3DEP data (meters).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ThreeDepCoverageResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        resolution=resolution,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    resolution: ThreeDepResolution | Unset = UNSET,
) -> HTTPValidationError | ThreeDepCoverageResponse | None:
    """Check 3DEP tile coverage for a domain

     # Check 3DEP Tile Coverage

    Immediate pre-flight check that reports which 3DEP tiles are available
    for the domain at the requested resolution. Use this before creating a
    3DEP grid to avoid waiting for async processing only to discover a
    coverage gap — especially useful for 1m (S1M) data where coverage is
    regional.

    ## Query Parameters

    - **resolution**: Resolution in meters: 1, 10, or 30. Default: 1.

    ## Response

    Returns tile availability, count, URLs, and (for 1m) acquisition dates.

    Args:
        domain_id (str):
        resolution (ThreeDepResolution | Unset): Available resolutions for 3DEP data (meters).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ThreeDepCoverageResponse
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            resolution=resolution,
        )
    ).parsed
