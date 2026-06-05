from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.grid_data_array_format import GridDataArrayFormat
from ...models.grid_data_order import GridDataOrder
from ...models.grid_data_response import GridDataResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    grid_id: str,
    band: str,
    chunk_index: int,
    *,
    array_format: GridDataArrayFormat | Unset = UNSET,
    order: GridDataOrder | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_array_format: str | Unset = UNSET
    if not isinstance(array_format, Unset):
        json_array_format = array_format.value

    params["array_format"] = json_array_format

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/grids/{grid_id}/data/{band}/{chunk_index}".format(
            domain_id=quote(str(domain_id), safe=""),
            grid_id=quote(str(grid_id), safe=""),
            band=quote(str(band), safe=""),
            chunk_index=quote(str(chunk_index), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GridDataResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = GridDataResponse.from_dict(response.json())

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
) -> Response[GridDataResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    grid_id: str,
    band: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
    array_format: GridDataArrayFormat | Unset = UNSET,
    order: GridDataOrder | Unset = UNSET,
) -> Response[GridDataResponse | HTTPValidationError]:
    r"""Get band data for a chunk (JSON)

     # Get Grid Data (JSON)

    Returns the values of a single band within a single chunk of a completed
    grid as a JSON payload — either dense values or a sparse representation,
    selected via `array_format`.

    For raw bytes (smaller, faster to parse), use the `/binary` variant of
    this endpoint.

    ## Path Parameters

    - **domain_id**: The domain the grid belongs to.
    - **grid_id**: The grid identifier.
    - **band**: Band key to read (must be present in the grid's `bands`).
    - **chunk_index**: Zero-based flat chunk index. 2D grids index in (y, x);
      3D grids index in (z, y, x). The chunk's shape, offset, and affine
      transform are returned alongside the data — no separate metadata call
      is required. (`GET …/chunks/{chunk_index}` is still available for
      clients that want to lay out chunks before fetching data.)

    ## Query Parameters

    - **array_format**: `dense` (default) or `sparse`. Sparse compresses out
      cells equal to the band's fill value, returning only the non-fill
      entries.
    - **order**: Flattening order — `C` (row-major, default) or `F`
      (column-major).

    ## Response

    Both variants share `shape` (chunk dimensions), `order` (flattening
    order used for the values), and `metadata` (the chunk's index, shape,
    offset, and affine transform — and `z_origin`/`z_resolution` for 3D
    grids). The CRS does not vary per chunk; read it from the grid's
    `georeference.crs`.

    **Dense** (`array_format=dense`): `data.format = \"dense\"`, `data.values`
    is a flat list of all cells.

    **Sparse** (`array_format=sparse`): `data.format = \"sparse\"`,
    `data.indices` are flat positions of non-fill cells, `data.values` are
    their values. `data.fill_value` is the band's fill value, or `null` if
    the band does not define one — in which case every cell is listed and no
    compression has been applied.

    ## Errors

    - **404**: Grid not found, not completed, or not accessible.
    - **422**: Band does not exist on this grid, or chunk index out of range.
    - **413**: Response would exceed the size limit. Try `array_format=sparse`,
      the `/binary` variant, or a smaller chunk.

    Args:
        domain_id (str):
        grid_id (str):
        band (str):
        chunk_index (int):
        array_format (GridDataArrayFormat | Unset):
        order (GridDataOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridDataResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
        band=band,
        chunk_index=chunk_index,
        array_format=array_format,
        order=order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    grid_id: str,
    band: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
    array_format: GridDataArrayFormat | Unset = UNSET,
    order: GridDataOrder | Unset = UNSET,
) -> GridDataResponse | HTTPValidationError | None:
    r"""Get band data for a chunk (JSON)

     # Get Grid Data (JSON)

    Returns the values of a single band within a single chunk of a completed
    grid as a JSON payload — either dense values or a sparse representation,
    selected via `array_format`.

    For raw bytes (smaller, faster to parse), use the `/binary` variant of
    this endpoint.

    ## Path Parameters

    - **domain_id**: The domain the grid belongs to.
    - **grid_id**: The grid identifier.
    - **band**: Band key to read (must be present in the grid's `bands`).
    - **chunk_index**: Zero-based flat chunk index. 2D grids index in (y, x);
      3D grids index in (z, y, x). The chunk's shape, offset, and affine
      transform are returned alongside the data — no separate metadata call
      is required. (`GET …/chunks/{chunk_index}` is still available for
      clients that want to lay out chunks before fetching data.)

    ## Query Parameters

    - **array_format**: `dense` (default) or `sparse`. Sparse compresses out
      cells equal to the band's fill value, returning only the non-fill
      entries.
    - **order**: Flattening order — `C` (row-major, default) or `F`
      (column-major).

    ## Response

    Both variants share `shape` (chunk dimensions), `order` (flattening
    order used for the values), and `metadata` (the chunk's index, shape,
    offset, and affine transform — and `z_origin`/`z_resolution` for 3D
    grids). The CRS does not vary per chunk; read it from the grid's
    `georeference.crs`.

    **Dense** (`array_format=dense`): `data.format = \"dense\"`, `data.values`
    is a flat list of all cells.

    **Sparse** (`array_format=sparse`): `data.format = \"sparse\"`,
    `data.indices` are flat positions of non-fill cells, `data.values` are
    their values. `data.fill_value` is the band's fill value, or `null` if
    the band does not define one — in which case every cell is listed and no
    compression has been applied.

    ## Errors

    - **404**: Grid not found, not completed, or not accessible.
    - **422**: Band does not exist on this grid, or chunk index out of range.
    - **413**: Response would exceed the size limit. Try `array_format=sparse`,
      the `/binary` variant, or a smaller chunk.

    Args:
        domain_id (str):
        grid_id (str):
        band (str):
        chunk_index (int):
        array_format (GridDataArrayFormat | Unset):
        order (GridDataOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridDataResponse | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        grid_id=grid_id,
        band=band,
        chunk_index=chunk_index,
        client=client,
        array_format=array_format,
        order=order,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    grid_id: str,
    band: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
    array_format: GridDataArrayFormat | Unset = UNSET,
    order: GridDataOrder | Unset = UNSET,
) -> Response[GridDataResponse | HTTPValidationError]:
    r"""Get band data for a chunk (JSON)

     # Get Grid Data (JSON)

    Returns the values of a single band within a single chunk of a completed
    grid as a JSON payload — either dense values or a sparse representation,
    selected via `array_format`.

    For raw bytes (smaller, faster to parse), use the `/binary` variant of
    this endpoint.

    ## Path Parameters

    - **domain_id**: The domain the grid belongs to.
    - **grid_id**: The grid identifier.
    - **band**: Band key to read (must be present in the grid's `bands`).
    - **chunk_index**: Zero-based flat chunk index. 2D grids index in (y, x);
      3D grids index in (z, y, x). The chunk's shape, offset, and affine
      transform are returned alongside the data — no separate metadata call
      is required. (`GET …/chunks/{chunk_index}` is still available for
      clients that want to lay out chunks before fetching data.)

    ## Query Parameters

    - **array_format**: `dense` (default) or `sparse`. Sparse compresses out
      cells equal to the band's fill value, returning only the non-fill
      entries.
    - **order**: Flattening order — `C` (row-major, default) or `F`
      (column-major).

    ## Response

    Both variants share `shape` (chunk dimensions), `order` (flattening
    order used for the values), and `metadata` (the chunk's index, shape,
    offset, and affine transform — and `z_origin`/`z_resolution` for 3D
    grids). The CRS does not vary per chunk; read it from the grid's
    `georeference.crs`.

    **Dense** (`array_format=dense`): `data.format = \"dense\"`, `data.values`
    is a flat list of all cells.

    **Sparse** (`array_format=sparse`): `data.format = \"sparse\"`,
    `data.indices` are flat positions of non-fill cells, `data.values` are
    their values. `data.fill_value` is the band's fill value, or `null` if
    the band does not define one — in which case every cell is listed and no
    compression has been applied.

    ## Errors

    - **404**: Grid not found, not completed, or not accessible.
    - **422**: Band does not exist on this grid, or chunk index out of range.
    - **413**: Response would exceed the size limit. Try `array_format=sparse`,
      the `/binary` variant, or a smaller chunk.

    Args:
        domain_id (str):
        grid_id (str):
        band (str):
        chunk_index (int):
        array_format (GridDataArrayFormat | Unset):
        order (GridDataOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridDataResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
        band=band,
        chunk_index=chunk_index,
        array_format=array_format,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    grid_id: str,
    band: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
    array_format: GridDataArrayFormat | Unset = UNSET,
    order: GridDataOrder | Unset = UNSET,
) -> GridDataResponse | HTTPValidationError | None:
    r"""Get band data for a chunk (JSON)

     # Get Grid Data (JSON)

    Returns the values of a single band within a single chunk of a completed
    grid as a JSON payload — either dense values or a sparse representation,
    selected via `array_format`.

    For raw bytes (smaller, faster to parse), use the `/binary` variant of
    this endpoint.

    ## Path Parameters

    - **domain_id**: The domain the grid belongs to.
    - **grid_id**: The grid identifier.
    - **band**: Band key to read (must be present in the grid's `bands`).
    - **chunk_index**: Zero-based flat chunk index. 2D grids index in (y, x);
      3D grids index in (z, y, x). The chunk's shape, offset, and affine
      transform are returned alongside the data — no separate metadata call
      is required. (`GET …/chunks/{chunk_index}` is still available for
      clients that want to lay out chunks before fetching data.)

    ## Query Parameters

    - **array_format**: `dense` (default) or `sparse`. Sparse compresses out
      cells equal to the band's fill value, returning only the non-fill
      entries.
    - **order**: Flattening order — `C` (row-major, default) or `F`
      (column-major).

    ## Response

    Both variants share `shape` (chunk dimensions), `order` (flattening
    order used for the values), and `metadata` (the chunk's index, shape,
    offset, and affine transform — and `z_origin`/`z_resolution` for 3D
    grids). The CRS does not vary per chunk; read it from the grid's
    `georeference.crs`.

    **Dense** (`array_format=dense`): `data.format = \"dense\"`, `data.values`
    is a flat list of all cells.

    **Sparse** (`array_format=sparse`): `data.format = \"sparse\"`,
    `data.indices` are flat positions of non-fill cells, `data.values` are
    their values. `data.fill_value` is the band's fill value, or `null` if
    the band does not define one — in which case every cell is listed and no
    compression has been applied.

    ## Errors

    - **404**: Grid not found, not completed, or not accessible.
    - **422**: Band does not exist on this grid, or chunk index out of range.
    - **413**: Response would exceed the size limit. Try `array_format=sparse`,
      the `/binary` variant, or a smaller chunk.

    Args:
        domain_id (str):
        grid_id (str):
        band (str):
        chunk_index (int):
        array_format (GridDataArrayFormat | Unset):
        order (GridDataOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridDataResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            grid_id=grid_id,
            band=band,
            chunk_index=chunk_index,
            client=client,
            array_format=array_format,
            order=order,
        )
    ).parsed
