from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_chm_inventory_request import CreateChmInventoryRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateChmInventoryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/tree/chm".format(
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
    body: CreateChmInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory from a Canopy Height Model (CHM)

     # Create CHM Extraction Inventory

    Extracts individual tree records from a Canopy Height Model (CHM) grid
    using a specified stem isolation algorithm.

    Currently supports two algorithms:
    1. **Local Maximum Filtering (LMF)**: Sweeps a fixed circular window across the CHM.
    2. **Variable Window Filtering (VWF)**: Sweeps a dynamic window that scales in size based on the
    height of the canopy, allowing for better detection of mixed stand structures.

    ## Request Body

    - **source_chm_grid_id**: (required) ID of a completed CHM grid.
    - **algorithm**: (optional) Configuration for the stem isolation algorithm. Must specify `\"name\":
    \"lmf\"` or `\"name\": \"vwf\"`. Defaults to LMF.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateChmInventoryRequest): Request body for creating an inventory via CHM
            extraction.

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
    body: CreateChmInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory from a Canopy Height Model (CHM)

     # Create CHM Extraction Inventory

    Extracts individual tree records from a Canopy Height Model (CHM) grid
    using a specified stem isolation algorithm.

    Currently supports two algorithms:
    1. **Local Maximum Filtering (LMF)**: Sweeps a fixed circular window across the CHM.
    2. **Variable Window Filtering (VWF)**: Sweeps a dynamic window that scales in size based on the
    height of the canopy, allowing for better detection of mixed stand structures.

    ## Request Body

    - **source_chm_grid_id**: (required) ID of a completed CHM grid.
    - **algorithm**: (optional) Configuration for the stem isolation algorithm. Must specify `\"name\":
    \"lmf\"` or `\"name\": \"vwf\"`. Defaults to LMF.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateChmInventoryRequest): Request body for creating an inventory via CHM
            extraction.

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
    body: CreateChmInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory from a Canopy Height Model (CHM)

     # Create CHM Extraction Inventory

    Extracts individual tree records from a Canopy Height Model (CHM) grid
    using a specified stem isolation algorithm.

    Currently supports two algorithms:
    1. **Local Maximum Filtering (LMF)**: Sweeps a fixed circular window across the CHM.
    2. **Variable Window Filtering (VWF)**: Sweeps a dynamic window that scales in size based on the
    height of the canopy, allowing for better detection of mixed stand structures.

    ## Request Body

    - **source_chm_grid_id**: (required) ID of a completed CHM grid.
    - **algorithm**: (optional) Configuration for the stem isolation algorithm. Must specify `\"name\":
    \"lmf\"` or `\"name\": \"vwf\"`. Defaults to LMF.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateChmInventoryRequest): Request body for creating an inventory via CHM
            extraction.

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
    body: CreateChmInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory from a Canopy Height Model (CHM)

     # Create CHM Extraction Inventory

    Extracts individual tree records from a Canopy Height Model (CHM) grid
    using a specified stem isolation algorithm.

    Currently supports two algorithms:
    1. **Local Maximum Filtering (LMF)**: Sweeps a fixed circular window across the CHM.
    2. **Variable Window Filtering (VWF)**: Sweeps a dynamic window that scales in size based on the
    height of the canopy, allowing for better detection of mixed stand structures.

    ## Request Body

    - **source_chm_grid_id**: (required) ID of a completed CHM grid.
    - **algorithm**: (optional) Configuration for the stem isolation algorithm. Must specify `\"name\":
    \"lmf\"` or `\"name\": \"vwf\"`. Defaults to LMF.
    - **type**: (optional) Entity type. Default: ``\"tree\"``.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) will process the extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateChmInventoryRequest): Request body for creating an inventory via CHM
            extraction.

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
