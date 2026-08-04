from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_geo_tiff_upload_request import CreateGeoTIFFUploadRequest
from ...models.grid_upload_created_response import GridUploadCreatedResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateGeoTIFFUploadRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/upload/geotiff".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = GridUploadCreatedResponse.from_dict(response.json())

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
) -> Response[GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail]:
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
    body: CreateGeoTIFFUploadRequest,
) -> Response[GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from a direct GeoTIFF upload

     # Create Upload Grid (GeoTIFF)

    Creates a grid resource and returns a signed URL for uploading a GeoTIFF
    directly to GCS. Upload with HTTP PUT, sending **every header in the
    response's `upload.headers`** exactly as given — the signed URL commits to
    them, and the upload is rejected if any is missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.tif       -H \"Content-Type: image/tiff\"       -H \"x-goog-content-
    length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Band Definitions

    The `bands` array maps 1:1 to GeoTIFF raster bands in order:
    `bands[0]` → GeoTIFF band 1, `bands[1]` → GeoTIFF band 2, etc.
    Each band key becomes a variable name in the output Zarr store.

    ## CRS Handling

    The GeoTIFF must have a CRS set and must match the domain CRS. A mismatch
    fails with `CRS_MISMATCH`; reproject the GeoTIFF (e.g., `gdalwarp -t_srs`)
    before uploading.

    ## Buffer Cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain extent
    in the stored grid. The uploaded GeoTIFF must cover the domain bbox
    expanded by `num_buffer_cells * native_pixel_size` on each side; pixels
    beyond that expanded extent are clipped away.

    ## File requirements

    Single or multi-band GeoTIFF (`.tif`, `.tiff`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateGeoTIFFUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateGeoTIFFUploadRequest,
) -> GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from a direct GeoTIFF upload

     # Create Upload Grid (GeoTIFF)

    Creates a grid resource and returns a signed URL for uploading a GeoTIFF
    directly to GCS. Upload with HTTP PUT, sending **every header in the
    response's `upload.headers`** exactly as given — the signed URL commits to
    them, and the upload is rejected if any is missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.tif       -H \"Content-Type: image/tiff\"       -H \"x-goog-content-
    length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Band Definitions

    The `bands` array maps 1:1 to GeoTIFF raster bands in order:
    `bands[0]` → GeoTIFF band 1, `bands[1]` → GeoTIFF band 2, etc.
    Each band key becomes a variable name in the output Zarr store.

    ## CRS Handling

    The GeoTIFF must have a CRS set and must match the domain CRS. A mismatch
    fails with `CRS_MISMATCH`; reproject the GeoTIFF (e.g., `gdalwarp -t_srs`)
    before uploading.

    ## Buffer Cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain extent
    in the stored grid. The uploaded GeoTIFF must cover the domain bbox
    expanded by `num_buffer_cells * native_pixel_size` on each side; pixels
    beyond that expanded extent are clipped away.

    ## File requirements

    Single or multi-band GeoTIFF (`.tif`, `.tiff`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateGeoTIFFUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail
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
    body: CreateGeoTIFFUploadRequest,
) -> Response[GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from a direct GeoTIFF upload

     # Create Upload Grid (GeoTIFF)

    Creates a grid resource and returns a signed URL for uploading a GeoTIFF
    directly to GCS. Upload with HTTP PUT, sending **every header in the
    response's `upload.headers`** exactly as given — the signed URL commits to
    them, and the upload is rejected if any is missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.tif       -H \"Content-Type: image/tiff\"       -H \"x-goog-content-
    length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Band Definitions

    The `bands` array maps 1:1 to GeoTIFF raster bands in order:
    `bands[0]` → GeoTIFF band 1, `bands[1]` → GeoTIFF band 2, etc.
    Each band key becomes a variable name in the output Zarr store.

    ## CRS Handling

    The GeoTIFF must have a CRS set and must match the domain CRS. A mismatch
    fails with `CRS_MISMATCH`; reproject the GeoTIFF (e.g., `gdalwarp -t_srs`)
    before uploading.

    ## Buffer Cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain extent
    in the stored grid. The uploaded GeoTIFF must cover the domain bbox
    expanded by `num_buffer_cells * native_pixel_size` on each side; pixels
    beyond that expanded extent are clipped away.

    ## File requirements

    Single or multi-band GeoTIFF (`.tif`, `.tiff`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateGeoTIFFUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateGeoTIFFUploadRequest,
) -> GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from a direct GeoTIFF upload

     # Create Upload Grid (GeoTIFF)

    Creates a grid resource and returns a signed URL for uploading a GeoTIFF
    directly to GCS. Upload with HTTP PUT, sending **every header in the
    response's `upload.headers`** exactly as given — the signed URL commits to
    them, and the upload is rejected if any is missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.tif       -H \"Content-Type: image/tiff\"       -H \"x-goog-content-
    length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Band Definitions

    The `bands` array maps 1:1 to GeoTIFF raster bands in order:
    `bands[0]` → GeoTIFF band 1, `bands[1]` → GeoTIFF band 2, etc.
    Each band key becomes a variable name in the output Zarr store.

    ## CRS Handling

    The GeoTIFF must have a CRS set and must match the domain CRS. A mismatch
    fails with `CRS_MISMATCH`; reproject the GeoTIFF (e.g., `gdalwarp -t_srs`)
    before uploading.

    ## Buffer Cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain extent
    in the stored grid. The uploaded GeoTIFF must cover the domain bbox
    expanded by `num_buffer_cells * native_pixel_size` on each side; pixels
    beyond that expanded extent are clipped away.

    ## File requirements

    Single or multi-band GeoTIFF (`.tif`, `.tiff`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateGeoTIFFUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridUploadCreatedResponse | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
