from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.domain import Domain
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Domain | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = Domain.from_dict(response.json())

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
) -> Response[Domain | HTTPValidationError]:
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
) -> Response[Domain | HTTPValidationError]:
    r"""Get a domain by ID

     # Get Domain Endpoint

    This endpoint retrieves a specific domain resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Response

    On success, returns the domain resource with:

    - **id**: (string) The unique identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) The domain geometry features.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
      - Returns 404 for both missing documents and ownership mismatches to avoid
        leaking information about document existence.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> Domain | HTTPValidationError | None:
    r"""Get a domain by ID

     # Get Domain Endpoint

    This endpoint retrieves a specific domain resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Response

    On success, returns the domain resource with:

    - **id**: (string) The unique identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) The domain geometry features.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
      - Returns 404 for both missing documents and ownership mismatches to avoid
        leaking information about document existence.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Domain | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Domain | HTTPValidationError]:
    r"""Get a domain by ID

     # Get Domain Endpoint

    This endpoint retrieves a specific domain resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Response

    On success, returns the domain resource with:

    - **id**: (string) The unique identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) The domain geometry features.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
      - Returns 404 for both missing documents and ownership mismatches to avoid
        leaking information about document existence.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> Domain | HTTPValidationError | None:
    r"""Get a domain by ID

     # Get Domain Endpoint

    This endpoint retrieves a specific domain resource by its unique identifier.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Response

    On success, returns the domain resource with:

    - **id**: (string) The unique identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) The domain geometry features.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
      - Returns 404 for both missing documents and ownership mismatches to avoid
        leaking information about document existence.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Domain | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
        )
    ).parsed
