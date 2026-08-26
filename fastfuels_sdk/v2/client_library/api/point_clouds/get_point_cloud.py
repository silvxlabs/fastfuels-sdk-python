from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.point_cloud import PointCloud
from ...types import Response


def _get_kwargs(
    domain_id: str,
    point_cloud_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/pointclouds/{point_cloud_id}".format(
            domain_id=quote(str(domain_id), safe=""),
            point_cloud_id=quote(str(point_cloud_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PointCloud | None:
    if response.status_code == 200:
        response_200 = PointCloud.from_dict(response.json())

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
) -> Response[HTTPValidationError | PointCloud]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | PointCloud]:
    r"""Get a point cloud by ID

     # Get a Point Cloud

    Returns one point-cloud resource by ID. This endpoint returns resource
    metadata and processing state; it does not return the individual points.
    Use `/data/metadata` and the tile data endpoints for point values after the
    resource reaches `status=\"completed\"`.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    The complete point-cloud resource, including its acquisition `type`,
    `source` provenance, processing `status`, georeference, content summary,
    checksum, and user-editable metadata. Derived fields such as `georeference`
    and `summary` are null until processing completes.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloud]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PointCloud | None:
    r"""Get a point cloud by ID

     # Get a Point Cloud

    Returns one point-cloud resource by ID. This endpoint returns resource
    metadata and processing state; it does not return the individual points.
    Use `/data/metadata` and the tile data endpoints for point values after the
    resource reaches `status=\"completed\"`.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    The complete point-cloud resource, including its acquisition `type`,
    `source` provenance, processing `status`, georeference, content summary,
    checksum, and user-editable metadata. Derived fields such as `georeference`
    and `summary` are null until processing completes.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloud
    """

    return sync_detailed(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | PointCloud]:
    r"""Get a point cloud by ID

     # Get a Point Cloud

    Returns one point-cloud resource by ID. This endpoint returns resource
    metadata and processing state; it does not return the individual points.
    Use `/data/metadata` and the tile data endpoints for point values after the
    resource reaches `status=\"completed\"`.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    The complete point-cloud resource, including its acquisition `type`,
    `source` provenance, processing `status`, georeference, content summary,
    checksum, and user-editable metadata. Derived fields such as `georeference`
    and `summary` are null until processing completes.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloud]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PointCloud | None:
    r"""Get a point cloud by ID

     # Get a Point Cloud

    Returns one point-cloud resource by ID. This endpoint returns resource
    metadata and processing state; it does not return the individual points.
    Use `/data/metadata` and the tile data endpoints for point values after the
    resource reaches `status=\"completed\"`.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    The complete point-cloud resource, including its acquisition `type`,
    `source` provenance, processing `status`, georeference, content summary,
    checksum, and user-editable metadata. Derived fields such as `georeference`
    and `summary` are null until processing completes.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloud
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            point_cloud_id=point_cloud_id,
            client=client,
        )
    ).parsed
