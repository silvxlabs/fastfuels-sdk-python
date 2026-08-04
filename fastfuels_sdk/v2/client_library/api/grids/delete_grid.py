from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    grid_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/domains/{domain_id}/grids/{grid_id}".format(
            domain_id=quote(str(domain_id), safe=""),
            grid_id=quote(str(grid_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Delete a grid

     # Delete Grid Endpoint

    Permanently deletes a grid resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.

    ## Response

    Returns HTTP 204 No Content with an empty response body.

    ## Error Responses

    - **404 Not Found**: The grid does not exist or the user does not have access.

    Args:
        domain_id (str):
        grid_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Delete a grid

     # Delete Grid Endpoint

    Permanently deletes a grid resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.

    ## Response

    Returns HTTP 204 No Content with an empty response body.

    ## Error Responses

    - **404 Not Found**: The grid does not exist or the user does not have access.

    Args:
        domain_id (str):
        grid_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        grid_id=grid_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Delete a grid

     # Delete Grid Endpoint

    Permanently deletes a grid resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.

    ## Response

    Returns HTTP 204 No Content with an empty response body.

    ## Error Responses

    - **404 Not Found**: The grid does not exist or the user does not have access.

    Args:
        domain_id (str):
        grid_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Delete a grid

     # Delete Grid Endpoint

    Permanently deletes a grid resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The domain the grid belongs to.
    - **grid_id**: (string) The unique identifier of the grid.

    ## Response

    Returns HTTP 204 No Content with an empty response body.

    ## Error Responses

    - **404 Not Found**: The grid does not exist or the user does not have access.

    Args:
        domain_id (str):
        grid_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            grid_id=grid_id,
            client=client,
        )
    ).parsed
