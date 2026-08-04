from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory_data_metadata import InventoryDataMetadata
from ...types import Response


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/inventories/{inventory_id}/data/metadata".format(
            domain_id=quote(str(domain_id), safe=""),
            inventory_id=quote(str(inventory_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | InventoryDataMetadata | None:
    if response.status_code == 200:
        response_200 = InventoryDataMetadata.from_dict(response.json())

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
) -> Response[HTTPValidationError | InventoryDataMetadata]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | InventoryDataMetadata]:
    """Get inventory data metadata

     # Get Inventory Data Metadata

    Returns partition count, total rows, per-partition row counts, and column
    names for a completed inventory. Reads only the `_metadata` file from GCS
    (cached after first access).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.

    ## Response

    - **inventory_id**: The inventory ID.
    - **num_partitions**: Number of Parquet partitions.
    - **total_rows**: Total row count across all partitions.
    - **columns**: List of column names.
    - **partitions**: Per-partition index and row count.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory is not completed, or metadata
      file is not available.

    Args:
        domain_id (str):
        inventory_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InventoryDataMetadata]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | InventoryDataMetadata | None:
    """Get inventory data metadata

     # Get Inventory Data Metadata

    Returns partition count, total rows, per-partition row counts, and column
    names for a completed inventory. Reads only the `_metadata` file from GCS
    (cached after first access).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.

    ## Response

    - **inventory_id**: The inventory ID.
    - **num_partitions**: Number of Parquet partitions.
    - **total_rows**: Total row count across all partitions.
    - **columns**: List of column names.
    - **partitions**: Per-partition index and row count.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory is not completed, or metadata
      file is not available.

    Args:
        domain_id (str):
        inventory_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InventoryDataMetadata
    """

    return sync_detailed(
        domain_id=domain_id,
        inventory_id=inventory_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | InventoryDataMetadata]:
    """Get inventory data metadata

     # Get Inventory Data Metadata

    Returns partition count, total rows, per-partition row counts, and column
    names for a completed inventory. Reads only the `_metadata` file from GCS
    (cached after first access).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.

    ## Response

    - **inventory_id**: The inventory ID.
    - **num_partitions**: Number of Parquet partitions.
    - **total_rows**: Total row count across all partitions.
    - **columns**: List of column names.
    - **partitions**: Per-partition index and row count.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory is not completed, or metadata
      file is not available.

    Args:
        domain_id (str):
        inventory_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InventoryDataMetadata]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | InventoryDataMetadata | None:
    """Get inventory data metadata

     # Get Inventory Data Metadata

    Returns partition count, total rows, per-partition row counts, and column
    names for a completed inventory. Reads only the `_metadata` file from GCS
    (cached after first access).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.

    ## Response

    - **inventory_id**: The inventory ID.
    - **num_partitions**: Number of Parquet partitions.
    - **total_rows**: Total row count across all partitions.
    - **columns**: List of column names.
    - **partitions**: Per-partition index and row count.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory is not completed, or metadata
      file is not available.

    Args:
        domain_id (str):
        inventory_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InventoryDataMetadata
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            inventory_id=inventory_id,
            client=client,
        )
    ).parsed
