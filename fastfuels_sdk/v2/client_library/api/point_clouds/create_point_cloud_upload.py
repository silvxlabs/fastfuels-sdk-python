from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_point_cloud_upload_request import CreatePointCloudUploadRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.point_cloud_upload_created_response import (
    PointCloudUploadCreatedResponse,
)
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreatePointCloudUploadRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/pointclouds/upload".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = PointCloudUploadCreatedResponse.from_dict(response.json())

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
) -> Response[
    HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail
]:
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
    body: CreatePointCloudUploadRequest,
) -> Response[
    HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail
]:
    r"""Create a point cloud from a direct file upload

     # Upload a Point Cloud

    Creates a point cloud resource and returns a signed URL for uploading the
    source file directly to storage. Upload is a two-step flow:

    1. **POST** this request to create the point cloud and receive an `upload`
       spec containing a signed URL.
    2. **PUT** your file to `upload.url`, sending **every header in
       `upload.headers`** exactly as given — the signed URL commits to them,
       and the upload is rejected if any is missing or altered. The file must
       not exceed `upload.max_size_bytes`, and the upload must complete before
       `upload.expires_at`. For example:

       ```bash
       curl -X PUT --upload-file cloud.laz          -H \"Content-Type: application/octet-stream\"
    -H \"x-goog-content-length-range: 0,1073741824\"          \"<upload.url>\"
       ```

    The point cloud is returned immediately with `status` = `pending`. Once the
    file finishes uploading it is ingested in the background: `status` becomes
    `running`, then `completed` after the cloud is validated and its
    `georeference` and `summary` are filled in — or `failed` if the file cannot
    be read as a point cloud with a coordinate reference system. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    ## Supported formats

    Upload an uncompressed **LAS** or compressed **LAZ** file (including Cloud
    Optimized Point Clouds, which are valid LAZ). The format is detected from
    the file itself — there is nothing to declare.

    ## Coordinate reference system

    The file must carry a coordinate reference system; uploads without one are
    rejected during ingestion. A cloud in a different CRS than its domain is
    automatically reprojected to the domain CRS (horizontal coordinates only —
    elevations are preserved as-is), so the stored cloud is always in the
    domain CRS.

    Args:
        domain_id (str):
        body (CreatePointCloudUploadRequest): Request body for creating a point cloud from a
            direct file upload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail]
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
    body: CreatePointCloudUploadRequest,
) -> HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail | None:
    r"""Create a point cloud from a direct file upload

     # Upload a Point Cloud

    Creates a point cloud resource and returns a signed URL for uploading the
    source file directly to storage. Upload is a two-step flow:

    1. **POST** this request to create the point cloud and receive an `upload`
       spec containing a signed URL.
    2. **PUT** your file to `upload.url`, sending **every header in
       `upload.headers`** exactly as given — the signed URL commits to them,
       and the upload is rejected if any is missing or altered. The file must
       not exceed `upload.max_size_bytes`, and the upload must complete before
       `upload.expires_at`. For example:

       ```bash
       curl -X PUT --upload-file cloud.laz          -H \"Content-Type: application/octet-stream\"
    -H \"x-goog-content-length-range: 0,1073741824\"          \"<upload.url>\"
       ```

    The point cloud is returned immediately with `status` = `pending`. Once the
    file finishes uploading it is ingested in the background: `status` becomes
    `running`, then `completed` after the cloud is validated and its
    `georeference` and `summary` are filled in — or `failed` if the file cannot
    be read as a point cloud with a coordinate reference system. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    ## Supported formats

    Upload an uncompressed **LAS** or compressed **LAZ** file (including Cloud
    Optimized Point Clouds, which are valid LAZ). The format is detected from
    the file itself — there is nothing to declare.

    ## Coordinate reference system

    The file must carry a coordinate reference system; uploads without one are
    rejected during ingestion. A cloud in a different CRS than its domain is
    automatically reprojected to the domain CRS (horizontal coordinates only —
    elevations are preserved as-is), so the stored cloud is always in the
    domain CRS.

    Args:
        domain_id (str):
        body (CreatePointCloudUploadRequest): Request body for creating a point cloud from a
            direct file upload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail
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
    body: CreatePointCloudUploadRequest,
) -> Response[
    HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail
]:
    r"""Create a point cloud from a direct file upload

     # Upload a Point Cloud

    Creates a point cloud resource and returns a signed URL for uploading the
    source file directly to storage. Upload is a two-step flow:

    1. **POST** this request to create the point cloud and receive an `upload`
       spec containing a signed URL.
    2. **PUT** your file to `upload.url`, sending **every header in
       `upload.headers`** exactly as given — the signed URL commits to them,
       and the upload is rejected if any is missing or altered. The file must
       not exceed `upload.max_size_bytes`, and the upload must complete before
       `upload.expires_at`. For example:

       ```bash
       curl -X PUT --upload-file cloud.laz          -H \"Content-Type: application/octet-stream\"
    -H \"x-goog-content-length-range: 0,1073741824\"          \"<upload.url>\"
       ```

    The point cloud is returned immediately with `status` = `pending`. Once the
    file finishes uploading it is ingested in the background: `status` becomes
    `running`, then `completed` after the cloud is validated and its
    `georeference` and `summary` are filled in — or `failed` if the file cannot
    be read as a point cloud with a coordinate reference system. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    ## Supported formats

    Upload an uncompressed **LAS** or compressed **LAZ** file (including Cloud
    Optimized Point Clouds, which are valid LAZ). The format is detected from
    the file itself — there is nothing to declare.

    ## Coordinate reference system

    The file must carry a coordinate reference system; uploads without one are
    rejected during ingestion. A cloud in a different CRS than its domain is
    automatically reprojected to the domain CRS (horizontal coordinates only —
    elevations are preserved as-is), so the stored cloud is always in the
    domain CRS.

    Args:
        domain_id (str):
        body (CreatePointCloudUploadRequest): Request body for creating a point cloud from a
            direct file upload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail]
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
    body: CreatePointCloudUploadRequest,
) -> HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail | None:
    r"""Create a point cloud from a direct file upload

     # Upload a Point Cloud

    Creates a point cloud resource and returns a signed URL for uploading the
    source file directly to storage. Upload is a two-step flow:

    1. **POST** this request to create the point cloud and receive an `upload`
       spec containing a signed URL.
    2. **PUT** your file to `upload.url`, sending **every header in
       `upload.headers`** exactly as given — the signed URL commits to them,
       and the upload is rejected if any is missing or altered. The file must
       not exceed `upload.max_size_bytes`, and the upload must complete before
       `upload.expires_at`. For example:

       ```bash
       curl -X PUT --upload-file cloud.laz          -H \"Content-Type: application/octet-stream\"
    -H \"x-goog-content-length-range: 0,1073741824\"          \"<upload.url>\"
       ```

    The point cloud is returned immediately with `status` = `pending`. Once the
    file finishes uploading it is ingested in the background: `status` becomes
    `running`, then `completed` after the cloud is validated and its
    `georeference` and `summary` are filled in — or `failed` if the file cannot
    be read as a point cloud with a coordinate reference system. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    ## Supported formats

    Upload an uncompressed **LAS** or compressed **LAZ** file (including Cloud
    Optimized Point Clouds, which are valid LAZ). The format is detected from
    the file itself — there is nothing to declare.

    ## Coordinate reference system

    The file must carry a coordinate reference system; uploads without one are
    rejected during ingestion. A cloud in a different CRS than its domain is
    automatically reprojected to the domain CRS (horizontal coordinates only —
    elevations are preserved as-is), so the stored cloud is always in the
    domain CRS.

    Args:
        domain_id (str):
        body (CreatePointCloudUploadRequest): Request body for creating a point cloud from a
            direct file upload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudUploadCreatedResponse | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
