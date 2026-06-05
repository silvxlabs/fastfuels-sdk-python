from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.application import Application
from ...models.http_validation_error import HTTPValidationError
from ...models.update_application_request import UpdateApplicationRequest
from ...types import Response


def _get_kwargs(
    application_id: str,
    *,
    body: UpdateApplicationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/applications/{application_id}".format(
            application_id=quote(str(application_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Application | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = Application.from_dict(response.json())

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
) -> Response[Application | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    application_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateApplicationRequest,
) -> Response[Application | HTTPValidationError]:
    """Update an application

     Update an application's name or description.

    Args:
        application_id (str):
        body (UpdateApplicationRequest): Request body for updating an application.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Application | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    application_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateApplicationRequest,
) -> Application | HTTPValidationError | None:
    """Update an application

     Update an application's name or description.

    Args:
        application_id (str):
        body (UpdateApplicationRequest): Request body for updating an application.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Application | HTTPValidationError
    """

    return sync_detailed(
        application_id=application_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    application_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateApplicationRequest,
) -> Response[Application | HTTPValidationError]:
    """Update an application

     Update an application's name or description.

    Args:
        application_id (str):
        body (UpdateApplicationRequest): Request body for updating an application.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Application | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateApplicationRequest,
) -> Application | HTTPValidationError | None:
    """Update an application

     Update an application's name or description.

    Args:
        application_id (str):
        body (UpdateApplicationRequest): Request body for updating an application.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Application | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            application_id=application_id,
            client=client,
            body=body,
        )
    ).parsed
