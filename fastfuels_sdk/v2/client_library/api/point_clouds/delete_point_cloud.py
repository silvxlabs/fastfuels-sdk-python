from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    point_cloud_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/domains/{domain_id}/pointclouds/{point_cloud_id}".format(
            domain_id=quote(str(domain_id), safe=""),
            point_cloud_id=quote(str(point_cloud_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
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
) -> Response[Any | HTTPValidationError]:
    """Delete a point cloud

     # Delete a Point Cloud

    Deletes a point-cloud resource. This action cannot be undone through the
    API. Its GCS artifact becomes orphaned and is reclaimed asynchronously by
    the storage cleanup service; callers should treat the point cloud as deleted
    as soon as this endpoint returns.

    Deleting a point cloud does not delete grids or inventories that were
    derived from it. Those resources retain their recorded provenance, although
    the source point cloud can no longer be queried.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    HTTP `204 No Content` with an empty response body.

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
        Response[Any | HTTPValidationError]
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
) -> Any | HTTPValidationError | None:
    """Delete a point cloud

     # Delete a Point Cloud

    Deletes a point-cloud resource. This action cannot be undone through the
    API. Its GCS artifact becomes orphaned and is reclaimed asynchronously by
    the storage cleanup service; callers should treat the point cloud as deleted
    as soon as this endpoint returns.

    Deleting a point cloud does not delete grids or inventories that were
    derived from it. Those resources retain their recorded provenance, although
    the source point cloud can no longer be queried.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    HTTP `204 No Content` with an empty response body.

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
        Any | HTTPValidationError
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
) -> Response[Any | HTTPValidationError]:
    """Delete a point cloud

     # Delete a Point Cloud

    Deletes a point-cloud resource. This action cannot be undone through the
    API. Its GCS artifact becomes orphaned and is reclaimed asynchronously by
    the storage cleanup service; callers should treat the point cloud as deleted
    as soon as this endpoint returns.

    Deleting a point cloud does not delete grids or inventories that were
    derived from it. Those resources retain their recorded provenance, although
    the source point cloud can no longer be queried.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    HTTP `204 No Content` with an empty response body.

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
        Response[Any | HTTPValidationError]
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
) -> Any | HTTPValidationError | None:
    """Delete a point cloud

     # Delete a Point Cloud

    Deletes a point-cloud resource. This action cannot be undone through the
    API. Its GCS artifact becomes orphaned and is reclaimed asynchronously by
    the storage cleanup service; callers should treat the point cloud as deleted
    as soon as this endpoint returns.

    Deleting a point cloud does not delete grids or inventories that were
    derived from it. Those resources retain their recorded provenance, although
    the source point cloud can no longer be queried.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    HTTP `204 No Content` with an empty response body.

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
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            point_cloud_id=point_cloud_id,
            client=client,
        )
    ).parsed
