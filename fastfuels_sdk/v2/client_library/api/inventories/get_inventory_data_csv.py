from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
    partition_index: int,
    *,
    columns: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_columns: None | str | Unset
    if isinstance(columns, Unset):
        json_columns = UNSET
    else:
        json_columns = columns
    params["columns"] = json_columns

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/inventories/{inventory_id}/data/{partition_index}/csv".format(
            domain_id=quote(str(domain_id), safe=""),
            inventory_id=quote(str(inventory_id), safe=""),
            partition_index=quote(str(partition_index), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | str | None:
    if response.status_code == 200:
        response_200 = response.text
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
) -> Response[HTTPValidationError | str]:
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
    columns: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | str]:
    """Get inventory data for a partition (CSV)

     # Get Inventory Data (CSV)

    Reads a single partition of a completed inventory's Parquet data on GCS and
    returns the tree records as a `text/csv` body with a header row. Use this
    when you want to hand the response straight to a CSV reader.

    For a structured JSON payload, use the JSON variant of this endpoint (drop
    the trailing `/csv`).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **columns**: Comma-separated column subset (default: all).

    ## Response

    A `text/csv` body, with partition metadata in these response headers:

    - `X-Partition-Index`: the partition this body came from.
    - `X-Row-Count`: rows in this partition.
    - `X-Total-Rows`: rows across all partitions of the inventory.
    - `X-Num-Partitions`: total number of partitions.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | str]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        partition_index=partition_index,
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
    columns: None | str | Unset = UNSET,
) -> HTTPValidationError | str | None:
    """Get inventory data for a partition (CSV)

     # Get Inventory Data (CSV)

    Reads a single partition of a completed inventory's Parquet data on GCS and
    returns the tree records as a `text/csv` body with a header row. Use this
    when you want to hand the response straight to a CSV reader.

    For a structured JSON payload, use the JSON variant of this endpoint (drop
    the trailing `/csv`).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **columns**: Comma-separated column subset (default: all).

    ## Response

    A `text/csv` body, with partition metadata in these response headers:

    - `X-Partition-Index`: the partition this body came from.
    - `X-Row-Count`: rows in this partition.
    - `X-Total-Rows`: rows across all partitions of the inventory.
    - `X-Num-Partitions`: total number of partitions.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | str
    """

    return sync_detailed(
        domain_id=domain_id,
        inventory_id=inventory_id,
        partition_index=partition_index,
        client=client,
        columns=columns,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    inventory_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
    columns: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | str]:
    """Get inventory data for a partition (CSV)

     # Get Inventory Data (CSV)

    Reads a single partition of a completed inventory's Parquet data on GCS and
    returns the tree records as a `text/csv` body with a header row. Use this
    when you want to hand the response straight to a CSV reader.

    For a structured JSON payload, use the JSON variant of this endpoint (drop
    the trailing `/csv`).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **columns**: Comma-separated column subset (default: all).

    ## Response

    A `text/csv` body, with partition metadata in these response headers:

    - `X-Partition-Index`: the partition this body came from.
    - `X-Row-Count`: rows in this partition.
    - `X-Total-Rows`: rows across all partitions of the inventory.
    - `X-Num-Partitions`: total number of partitions.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | str]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        partition_index=partition_index,
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
    columns: None | str | Unset = UNSET,
) -> HTTPValidationError | str | None:
    """Get inventory data for a partition (CSV)

     # Get Inventory Data (CSV)

    Reads a single partition of a completed inventory's Parquet data on GCS and
    returns the tree records as a `text/csv` body with a header row. Use this
    when you want to hand the response straight to a CSV reader.

    For a structured JSON payload, use the JSON variant of this endpoint (drop
    the trailing `/csv`).

    ## Path Parameters

    - **domain_id**: The domain the inventory belongs to.
    - **inventory_id**: The unique identifier of the inventory.
    - **partition_index**: Zero-based partition index.

    ## Query Parameters

    - **columns**: Comma-separated column subset (default: all).

    ## Response

    A `text/csv` body, with partition metadata in these response headers:

    - `X-Partition-Index`: the partition this body came from.
    - `X-Row-Count`: rows in this partition.
    - `X-Total-Rows`: rows across all partitions of the inventory.
    - `X-Num-Partitions`: total number of partitions.

    ## Error Responses

    - **404 Not Found**: Inventory does not exist or user does not have access.
    - **422 Unprocessable Entity**: Inventory not completed, partition index
      out of range, invalid column names, or metadata not available.

    Args:
        domain_id (str):
        inventory_id (str):
        partition_index (int): Zero-based partition index.
        columns (None | str | Unset): Comma-separated column subset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | str
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            inventory_id=inventory_id,
            partition_index=partition_index,
            client=client,
            columns=columns,
        )
    ).parsed
