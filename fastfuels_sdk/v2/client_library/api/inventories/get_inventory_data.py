from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory_data_format import InventoryDataFormat
from ...models.inventory_data_response import InventoryDataResponse
from ...models.inventory_json_orientation import InventoryJsonOrientation
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
    partition_index: int,
    *,
    format_: InventoryDataFormat | Unset = UNSET,
    json_orientation: InventoryJsonOrientation | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_format_: str | Unset = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    json_json_orientation: str | Unset = UNSET
    if not isinstance(json_orientation, Unset):
        json_json_orientation = json_orientation.value

    params["json_orientation"] = json_json_orientation

    json_columns: None | str | Unset
    if isinstance(columns, Unset):
        json_columns = UNSET
    else:
        json_columns = columns
    params["columns"] = json_columns

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/inventories/{inventory_id}/data/{partition_index}".format(
            domain_id=quote(str(domain_id), safe=""),
            inventory_id=quote(str(inventory_id), safe=""),
            partition_index=quote(str(partition_index), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | InventoryDataResponse | None:
    if response.status_code == 200:
        response_200 = InventoryDataResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | InventoryDataResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    inventory_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
    format_: InventoryDataFormat | Unset = UNSET,
    json_orientation: InventoryJsonOrientation | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InventoryDataResponse]:
    """Get inventory data for a partition

     # Get Inventory Data

    Reads a single partition of a completed inventory's Parquet data on GCS.
    Returns the tree records as JSON (split or records orientation) or CSV.

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **format**: Response format: `json` (default) or `csv`.
    - **json_orientation**: JSON layout: `split` (default, compact) or
      `records` (self-describing). Ignored for CSV.
    - **columns**: Comma-separated column subset (default: all).

    ## Response

    **JSON split** (default): column names + 2D array of values.

    **JSON records**: list of row objects.

    **CSV**: `text/csv` body with metadata in response headers
    `X-Partition-Index`, `X-Row-Count`, `X-Total-Rows`, `X-Num-Partitions`.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        format_ (InventoryDataFormat | Unset):
        json_orientation (InventoryJsonOrientation | Unset):
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InventoryDataResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        partition_index=partition_index,
        format_=format_,
        json_orientation=json_orientation,
        columns=columns,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    inventory_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
    format_: InventoryDataFormat | Unset = UNSET,
    json_orientation: InventoryJsonOrientation | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> HTTPValidationError | InventoryDataResponse | None:
    """Get inventory data for a partition

     # Get Inventory Data

    Reads a single partition of a completed inventory's Parquet data on GCS.
    Returns the tree records as JSON (split or records orientation) or CSV.

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **format**: Response format: `json` (default) or `csv`.
    - **json_orientation**: JSON layout: `split` (default, compact) or
      `records` (self-describing). Ignored for CSV.
    - **columns**: Comma-separated column subset (default: all).

    ## Response

    **JSON split** (default): column names + 2D array of values.

    **JSON records**: list of row objects.

    **CSV**: `text/csv` body with metadata in response headers
    `X-Partition-Index`, `X-Row-Count`, `X-Total-Rows`, `X-Num-Partitions`.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        format_ (InventoryDataFormat | Unset):
        json_orientation (InventoryJsonOrientation | Unset):
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InventoryDataResponse
    """

    return sync_detailed(
        domain_id=domain_id,
        inventory_id=inventory_id,
        partition_index=partition_index,
        client=client,
        format_=format_,
        json_orientation=json_orientation,
        columns=columns,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    inventory_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
    format_: InventoryDataFormat | Unset = UNSET,
    json_orientation: InventoryJsonOrientation | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InventoryDataResponse]:
    """Get inventory data for a partition

     # Get Inventory Data

    Reads a single partition of a completed inventory's Parquet data on GCS.
    Returns the tree records as JSON (split or records orientation) or CSV.

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **format**: Response format: `json` (default) or `csv`.
    - **json_orientation**: JSON layout: `split` (default, compact) or
      `records` (self-describing). Ignored for CSV.
    - **columns**: Comma-separated column subset (default: all).

    ## Response

    **JSON split** (default): column names + 2D array of values.

    **JSON records**: list of row objects.

    **CSV**: `text/csv` body with metadata in response headers
    `X-Partition-Index`, `X-Row-Count`, `X-Total-Rows`, `X-Num-Partitions`.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        format_ (InventoryDataFormat | Unset):
        json_orientation (InventoryJsonOrientation | Unset):
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InventoryDataResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        partition_index=partition_index,
        format_=format_,
        json_orientation=json_orientation,
        columns=columns,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    inventory_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
    format_: InventoryDataFormat | Unset = UNSET,
    json_orientation: InventoryJsonOrientation | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> HTTPValidationError | InventoryDataResponse | None:
    """Get inventory data for a partition

     # Get Inventory Data

    Reads a single partition of a completed inventory's Parquet data on GCS.
    Returns the tree records as JSON (split or records orientation) or CSV.

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **format**: Response format: `json` (default) or `csv`.
    - **json_orientation**: JSON layout: `split` (default, compact) or
      `records` (self-describing). Ignored for CSV.
    - **columns**: Comma-separated column subset (default: all).

    ## Response

    **JSON split** (default): column names + 2D array of values.

    **JSON records**: list of row objects.

    **CSV**: `text/csv` body with metadata in response headers
    `X-Partition-Index`, `X-Row-Count`, `X-Total-Rows`, `X-Num-Partitions`.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        format_ (InventoryDataFormat | Unset):
        json_orientation (InventoryJsonOrientation | Unset):
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InventoryDataResponse
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            inventory_id=inventory_id,
            partition_index=partition_index,
            client=client,
            format_=format_,
            json_orientation=json_orientation,
            columns=columns,
        )
    ).parsed
