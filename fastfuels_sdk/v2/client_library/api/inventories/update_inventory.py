from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.update_inventory_request_body import UpdateInventoryRequestBody
from ...types import Response


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
    *,
    body: UpdateInventoryRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/domains/{domain_id}/inventories/{inventory_id}".format(
            domain_id=quote(str(domain_id), safe=""),
            inventory_id=quote(str(inventory_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | Inventory | None:
    if response.status_code == 200:
        response_200 = Inventory.from_dict(response.json())

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
) -> Response[HTTPValidationError | Inventory]:
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
    body: UpdateInventoryRequestBody,
) -> Response[HTTPValidationError | Inventory]:
    """Update an inventory

     # Update Inventory Endpoint

    Updates the metadata of an existing inventory resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique identifier of the inventory.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the inventory.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **modifications**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the inventory's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated inventory resource.

    Args:
        domain_id (str):
        inventory_id (str):
        body (UpdateInventoryRequestBody): Request body for updating inventory metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        body=body,
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
    body: UpdateInventoryRequestBody,
) -> HTTPValidationError | Inventory | None:
    """Update an inventory

     # Update Inventory Endpoint

    Updates the metadata of an existing inventory resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique identifier of the inventory.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the inventory.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **modifications**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the inventory's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated inventory resource.

    Args:
        domain_id (str):
        inventory_id (str):
        body (UpdateInventoryRequestBody): Request body for updating inventory metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory
    """

    return sync_detailed(
        domain_id=domain_id,
        inventory_id=inventory_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateInventoryRequestBody,
) -> Response[HTTPValidationError | Inventory]:
    """Update an inventory

     # Update Inventory Endpoint

    Updates the metadata of an existing inventory resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique identifier of the inventory.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the inventory.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **modifications**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the inventory's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated inventory resource.

    Args:
        domain_id (str):
        inventory_id (str):
        body (UpdateInventoryRequestBody): Request body for updating inventory metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateInventoryRequestBody,
) -> HTTPValidationError | Inventory | None:
    """Update an inventory

     # Update Inventory Endpoint

    Updates the metadata of an existing inventory resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique identifier of the inventory.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the inventory.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **modifications**, **georeference**
    - **created_on** (creation timestamp is permanent)
    - **checksum** (changes only when the inventory's content is rebuilt, never
      via metadata updates)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated inventory resource.

    Args:
        domain_id (str):
        inventory_id (str):
        body (UpdateInventoryRequestBody): Request body for updating inventory metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            inventory_id=inventory_id,
            client=client,
            body=body,
        )
    ).parsed
