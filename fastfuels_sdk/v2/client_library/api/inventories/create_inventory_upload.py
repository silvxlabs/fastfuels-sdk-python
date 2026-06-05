from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_inventory_upload_request import CreateInventoryUploadRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory_upload_created_response import InventoryUploadCreatedResponse
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateInventoryUploadRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/tree/upload".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | InventoryUploadCreatedResponse | None:
    if response.status_code == 201:
        response_201 = InventoryUploadCreatedResponse.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | InventoryUploadCreatedResponse]:
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
    body: CreateInventoryUploadRequest,
) -> Response[HTTPValidationError | InventoryUploadCreatedResponse]:
    """Create an inventory from a direct file upload

     # Create Upload Inventory

    Creates an inventory resource and returns a signed URL for uploading the
    source file directly to GCS. The upload must use HTTP PUT with the
    Content-Type header matching the value in the response.

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the inventory status to
    `completed` (or `failed` on error).

    ## Supported Formats

    - **csv**: Comma-separated values. Coordinates must already be in the
      domain's CRS.
    - **geojson**: GeoJSON FeatureCollection with Point or MultiPoint
      geometries. Reprojected to domain CRS automatically.
    - **geopackage**: OGC GeoPackage. Reprojected to domain CRS automatically.

    ## Column Mapping

    Use the `columns` field to map v2 column names to the column names in
    your file. Omit entries where the file already uses v2 names. Required
    in the file: `x`, `y`, `height`.

    Args:
        domain_id (str):
        body (CreateInventoryUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InventoryUploadCreatedResponse]
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
    body: CreateInventoryUploadRequest,
) -> HTTPValidationError | InventoryUploadCreatedResponse | None:
    """Create an inventory from a direct file upload

     # Create Upload Inventory

    Creates an inventory resource and returns a signed URL for uploading the
    source file directly to GCS. The upload must use HTTP PUT with the
    Content-Type header matching the value in the response.

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the inventory status to
    `completed` (or `failed` on error).

    ## Supported Formats

    - **csv**: Comma-separated values. Coordinates must already be in the
      domain's CRS.
    - **geojson**: GeoJSON FeatureCollection with Point or MultiPoint
      geometries. Reprojected to domain CRS automatically.
    - **geopackage**: OGC GeoPackage. Reprojected to domain CRS automatically.

    ## Column Mapping

    Use the `columns` field to map v2 column names to the column names in
    your file. Omit entries where the file already uses v2 names. Required
    in the file: `x`, `y`, `height`.

    Args:
        domain_id (str):
        body (CreateInventoryUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InventoryUploadCreatedResponse
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
    body: CreateInventoryUploadRequest,
) -> Response[HTTPValidationError | InventoryUploadCreatedResponse]:
    """Create an inventory from a direct file upload

     # Create Upload Inventory

    Creates an inventory resource and returns a signed URL for uploading the
    source file directly to GCS. The upload must use HTTP PUT with the
    Content-Type header matching the value in the response.

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the inventory status to
    `completed` (or `failed` on error).

    ## Supported Formats

    - **csv**: Comma-separated values. Coordinates must already be in the
      domain's CRS.
    - **geojson**: GeoJSON FeatureCollection with Point or MultiPoint
      geometries. Reprojected to domain CRS automatically.
    - **geopackage**: OGC GeoPackage. Reprojected to domain CRS automatically.

    ## Column Mapping

    Use the `columns` field to map v2 column names to the column names in
    your file. Omit entries where the file already uses v2 names. Required
    in the file: `x`, `y`, `height`.

    Args:
        domain_id (str):
        body (CreateInventoryUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InventoryUploadCreatedResponse]
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
    body: CreateInventoryUploadRequest,
) -> HTTPValidationError | InventoryUploadCreatedResponse | None:
    """Create an inventory from a direct file upload

     # Create Upload Inventory

    Creates an inventory resource and returns a signed URL for uploading the
    source file directly to GCS. The upload must use HTTP PUT with the
    Content-Type header matching the value in the response.

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the inventory status to
    `completed` (or `failed` on error).

    ## Supported Formats

    - **csv**: Comma-separated values. Coordinates must already be in the
      domain's CRS.
    - **geojson**: GeoJSON FeatureCollection with Point or MultiPoint
      geometries. Reprojected to domain CRS automatically.
    - **geopackage**: OGC GeoPackage. Reprojected to domain CRS automatically.

    ## Column Mapping

    Use the `columns` field to map v2 column names to the column names in
    your file. Omit entries where the file already uses v2 names. Required
    in the file: `x`, `y`, `height`.

    Args:
        domain_id (str):
        body (CreateInventoryUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InventoryUploadCreatedResponse
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
