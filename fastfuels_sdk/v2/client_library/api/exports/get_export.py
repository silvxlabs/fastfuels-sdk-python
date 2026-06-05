from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export import Export
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    export_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/exports/{export_id}".format(
            export_id=quote(str(export_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Export | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = Export.from_dict(response.json())

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
) -> Response[Export | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    export_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Export | HTTPValidationError]:
    """Get an export by ID

     # Get Export Endpoint

    Retrieves a specific export resource by its unique identifier.
    When the export is completed, the response includes a signed_url.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Response

    Returns the export resource.

    ## Error Responses

    - **404 Not Found**: The export does not exist or the user does not have access.

    Args:
        export_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        export_id=export_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    export_id: str,
    *,
    client: AuthenticatedClient,
) -> Export | HTTPValidationError | None:
    """Get an export by ID

     # Get Export Endpoint

    Retrieves a specific export resource by its unique identifier.
    When the export is completed, the response includes a signed_url.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Response

    Returns the export resource.

    ## Error Responses

    - **404 Not Found**: The export does not exist or the user does not have access.

    Args:
        export_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError
    """

    return sync_detailed(
        export_id=export_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    export_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Export | HTTPValidationError]:
    """Get an export by ID

     # Get Export Endpoint

    Retrieves a specific export resource by its unique identifier.
    When the export is completed, the response includes a signed_url.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Response

    Returns the export resource.

    ## Error Responses

    - **404 Not Found**: The export does not exist or the user does not have access.

    Args:
        export_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        export_id=export_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    export_id: str,
    *,
    client: AuthenticatedClient,
) -> Export | HTTPValidationError | None:
    """Get an export by ID

     # Get Export Endpoint

    Retrieves a specific export resource by its unique identifier.
    When the export is completed, the response includes a signed_url.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Response

    Returns the export resource.

    ## Error Responses

    - **404 Not Found**: The export does not exist or the user does not have access.

    Args:
        export_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            export_id=export_id,
            client=client,
        )
    ).parsed
