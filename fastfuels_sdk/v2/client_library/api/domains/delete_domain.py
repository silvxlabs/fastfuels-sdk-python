from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    *,
    force: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/domains/{domain_id}".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
        "params": params,
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
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
) -> Response[Any | HTTPValidationError]:
    """Delete a domain

     # Delete Domain Endpoint

    This endpoint permanently deletes a domain resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Query Parameters

    - **force**: (boolean, optional) If true, cascade-deletes all child resources
      (grids, etc.) before deleting the domain. Default: false.

    ## Response

    On success, returns HTTP 204 No Content with an empty response body.

    ## Cascade Behavior (AIP-135)

    - **Without `force`**: If the domain has child grids, returns 412 Precondition
      Failed. Delete child resources first, or use `force=true`.
    - **With `force=true`**: Deletes the domain and all child grids in a single
      operation.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **412 Precondition Failed**: The domain has child resources and `force` was
      not set to true.

    Args:
        domain_id (str):
        force (bool | Unset): Force cascade delete of all child resources (grids, etc.). Without
            this, returns 412 if child resources exist. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        force=force,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
) -> Any | HTTPValidationError | None:
    """Delete a domain

     # Delete Domain Endpoint

    This endpoint permanently deletes a domain resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Query Parameters

    - **force**: (boolean, optional) If true, cascade-deletes all child resources
      (grids, etc.) before deleting the domain. Default: false.

    ## Response

    On success, returns HTTP 204 No Content with an empty response body.

    ## Cascade Behavior (AIP-135)

    - **Without `force`**: If the domain has child grids, returns 412 Precondition
      Failed. Delete child resources first, or use `force=true`.
    - **With `force=true`**: Deletes the domain and all child grids in a single
      operation.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **412 Precondition Failed**: The domain has child resources and `force` was
      not set to true.

    Args:
        domain_id (str):
        force (bool | Unset): Force cascade delete of all child resources (grids, etc.). Without
            this, returns 412 if child resources exist. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        force=force,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
) -> Response[Any | HTTPValidationError]:
    """Delete a domain

     # Delete Domain Endpoint

    This endpoint permanently deletes a domain resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Query Parameters

    - **force**: (boolean, optional) If true, cascade-deletes all child resources
      (grids, etc.) before deleting the domain. Default: false.

    ## Response

    On success, returns HTTP 204 No Content with an empty response body.

    ## Cascade Behavior (AIP-135)

    - **Without `force`**: If the domain has child grids, returns 412 Precondition
      Failed. Delete child resources first, or use `force=true`.
    - **With `force=true`**: Deletes the domain and all child grids in a single
      operation.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **412 Precondition Failed**: The domain has child resources and `force` was
      not set to true.

    Args:
        domain_id (str):
        force (bool | Unset): Force cascade delete of all child resources (grids, etc.). Without
            this, returns 412 if child resources exist. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        force=force,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
) -> Any | HTTPValidationError | None:
    """Delete a domain

     # Delete Domain Endpoint

    This endpoint permanently deletes a domain resource by its unique identifier.
    This action cannot be undone.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Query Parameters

    - **force**: (boolean, optional) If true, cascade-deletes all child resources
      (grids, etc.) before deleting the domain. Default: false.

    ## Response

    On success, returns HTTP 204 No Content with an empty response body.

    ## Cascade Behavior (AIP-135)

    - **Without `force`**: If the domain has child grids, returns 412 Precondition
      Failed. Delete child resources first, or use `force=true`.
    - **With `force=true`**: Deletes the domain and all child grids in a single
      operation.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **412 Precondition Failed**: The domain has child resources and `force` was
      not set to true.

    Args:
        domain_id (str):
        force (bool | Unset): Force cascade delete of all child resources (grids, etc.). Without
            this, returns 412 if child resources exist. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            force=force,
        )
    ).parsed
