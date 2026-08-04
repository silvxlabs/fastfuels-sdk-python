from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.grid_data_chunk_metadata import GridDataChunkMetadata
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    grid_id: str,
    chunk_index: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/grids/{grid_id}/chunks/{chunk_index}".format(
            domain_id=quote(str(domain_id), safe=""),
            grid_id=quote(str(grid_id), safe=""),
            chunk_index=quote(str(chunk_index), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GridDataChunkMetadata | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = GridDataChunkMetadata.from_dict(response.json())

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
) -> Response[GridDataChunkMetadata | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    grid_id: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
) -> Response[GridDataChunkMetadata | HTTPValidationError]:
    """Get chunk metadata

     # Get Chunk Metadata Endpoint

    Retrieves the shape, pixel offset, and affine transform for a single 2D or
    3D chunk of a completed grid. This is a lightweight call — no raster data
    is read.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.
    - **chunk_index**: (integer) Zero-based flat chunk index. 2D grids use
      y,x order. 3D grids use z,y,x order.

    ## Response

    Returns chunk metadata:

    - **index**: The chunk index.
    - **shape**: 2D `(height, width)` or 3D `(z, height, width)`. Edge chunks
      may be smaller than the grid's chunk shape.
    - **offset**: 2D `(row, column)` or 3D `(z, row, column)` pixel offset of
      the chunk within the full grid.
    - **transform**: Six-element affine transform for the chunk's spatial extent.
    - **z_origin**, **z_resolution**: Present only for 3D grids.

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not completed, or the user
      does not have access.
    - **422 Unprocessable Entity**: The chunk index is out of range.

    Args:
        domain_id (str):
        grid_id (str):
        chunk_index (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridDataChunkMetadata | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
        chunk_index=chunk_index,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    grid_id: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
) -> GridDataChunkMetadata | HTTPValidationError | None:
    """Get chunk metadata

     # Get Chunk Metadata Endpoint

    Retrieves the shape, pixel offset, and affine transform for a single 2D or
    3D chunk of a completed grid. This is a lightweight call — no raster data
    is read.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.
    - **chunk_index**: (integer) Zero-based flat chunk index. 2D grids use
      y,x order. 3D grids use z,y,x order.

    ## Response

    Returns chunk metadata:

    - **index**: The chunk index.
    - **shape**: 2D `(height, width)` or 3D `(z, height, width)`. Edge chunks
      may be smaller than the grid's chunk shape.
    - **offset**: 2D `(row, column)` or 3D `(z, row, column)` pixel offset of
      the chunk within the full grid.
    - **transform**: Six-element affine transform for the chunk's spatial extent.
    - **z_origin**, **z_resolution**: Present only for 3D grids.

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not completed, or the user
      does not have access.
    - **422 Unprocessable Entity**: The chunk index is out of range.

    Args:
        domain_id (str):
        grid_id (str):
        chunk_index (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridDataChunkMetadata | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        grid_id=grid_id,
        chunk_index=chunk_index,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    grid_id: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
) -> Response[GridDataChunkMetadata | HTTPValidationError]:
    """Get chunk metadata

     # Get Chunk Metadata Endpoint

    Retrieves the shape, pixel offset, and affine transform for a single 2D or
    3D chunk of a completed grid. This is a lightweight call — no raster data
    is read.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.
    - **chunk_index**: (integer) Zero-based flat chunk index. 2D grids use
      y,x order. 3D grids use z,y,x order.

    ## Response

    Returns chunk metadata:

    - **index**: The chunk index.
    - **shape**: 2D `(height, width)` or 3D `(z, height, width)`. Edge chunks
      may be smaller than the grid's chunk shape.
    - **offset**: 2D `(row, column)` or 3D `(z, row, column)` pixel offset of
      the chunk within the full grid.
    - **transform**: Six-element affine transform for the chunk's spatial extent.
    - **z_origin**, **z_resolution**: Present only for 3D grids.

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not completed, or the user
      does not have access.
    - **422 Unprocessable Entity**: The chunk index is out of range.

    Args:
        domain_id (str):
        grid_id (str):
        chunk_index (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GridDataChunkMetadata | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
        chunk_index=chunk_index,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    grid_id: str,
    chunk_index: int,
    *,
    client: AuthenticatedClient,
) -> GridDataChunkMetadata | HTTPValidationError | None:
    """Get chunk metadata

     # Get Chunk Metadata Endpoint

    Retrieves the shape, pixel offset, and affine transform for a single 2D or
    3D chunk of a completed grid. This is a lightweight call — no raster data
    is read.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.
    - **chunk_index**: (integer) Zero-based flat chunk index. 2D grids use
      y,x order. 3D grids use z,y,x order.

    ## Response

    Returns chunk metadata:

    - **index**: The chunk index.
    - **shape**: 2D `(height, width)` or 3D `(z, height, width)`. Edge chunks
      may be smaller than the grid's chunk shape.
    - **offset**: 2D `(row, column)` or 3D `(z, row, column)` pixel offset of
      the chunk within the full grid.
    - **transform**: Six-element affine transform for the chunk's spatial extent.
    - **z_origin**, **z_resolution**: Present only for 3D grids.

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not completed, or the user
      does not have access.
    - **422 Unprocessable Entity**: The chunk index is out of range.

    Args:
        domain_id (str):
        grid_id (str):
        chunk_index (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GridDataChunkMetadata | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            grid_id=grid_id,
            chunk_index=chunk_index,
            client=client,
        )
    ).parsed
