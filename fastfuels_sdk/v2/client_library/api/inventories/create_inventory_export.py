from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export import Export
from ...models.export_inventory_request import ExportInventoryRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory_export_format import InventoryExportFormat
from ...types import Response


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
    format_: InventoryExportFormat,
    *,
    body: ExportInventoryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/{inventory_id}/exports/{format_}".format(
            domain_id=quote(str(domain_id), safe=""),
            inventory_id=quote(str(inventory_id), safe=""),
            format_=quote(str(format_), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Export | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = Export.from_dict(response.json())

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
) -> Response[Export | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    inventory_id: str,
    format_: InventoryExportFormat,
    *,
    client: AuthenticatedClient,
    body: ExportInventoryRequest,
) -> Response[Export | HTTPValidationError]:
    """Export an inventory

     Export an inventory to the specified format.

    Supported formats: `parquet` (zipped), `csv`, `geojson`, `geopackage`.

    The inventory must belong to this domain and have status `completed`.
    If `columns` is specified, only those columns are included; otherwise
    all columns are exported.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to get the
    signed download URL.

    Args:
        domain_id (str):
        inventory_id (str):
        format_ (InventoryExportFormat): Supported inventory export formats.
        body (ExportInventoryRequest): Request body for creating an inventory export.

            Used at: POST /domains/{domain_id}/inventories/{inventory_id}/exports/{format}

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        format_=format_,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    inventory_id: str,
    format_: InventoryExportFormat,
    *,
    client: AuthenticatedClient,
    body: ExportInventoryRequest,
) -> Export | HTTPValidationError | None:
    """Export an inventory

     Export an inventory to the specified format.

    Supported formats: `parquet` (zipped), `csv`, `geojson`, `geopackage`.

    The inventory must belong to this domain and have status `completed`.
    If `columns` is specified, only those columns are included; otherwise
    all columns are exported.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to get the
    signed download URL.

    Args:
        domain_id (str):
        inventory_id (str):
        format_ (InventoryExportFormat): Supported inventory export formats.
        body (ExportInventoryRequest): Request body for creating an inventory export.

            Used at: POST /domains/{domain_id}/inventories/{inventory_id}/exports/{format}

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        inventory_id=inventory_id,
        format_=format_,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    inventory_id: str,
    format_: InventoryExportFormat,
    *,
    client: AuthenticatedClient,
    body: ExportInventoryRequest,
) -> Response[Export | HTTPValidationError]:
    """Export an inventory

     Export an inventory to the specified format.

    Supported formats: `parquet` (zipped), `csv`, `geojson`, `geopackage`.

    The inventory must belong to this domain and have status `completed`.
    If `columns` is specified, only those columns are included; otherwise
    all columns are exported.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to get the
    signed download URL.

    Args:
        domain_id (str):
        inventory_id (str):
        format_ (InventoryExportFormat): Supported inventory export formats.
        body (ExportInventoryRequest): Request body for creating an inventory export.

            Used at: POST /domains/{domain_id}/inventories/{inventory_id}/exports/{format}

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        format_=format_,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    inventory_id: str,
    format_: InventoryExportFormat,
    *,
    client: AuthenticatedClient,
    body: ExportInventoryRequest,
) -> Export | HTTPValidationError | None:
    """Export an inventory

     Export an inventory to the specified format.

    Supported formats: `parquet` (zipped), `csv`, `geojson`, `geopackage`.

    The inventory must belong to this domain and have status `completed`.
    If `columns` is specified, only those columns are included; otherwise
    all columns are exported.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to get the
    signed download URL.

    Args:
        domain_id (str):
        inventory_id (str):
        format_ (InventoryExportFormat): Supported inventory export formats.
        body (ExportInventoryRequest): Request body for creating an inventory export.

            Used at: POST /domains/{domain_id}/inventories/{inventory_id}/exports/{format}

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            inventory_id=inventory_id,
            format_=format_,
            client=client,
            body=body,
        )
    ).parsed
