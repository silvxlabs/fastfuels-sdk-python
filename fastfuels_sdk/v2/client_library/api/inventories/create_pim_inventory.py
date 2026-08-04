from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_pim_inventory_request import CreatePimInventoryRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreatePimInventoryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/tree/pim".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = Inventory.from_dict(response.json())

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
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
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
    body: CreatePimInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory from PIM expansion

     # Create PIM Expansion Inventory

    Expands a Plot Imputation Map (PIM) grid into individual tree records
    with spatial coordinates.

    A PIM grid maps each 30m cell to an FIA plot ID. This endpoint takes
    that mapping and generates a full tree inventory using an inhomogeneous
    Poisson point process:

    1. Tree density (trees per area) is interpolated from plot-level data
       onto a sub-cell grid (15m resolution)
    2. Plot IDs are assigned to each sub-cell via nearest-neighbor
       interpolation (Voronoi tessellation)
    3. For each sub-cell, a Poisson-distributed random count of trees is
       drawn from the local density
    4. Trees are sampled from the assigned plot's tree list, weighted by
       trees-per-area (TPA)
    5. Each tree receives a random coordinate within its sub-cell

    The result is a spatially explicit tree inventory that preserves the
    species composition and size distributions of the FIA plots while
    producing realistic spatial patterns.

    The PIM endpoint is source-agnostic: it works the same regardless of
    whether the source grid is from TreeMap, BIGMAP, or FSE. The grid's
    own ``source`` field carries that lineage.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **seed**: (optional) Random seed for reproducibility. Generated
      randomly if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the expansion asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimInventoryRequest): Request body for creating an inventory via PIM
            expansion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory | QuotaExceededDetail]
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
    body: CreatePimInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory from PIM expansion

     # Create PIM Expansion Inventory

    Expands a Plot Imputation Map (PIM) grid into individual tree records
    with spatial coordinates.

    A PIM grid maps each 30m cell to an FIA plot ID. This endpoint takes
    that mapping and generates a full tree inventory using an inhomogeneous
    Poisson point process:

    1. Tree density (trees per area) is interpolated from plot-level data
       onto a sub-cell grid (15m resolution)
    2. Plot IDs are assigned to each sub-cell via nearest-neighbor
       interpolation (Voronoi tessellation)
    3. For each sub-cell, a Poisson-distributed random count of trees is
       drawn from the local density
    4. Trees are sampled from the assigned plot's tree list, weighted by
       trees-per-area (TPA)
    5. Each tree receives a random coordinate within its sub-cell

    The result is a spatially explicit tree inventory that preserves the
    species composition and size distributions of the FIA plots while
    producing realistic spatial patterns.

    The PIM endpoint is source-agnostic: it works the same regardless of
    whether the source grid is from TreeMap, BIGMAP, or FSE. The grid's
    own ``source`` field carries that lineage.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **seed**: (optional) Random seed for reproducibility. Generated
      randomly if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the expansion asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimInventoryRequest): Request body for creating an inventory via PIM
            expansion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory | QuotaExceededDetail
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
    body: CreatePimInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory from PIM expansion

     # Create PIM Expansion Inventory

    Expands a Plot Imputation Map (PIM) grid into individual tree records
    with spatial coordinates.

    A PIM grid maps each 30m cell to an FIA plot ID. This endpoint takes
    that mapping and generates a full tree inventory using an inhomogeneous
    Poisson point process:

    1. Tree density (trees per area) is interpolated from plot-level data
       onto a sub-cell grid (15m resolution)
    2. Plot IDs are assigned to each sub-cell via nearest-neighbor
       interpolation (Voronoi tessellation)
    3. For each sub-cell, a Poisson-distributed random count of trees is
       drawn from the local density
    4. Trees are sampled from the assigned plot's tree list, weighted by
       trees-per-area (TPA)
    5. Each tree receives a random coordinate within its sub-cell

    The result is a spatially explicit tree inventory that preserves the
    species composition and size distributions of the FIA plots while
    producing realistic spatial patterns.

    The PIM endpoint is source-agnostic: it works the same regardless of
    whether the source grid is from TreeMap, BIGMAP, or FSE. The grid's
    own ``source`` field carries that lineage.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **seed**: (optional) Random seed for reproducibility. Generated
      randomly if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the expansion asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimInventoryRequest): Request body for creating an inventory via PIM
            expansion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory | QuotaExceededDetail]
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
    body: CreatePimInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory from PIM expansion

     # Create PIM Expansion Inventory

    Expands a Plot Imputation Map (PIM) grid into individual tree records
    with spatial coordinates.

    A PIM grid maps each 30m cell to an FIA plot ID. This endpoint takes
    that mapping and generates a full tree inventory using an inhomogeneous
    Poisson point process:

    1. Tree density (trees per area) is interpolated from plot-level data
       onto a sub-cell grid (15m resolution)
    2. Plot IDs are assigned to each sub-cell via nearest-neighbor
       interpolation (Voronoi tessellation)
    3. For each sub-cell, a Poisson-distributed random count of trees is
       drawn from the local density
    4. Trees are sampled from the assigned plot's tree list, weighted by
       trees-per-area (TPA)
    5. Each tree receives a random coordinate within its sub-cell

    The result is a spatially explicit tree inventory that preserves the
    species composition and size distributions of the FIA plots while
    producing realistic spatial patterns.

    The PIM endpoint is source-agnostic: it works the same regardless of
    whether the source grid is from TreeMap, BIGMAP, or FSE. The grid's
    own ``source`` field carries that lineage.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **seed**: (optional) Random seed for reproducibility. Generated
      randomly if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the expansion asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimInventoryRequest): Request body for creating an inventory via PIM
            expansion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
