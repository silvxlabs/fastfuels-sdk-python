from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.point_cloud_three_dep_coverage_response import (
    PointCloudThreeDepCoverageResponse,
)
from ...types import Response


def _get_kwargs(
    domain_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/pointclouds/3dep/coverage".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PointCloudThreeDepCoverageResponse | None:
    if response.status_code == 200:
        response_200 = PointCloudThreeDepCoverageResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PointCloudThreeDepCoverageResponse]:
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
) -> Response[HTTPValidationError | PointCloudThreeDepCoverageResponse]:
    """Check 3DEP lidar coverage for a domain

     # Check 3DEP Lidar Coverage

    Immediate pre-flight check reporting which USGS 3DEP lidar surveys are
    available for this domain, how much of it they cover, and roughly how many
    points a fetch would return. Use it before creating a 3DEP point cloud to
    avoid waiting on a background job only to find a coverage gap — 3DEP is
    regional, and survey boundaries are irregular.

    This checks lidar point clouds. Elevation raster coverage is a separate
    product with its own check at
    `GET /domains/{domain_id}/grids/topography/3dep/coverage`.

    ## Response

    Reports whether any lidar is available, the fraction of the domain covered,
    the surveys that would be read with what each contributes, and roughly how
    many points a fetch would return. `datasets[].name` values can be passed as
    `datasets` when creating the point cloud to pin the fetch.

    ## Error Responses

    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudThreeDepCoverageResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PointCloudThreeDepCoverageResponse | None:
    """Check 3DEP lidar coverage for a domain

     # Check 3DEP Lidar Coverage

    Immediate pre-flight check reporting which USGS 3DEP lidar surveys are
    available for this domain, how much of it they cover, and roughly how many
    points a fetch would return. Use it before creating a 3DEP point cloud to
    avoid waiting on a background job only to find a coverage gap — 3DEP is
    regional, and survey boundaries are irregular.

    This checks lidar point clouds. Elevation raster coverage is a separate
    product with its own check at
    `GET /domains/{domain_id}/grids/topography/3dep/coverage`.

    ## Response

    Reports whether any lidar is available, the fraction of the domain covered,
    the surveys that would be read with what each contributes, and roughly how
    many points a fetch would return. `datasets[].name` values can be passed as
    `datasets` when creating the point cloud to pin the fetch.

    ## Error Responses

    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudThreeDepCoverageResponse
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | PointCloudThreeDepCoverageResponse]:
    """Check 3DEP lidar coverage for a domain

     # Check 3DEP Lidar Coverage

    Immediate pre-flight check reporting which USGS 3DEP lidar surveys are
    available for this domain, how much of it they cover, and roughly how many
    points a fetch would return. Use it before creating a 3DEP point cloud to
    avoid waiting on a background job only to find a coverage gap — 3DEP is
    regional, and survey boundaries are irregular.

    This checks lidar point clouds. Elevation raster coverage is a separate
    product with its own check at
    `GET /domains/{domain_id}/grids/topography/3dep/coverage`.

    ## Response

    Reports whether any lidar is available, the fraction of the domain covered,
    the surveys that would be read with what each contributes, and roughly how
    many points a fetch would return. `datasets[].name` values can be passed as
    `datasets` when creating the point cloud to pin the fetch.

    ## Error Responses

    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudThreeDepCoverageResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PointCloudThreeDepCoverageResponse | None:
    """Check 3DEP lidar coverage for a domain

     # Check 3DEP Lidar Coverage

    Immediate pre-flight check reporting which USGS 3DEP lidar surveys are
    available for this domain, how much of it they cover, and roughly how many
    points a fetch would return. Use it before creating a 3DEP point cloud to
    avoid waiting on a background job only to find a coverage gap — 3DEP is
    regional, and survey boundaries are irregular.

    This checks lidar point clouds. Elevation raster coverage is a separate
    product with its own check at
    `GET /domains/{domain_id}/grids/topography/3dep/coverage`.

    ## Response

    Reports whether any lidar is available, the fraction of the domain covered,
    the surveys that would be read with what each contributes, and roughly how
    many points a fetch would return. `datasets[].name` values can be passed as
    `datasets` when creating the point cloud to pin the fetch.

    ## Error Responses

    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudThreeDepCoverageResponse
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
        )
    ).parsed
