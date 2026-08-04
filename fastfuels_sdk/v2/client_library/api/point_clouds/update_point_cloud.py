from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.point_cloud import PointCloud
from ...models.update_point_cloud_request_body import UpdatePointCloudRequestBody
from ...types import Response


def _get_kwargs(
    domain_id: str,
    point_cloud_id: str,
    *,
    body: UpdatePointCloudRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/domains/{domain_id}/pointclouds/{point_cloud_id}".format(
            domain_id=quote(str(domain_id), safe=""),
            point_cloud_id=quote(str(point_cloud_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: UpdatePointCloudRequestBody,
) -> Response[HTTPValidationError | PointCloud]:
    """Update a point cloud

     # Update Point Cloud

    Updates the metadata of an existing point cloud. Only the fields provided in
    the request body are modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the point cloud belongs to.
    - **point_cloud_id**: (string) The unique identifier of the point cloud.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the point cloud.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following are immutable through this endpoint:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the point cloud's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is updated automatically.

    ## Response

    Returns the updated point cloud resource.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist or the user does not have access.

    Args:
        domain_id (str):
        point_cloud_id (str):
        body (UpdatePointCloudRequestBody): Request body for updating point cloud metadata.

            Only metadata is mutable. The point cloud's content, source, and derived
            fields cannot be changed through this endpoint, so updates never alter the
            `checksum`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloud]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
        body=body,
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
    body: UpdatePointCloudRequestBody,
) -> HTTPValidationError | PointCloud | None:
    """Update a point cloud

     # Update Point Cloud

    Updates the metadata of an existing point cloud. Only the fields provided in
    the request body are modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the point cloud belongs to.
    - **point_cloud_id**: (string) The unique identifier of the point cloud.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the point cloud.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following are immutable through this endpoint:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the point cloud's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is updated automatically.

    ## Response

    Returns the updated point cloud resource.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist or the user does not have access.

    Args:
        domain_id (str):
        point_cloud_id (str):
        body (UpdatePointCloudRequestBody): Request body for updating point cloud metadata.

            Only metadata is mutable. The point cloud's content, source, and derived
            fields cannot be changed through this endpoint, so updates never alter the
            `checksum`.

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
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdatePointCloudRequestBody,
) -> Response[HTTPValidationError | PointCloud]:
    """Update a point cloud

     # Update Point Cloud

    Updates the metadata of an existing point cloud. Only the fields provided in
    the request body are modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the point cloud belongs to.
    - **point_cloud_id**: (string) The unique identifier of the point cloud.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the point cloud.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following are immutable through this endpoint:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the point cloud's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is updated automatically.

    ## Response

    Returns the updated point cloud resource.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist or the user does not have access.

    Args:
        domain_id (str):
        point_cloud_id (str):
        body (UpdatePointCloudRequestBody): Request body for updating point cloud metadata.

            Only metadata is mutable. The point cloud's content, source, and derived
            fields cannot be changed through this endpoint, so updates never alter the
            `checksum`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloud]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdatePointCloudRequestBody,
) -> HTTPValidationError | PointCloud | None:
    """Update a point cloud

     # Update Point Cloud

    Updates the metadata of an existing point cloud. Only the fields provided in
    the request body are modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the point cloud belongs to.
    - **point_cloud_id**: (string) The unique identifier of the point cloud.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the point cloud.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following are immutable through this endpoint:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the point cloud's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is updated automatically.

    ## Response

    Returns the updated point cloud resource.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist or the user does not have access.

    Args:
        domain_id (str):
        point_cloud_id (str):
        body (UpdatePointCloudRequestBody): Request body for updating point cloud metadata.

            Only metadata is mutable. The point cloud's content, source, and derived
            fields cannot be changed through this endpoint, so updates never alter the
            `checksum`.

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
            body=body,
        )
    ).parsed
