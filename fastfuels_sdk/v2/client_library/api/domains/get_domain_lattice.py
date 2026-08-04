from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.domain_lattice import DomainLattice
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    *,
    resolution: float,
    num_buffer_cells: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["resolution"] = resolution

    params["num_buffer_cells"] = num_buffer_cells

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/lattice".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DomainLattice | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DomainLattice.from_dict(response.json())

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
) -> Response[DomainLattice | HTTPValidationError]:
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
    resolution: float,
    num_buffer_cells: int | Unset = 0,
) -> Response[DomainLattice | HTTPValidationError]:
    """Get the pixel lattice for a domain at a given resolution

     # Get Domain Lattice Endpoint

    Returns the pixel lattice (transform + shape) for the domain at the
    requested resolution. Use this to align a GeoTIFF before uploading it
    via `POST /domains/{domain_id}/grids/upload`.

    ## Query Parameters

    - **resolution** (required): Pixel size in meters.
    - **num_buffer_cells** (optional, default 0): Expand the lattice by
      `N * resolution` meters on each side.

    ## Response

    - **crs**: The domain CRS (always projected).
    - **resolution**: Echoes the input.
    - **num_buffer_cells**: Echoes the input.
    - **transform**: Affine coefficients `[a, b, c, d, e, f]` (rasterio
      convention).
    - **shape**: `[height, width]` in pixels.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not
      have access.
    - **422 Unprocessable Entity**: `resolution` is missing or
      non-positive, or `num_buffer_cells` is negative.

    Args:
        domain_id (str):
        resolution (float): Pixel size in meters (domain CRS units, always projected).
        num_buffer_cells (int | Unset): Expand the lattice by N cells on each side. Mirrors the
            buffer semantics of POST /domains/{domain_id}/grids/upload and the LANDFIRE/3DEP grid
            creation endpoints. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DomainLattice | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        resolution=resolution,
        num_buffer_cells=num_buffer_cells,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    resolution: float,
    num_buffer_cells: int | Unset = 0,
) -> DomainLattice | HTTPValidationError | None:
    """Get the pixel lattice for a domain at a given resolution

     # Get Domain Lattice Endpoint

    Returns the pixel lattice (transform + shape) for the domain at the
    requested resolution. Use this to align a GeoTIFF before uploading it
    via `POST /domains/{domain_id}/grids/upload`.

    ## Query Parameters

    - **resolution** (required): Pixel size in meters.
    - **num_buffer_cells** (optional, default 0): Expand the lattice by
      `N * resolution` meters on each side.

    ## Response

    - **crs**: The domain CRS (always projected).
    - **resolution**: Echoes the input.
    - **num_buffer_cells**: Echoes the input.
    - **transform**: Affine coefficients `[a, b, c, d, e, f]` (rasterio
      convention).
    - **shape**: `[height, width]` in pixels.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not
      have access.
    - **422 Unprocessable Entity**: `resolution` is missing or
      non-positive, or `num_buffer_cells` is negative.

    Args:
        domain_id (str):
        resolution (float): Pixel size in meters (domain CRS units, always projected).
        num_buffer_cells (int | Unset): Expand the lattice by N cells on each side. Mirrors the
            buffer semantics of POST /domains/{domain_id}/grids/upload and the LANDFIRE/3DEP grid
            creation endpoints. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DomainLattice | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        resolution=resolution,
        num_buffer_cells=num_buffer_cells,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    resolution: float,
    num_buffer_cells: int | Unset = 0,
) -> Response[DomainLattice | HTTPValidationError]:
    """Get the pixel lattice for a domain at a given resolution

     # Get Domain Lattice Endpoint

    Returns the pixel lattice (transform + shape) for the domain at the
    requested resolution. Use this to align a GeoTIFF before uploading it
    via `POST /domains/{domain_id}/grids/upload`.

    ## Query Parameters

    - **resolution** (required): Pixel size in meters.
    - **num_buffer_cells** (optional, default 0): Expand the lattice by
      `N * resolution` meters on each side.

    ## Response

    - **crs**: The domain CRS (always projected).
    - **resolution**: Echoes the input.
    - **num_buffer_cells**: Echoes the input.
    - **transform**: Affine coefficients `[a, b, c, d, e, f]` (rasterio
      convention).
    - **shape**: `[height, width]` in pixels.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not
      have access.
    - **422 Unprocessable Entity**: `resolution` is missing or
      non-positive, or `num_buffer_cells` is negative.

    Args:
        domain_id (str):
        resolution (float): Pixel size in meters (domain CRS units, always projected).
        num_buffer_cells (int | Unset): Expand the lattice by N cells on each side. Mirrors the
            buffer semantics of POST /domains/{domain_id}/grids/upload and the LANDFIRE/3DEP grid
            creation endpoints. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DomainLattice | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        resolution=resolution,
        num_buffer_cells=num_buffer_cells,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    resolution: float,
    num_buffer_cells: int | Unset = 0,
) -> DomainLattice | HTTPValidationError | None:
    """Get the pixel lattice for a domain at a given resolution

     # Get Domain Lattice Endpoint

    Returns the pixel lattice (transform + shape) for the domain at the
    requested resolution. Use this to align a GeoTIFF before uploading it
    via `POST /domains/{domain_id}/grids/upload`.

    ## Query Parameters

    - **resolution** (required): Pixel size in meters.
    - **num_buffer_cells** (optional, default 0): Expand the lattice by
      `N * resolution` meters on each side.

    ## Response

    - **crs**: The domain CRS (always projected).
    - **resolution**: Echoes the input.
    - **num_buffer_cells**: Echoes the input.
    - **transform**: Affine coefficients `[a, b, c, d, e, f]` (rasterio
      convention).
    - **shape**: `[height, width]` in pixels.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not
      have access.
    - **422 Unprocessable Entity**: `resolution` is missing or
      non-positive, or `num_buffer_cells` is negative.

    Args:
        domain_id (str):
        resolution (float): Pixel size in meters (domain CRS units, always projected).
        num_buffer_cells (int | Unset): Expand the lattice by N cells on each side. Mirrors the
            buffer semantics of POST /domains/{domain_id}/grids/upload and the LANDFIRE/3DEP grid
            creation endpoints. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DomainLattice | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            resolution=resolution,
            num_buffer_cells=num_buffer_cells,
        )
    ).parsed
