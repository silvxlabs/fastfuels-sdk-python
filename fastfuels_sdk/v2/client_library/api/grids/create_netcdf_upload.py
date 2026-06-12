from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_netcdf_upload_request import CreateNetcdfUploadRequest
from ...models.grid_upload_created_response import GridUploadCreatedResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateNetcdfUploadRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/upload/netcdf".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GridUploadCreatedResponse | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = GridUploadCreatedResponse.from_dict(response.json())

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
) -> Response[GridUploadCreatedResponse | HTTPValidationError]:
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
    body: CreateNetcdfUploadRequest,
) -> Response[GridUploadCreatedResponse | HTTPValidationError]:
    r"""Create a grid from a direct netCDF upload

     # Create Upload Grid (netCDF)

    Creates a grid resource and returns a signed URL for uploading a
    CF-conformant netCDF directly to GCS. Upload with HTTP PUT, sending
    **every header in the response's `upload.headers`** exactly as given —
    the signed URL commits to them, and the upload is rejected if any is
    missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.nc       -H \"Content-Type: application/x-netcdf\"       -H \"x-goog-
    content-length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Bands

    Unlike the GeoTIFF route, the request body has **no `bands` field**.
    netCDF data variable names are the canonical band keys — they are
    extracted directly from the file and become the variable names in the
    output Zarr store. Per-band `units` (if set on the variable) and dtype
    drive the stored band metadata.

    ## Dimensions

    Each data variable must have dims exactly `(\"y\",\"x\")` (2D) or
    `(\"z\",\"y\",\"x\")` (3D) in that order. Mixed-rank datasets are rejected
    with `WRONG_DIMS`.

    ## CRS

    The dataset must carry a CF `grid_mapping` (typically `spatial_ref`)
    that matches the domain CRS. Missing CRS fails with `MISSING_CRS`;
    mismatched CRS fails with `CRS_MISMATCH`. No auto-reproject.

    ## Units

    If a data variable has a `units` attribute it must be in canonical
    UDUNITS-2 ASCII form with `**` exponents (e.g. `kg/m**3`, `1/m`, `%`).
    Non-canonical forms (`kg/m³`, `kg/m^3`, `kg/m3`) fail with
    `INVALID_UNITS`. See docs/units.md.

    ## Z axis (3D only)

    - `z.attrs[\"positive\"]` must equal `\"up\"`. `\"down\"` is rejected
      (`MISSING_Z_POSITIVE`).
    - z-coordinates must be uniformly spaced. Non-uniform spacing is
      rejected with `NONUNIFORM_Z`.

    ## Buffer cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain
    extent in the stored grid. The uploaded netCDF must cover the domain
    bbox expanded by `num_buffer_cells * native_pixel_size` on each side;
    pixels beyond that expanded extent are clipped away.

    ## File requirements

    CF-conformant netCDF (`.nc`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateNetcdfUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridUploadCreatedResponse | HTTPValidationError]
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
    body: CreateNetcdfUploadRequest,
) -> GridUploadCreatedResponse | HTTPValidationError | None:
    r"""Create a grid from a direct netCDF upload

     # Create Upload Grid (netCDF)

    Creates a grid resource and returns a signed URL for uploading a
    CF-conformant netCDF directly to GCS. Upload with HTTP PUT, sending
    **every header in the response's `upload.headers`** exactly as given —
    the signed URL commits to them, and the upload is rejected if any is
    missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.nc       -H \"Content-Type: application/x-netcdf\"       -H \"x-goog-
    content-length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Bands

    Unlike the GeoTIFF route, the request body has **no `bands` field**.
    netCDF data variable names are the canonical band keys — they are
    extracted directly from the file and become the variable names in the
    output Zarr store. Per-band `units` (if set on the variable) and dtype
    drive the stored band metadata.

    ## Dimensions

    Each data variable must have dims exactly `(\"y\",\"x\")` (2D) or
    `(\"z\",\"y\",\"x\")` (3D) in that order. Mixed-rank datasets are rejected
    with `WRONG_DIMS`.

    ## CRS

    The dataset must carry a CF `grid_mapping` (typically `spatial_ref`)
    that matches the domain CRS. Missing CRS fails with `MISSING_CRS`;
    mismatched CRS fails with `CRS_MISMATCH`. No auto-reproject.

    ## Units

    If a data variable has a `units` attribute it must be in canonical
    UDUNITS-2 ASCII form with `**` exponents (e.g. `kg/m**3`, `1/m`, `%`).
    Non-canonical forms (`kg/m³`, `kg/m^3`, `kg/m3`) fail with
    `INVALID_UNITS`. See docs/units.md.

    ## Z axis (3D only)

    - `z.attrs[\"positive\"]` must equal `\"up\"`. `\"down\"` is rejected
      (`MISSING_Z_POSITIVE`).
    - z-coordinates must be uniformly spaced. Non-uniform spacing is
      rejected with `NONUNIFORM_Z`.

    ## Buffer cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain
    extent in the stored grid. The uploaded netCDF must cover the domain
    bbox expanded by `num_buffer_cells * native_pixel_size` on each side;
    pixels beyond that expanded extent are clipped away.

    ## File requirements

    CF-conformant netCDF (`.nc`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateNetcdfUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridUploadCreatedResponse | HTTPValidationError
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
    body: CreateNetcdfUploadRequest,
) -> Response[GridUploadCreatedResponse | HTTPValidationError]:
    r"""Create a grid from a direct netCDF upload

     # Create Upload Grid (netCDF)

    Creates a grid resource and returns a signed URL for uploading a
    CF-conformant netCDF directly to GCS. Upload with HTTP PUT, sending
    **every header in the response's `upload.headers`** exactly as given —
    the signed URL commits to them, and the upload is rejected if any is
    missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.nc       -H \"Content-Type: application/x-netcdf\"       -H \"x-goog-
    content-length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Bands

    Unlike the GeoTIFF route, the request body has **no `bands` field**.
    netCDF data variable names are the canonical band keys — they are
    extracted directly from the file and become the variable names in the
    output Zarr store. Per-band `units` (if set on the variable) and dtype
    drive the stored band metadata.

    ## Dimensions

    Each data variable must have dims exactly `(\"y\",\"x\")` (2D) or
    `(\"z\",\"y\",\"x\")` (3D) in that order. Mixed-rank datasets are rejected
    with `WRONG_DIMS`.

    ## CRS

    The dataset must carry a CF `grid_mapping` (typically `spatial_ref`)
    that matches the domain CRS. Missing CRS fails with `MISSING_CRS`;
    mismatched CRS fails with `CRS_MISMATCH`. No auto-reproject.

    ## Units

    If a data variable has a `units` attribute it must be in canonical
    UDUNITS-2 ASCII form with `**` exponents (e.g. `kg/m**3`, `1/m`, `%`).
    Non-canonical forms (`kg/m³`, `kg/m^3`, `kg/m3`) fail with
    `INVALID_UNITS`. See docs/units.md.

    ## Z axis (3D only)

    - `z.attrs[\"positive\"]` must equal `\"up\"`. `\"down\"` is rejected
      (`MISSING_Z_POSITIVE`).
    - z-coordinates must be uniformly spaced. Non-uniform spacing is
      rejected with `NONUNIFORM_Z`.

    ## Buffer cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain
    extent in the stored grid. The uploaded netCDF must cover the domain
    bbox expanded by `num_buffer_cells * native_pixel_size` on each side;
    pixels beyond that expanded extent are clipped away.

    ## File requirements

    CF-conformant netCDF (`.nc`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateNetcdfUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridUploadCreatedResponse | HTTPValidationError]
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
    body: CreateNetcdfUploadRequest,
) -> GridUploadCreatedResponse | HTTPValidationError | None:
    r"""Create a grid from a direct netCDF upload

     # Create Upload Grid (netCDF)

    Creates a grid resource and returns a signed URL for uploading a
    CF-conformant netCDF directly to GCS. Upload with HTTP PUT, sending
    **every header in the response's `upload.headers`** exactly as given —
    the signed URL commits to them, and the upload is rejected if any is
    missing or altered. For example:

    ```bash
    curl -X PUT --upload-file grid.nc       -H \"Content-Type: application/x-netcdf\"       -H \"x-goog-
    content-length-range: 0,1073741824\"       \"<upload.url>\"
    ```

    When the upload completes, the uploader service processes the file
    automatically via Eventarc and updates the grid status to `completed`
    (or `failed` on error).

    ## Bands

    Unlike the GeoTIFF route, the request body has **no `bands` field**.
    netCDF data variable names are the canonical band keys — they are
    extracted directly from the file and become the variable names in the
    output Zarr store. Per-band `units` (if set on the variable) and dtype
    drive the stored band metadata.

    ## Dimensions

    Each data variable must have dims exactly `(\"y\",\"x\")` (2D) or
    `(\"z\",\"y\",\"x\")` (3D) in that order. Mixed-rank datasets are rejected
    with `WRONG_DIMS`.

    ## CRS

    The dataset must carry a CF `grid_mapping` (typically `spatial_ref`)
    that matches the domain CRS. Missing CRS fails with `MISSING_CRS`;
    mismatched CRS fails with `CRS_MISMATCH`. No auto-reproject.

    ## Units

    If a data variable has a `units` attribute it must be in canonical
    UDUNITS-2 ASCII form with `**` exponents (e.g. `kg/m**3`, `1/m`, `%`).
    Non-canonical forms (`kg/m³`, `kg/m^3`, `kg/m3`) fail with
    `INVALID_UNITS`. See docs/units.md.

    ## Z axis (3D only)

    - `z.attrs[\"positive\"]` must equal `\"up\"`. `\"down\"` is rejected
      (`MISSING_Z_POSITIVE`).
    - z-coordinates must be uniformly spaced. Non-uniform spacing is
      rejected with `NONUNIFORM_Z`.

    ## Buffer cells

    `num_buffer_cells` (default 0) keeps extra cells around the domain
    extent in the stored grid. The uploaded netCDF must cover the domain
    bbox expanded by `num_buffer_cells * native_pixel_size` on each side;
    pixels beyond that expanded extent are clipped away.

    ## File requirements

    CF-conformant netCDF (`.nc`). Maximum 1 GB.

    Args:
        domain_id (str):
        body (CreateNetcdfUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridUploadCreatedResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
