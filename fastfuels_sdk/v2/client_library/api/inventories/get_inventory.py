from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...types import Response


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/inventories/{inventory_id}".format(
            domain_id=quote(str(domain_id), safe=""),
            inventory_id=quote(str(inventory_id), safe=""),
        ),
    }

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
) -> Response[HTTPValidationError | Inventory]:
    """Get an inventory by ID

     # Get Inventory Endpoint

    Retrieves a specific inventory resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique 32-character hex identifier of the inventory.

    ## Response

    Returns the inventory resource.

    ## Error Responses

    - **404 Not Found**: The inventory does not exist or the user does not have access.

    Args:
        domain_id (str):
        inventory_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory]
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
) -> HTTPValidationError | Inventory | None:
    """Get an inventory by ID

     # Get Inventory Endpoint

    Retrieves a specific inventory resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique 32-character hex identifier of the inventory.

    ## Response

    Returns the inventory resource.

    ## Error Responses

    - **404 Not Found**: The inventory does not exist or the user does not have access.

    Args:
        domain_id (str):
        inventory_id (str):

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
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | Inventory]:
    """Get an inventory by ID

     # Get Inventory Endpoint

    Retrieves a specific inventory resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique 32-character hex identifier of the inventory.

    ## Response

    Returns the inventory resource.

    ## Error Responses

    - **404 Not Found**: The inventory does not exist or the user does not have access.

    Args:
        domain_id (str):
        inventory_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory]
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
) -> HTTPValidationError | Inventory | None:
    """Get an inventory by ID

     # Get Inventory Endpoint

    Retrieves a specific inventory resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The domain the inventory belongs to.
    - **inventory_id**: (string) The unique 32-character hex identifier of the inventory.

    ## Response

    Returns the inventory resource.

    ## Error Responses

    - **404 Not Found**: The inventory does not exist or the user does not have access.

    Args:
        domain_id (str):
        inventory_id (str):

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
        )
    ).parsed
