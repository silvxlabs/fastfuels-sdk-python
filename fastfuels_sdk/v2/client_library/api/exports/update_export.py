from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export import Export
from ...models.http_validation_error import HTTPValidationError
from ...models.update_export_request_body import UpdateExportRequestBody
from ...types import Response


def _get_kwargs(
    export_id: str,
    *,
    body: UpdateExportRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/exports/{export_id}".format(
            export_id=quote(str(export_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: UpdateExportRequestBody,
) -> Response[Export | HTTPValidationError]:
    """Update an export

     # Update Export Endpoint

    Updates the metadata of an existing export resource. Only the fields provided
    in the request body will be modified.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the export.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## Response

    Returns the updated export resource.

    Args:
        export_id (str):
        body (UpdateExportRequestBody): Request body for updating export metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        export_id=export_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    export_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateExportRequestBody,
) -> Export | HTTPValidationError | None:
    """Update an export

     # Update Export Endpoint

    Updates the metadata of an existing export resource. Only the fields provided
    in the request body will be modified.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the export.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## Response

    Returns the updated export resource.

    Args:
        export_id (str):
        body (UpdateExportRequestBody): Request body for updating export metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError
    """

    return sync_detailed(
        export_id=export_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    export_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateExportRequestBody,
) -> Response[Export | HTTPValidationError]:
    """Update an export

     # Update Export Endpoint

    Updates the metadata of an existing export resource. Only the fields provided
    in the request body will be modified.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the export.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## Response

    Returns the updated export resource.

    Args:
        export_id (str):
        body (UpdateExportRequestBody): Request body for updating export metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        export_id=export_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    export_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateExportRequestBody,
) -> Export | HTTPValidationError | None:
    """Update an export

     # Update Export Endpoint

    Updates the metadata of an existing export resource. Only the fields provided
    in the request body will be modified.

    ## Path Parameters

    - **export_id**: (string) The unique identifier of the export.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the export.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## Response

    Returns the updated export resource.

    Args:
        export_id (str):
        body (UpdateExportRequestBody): Request body for updating export metadata.

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
            body=body,
        )
    ).parsed
