from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.domain import Domain
from ...models.http_validation_error import HTTPValidationError
from ...models.update_domain_request_body import UpdateDomainRequestBody
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: UpdateDomainRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/domains/{domain_id}".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: UpdateDomainRequestBody,
) -> Response[Domain | HTTPValidationError]:
    r"""Update a domain

     # Update Domain Endpoint

    This endpoint updates the metadata of an existing domain resource. Only the
    fields provided in the request body will be modified; other fields remain
    unchanged.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Request Body

    All fields are optional. Only provided fields will be updated.

    - **name**: (string, optional) The new name for the domain.
    - **description**: (string, optional) The new description for the domain.
    - **tags**: (array of strings, optional) The new tags for the domain.
      This replaces the existing tags array entirely.

    ## What Cannot Be Updated

    The following fields are immutable after domain creation:

    - **id**: The domain identifier is permanent.
    - **features**: Geometry cannot be modified. Create a new domain instead.
    - **crs**: Coordinate reference system is tied to the geometry.
    - **created_on**: Creation timestamp is permanent.

    The **modified_on** field is automatically updated to the current time.

    ## Response

    On success, returns the updated domain resource with all fields,
    including the new `modified_on` timestamp.

    ## Example Request

    ```http
    PATCH /v2/domains/abc123def456...
    Content-Type: application/json

    {
      \"name\": \"Updated Domain Name\",
      \"tags\": [\"production\", \"verified\"]
    }
    ```

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **422 Unprocessable Entity**: Invalid request body.

    Args:
        domain_id (str):
        body (UpdateDomainRequestBody): Request body for updating a domain's metadata.

            All fields are optional. Only provided fields will be updated.
            Geometry (features) and CRS cannot be modified after creation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateDomainRequestBody,
) -> Domain | HTTPValidationError | None:
    r"""Update a domain

     # Update Domain Endpoint

    This endpoint updates the metadata of an existing domain resource. Only the
    fields provided in the request body will be modified; other fields remain
    unchanged.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Request Body

    All fields are optional. Only provided fields will be updated.

    - **name**: (string, optional) The new name for the domain.
    - **description**: (string, optional) The new description for the domain.
    - **tags**: (array of strings, optional) The new tags for the domain.
      This replaces the existing tags array entirely.

    ## What Cannot Be Updated

    The following fields are immutable after domain creation:

    - **id**: The domain identifier is permanent.
    - **features**: Geometry cannot be modified. Create a new domain instead.
    - **crs**: Coordinate reference system is tied to the geometry.
    - **created_on**: Creation timestamp is permanent.

    The **modified_on** field is automatically updated to the current time.

    ## Response

    On success, returns the updated domain resource with all fields,
    including the new `modified_on` timestamp.

    ## Example Request

    ```http
    PATCH /v2/domains/abc123def456...
    Content-Type: application/json

    {
      \"name\": \"Updated Domain Name\",
      \"tags\": [\"production\", \"verified\"]
    }
    ```

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **422 Unprocessable Entity**: Invalid request body.

    Args:
        domain_id (str):
        body (UpdateDomainRequestBody): Request body for updating a domain's metadata.

            All fields are optional. Only provided fields will be updated.
            Geometry (features) and CRS cannot be modified after creation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Domain | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateDomainRequestBody,
) -> Response[Domain | HTTPValidationError]:
    r"""Update a domain

     # Update Domain Endpoint

    This endpoint updates the metadata of an existing domain resource. Only the
    fields provided in the request body will be modified; other fields remain
    unchanged.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Request Body

    All fields are optional. Only provided fields will be updated.

    - **name**: (string, optional) The new name for the domain.
    - **description**: (string, optional) The new description for the domain.
    - **tags**: (array of strings, optional) The new tags for the domain.
      This replaces the existing tags array entirely.

    ## What Cannot Be Updated

    The following fields are immutable after domain creation:

    - **id**: The domain identifier is permanent.
    - **features**: Geometry cannot be modified. Create a new domain instead.
    - **crs**: Coordinate reference system is tied to the geometry.
    - **created_on**: Creation timestamp is permanent.

    The **modified_on** field is automatically updated to the current time.

    ## Response

    On success, returns the updated domain resource with all fields,
    including the new `modified_on` timestamp.

    ## Example Request

    ```http
    PATCH /v2/domains/abc123def456...
    Content-Type: application/json

    {
      \"name\": \"Updated Domain Name\",
      \"tags\": [\"production\", \"verified\"]
    }
    ```

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **422 Unprocessable Entity**: Invalid request body.

    Args:
        domain_id (str):
        body (UpdateDomainRequestBody): Request body for updating a domain's metadata.

            All fields are optional. Only provided fields will be updated.
            Geometry (features) and CRS cannot be modified after creation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateDomainRequestBody,
) -> Domain | HTTPValidationError | None:
    r"""Update a domain

     # Update Domain Endpoint

    This endpoint updates the metadata of an existing domain resource. Only the
    fields provided in the request body will be modified; other fields remain
    unchanged.

    ## Path Parameters

    - **domain_id**: (string) The unique 32-character hex identifier of the domain.

    ## Request Body

    All fields are optional. Only provided fields will be updated.

    - **name**: (string, optional) The new name for the domain.
    - **description**: (string, optional) The new description for the domain.
    - **tags**: (array of strings, optional) The new tags for the domain.
      This replaces the existing tags array entirely.

    ## What Cannot Be Updated

    The following fields are immutable after domain creation:

    - **id**: The domain identifier is permanent.
    - **features**: Geometry cannot be modified. Create a new domain instead.
    - **crs**: Coordinate reference system is tied to the geometry.
    - **created_on**: Creation timestamp is permanent.

    The **modified_on** field is automatically updated to the current time.

    ## Response

    On success, returns the updated domain resource with all fields,
    including the new `modified_on` timestamp.

    ## Example Request

    ```http
    PATCH /v2/domains/abc123def456...
    Content-Type: application/json

    {
      \"name\": \"Updated Domain Name\",
      \"tags\": [\"production\", \"verified\"]
    }
    ```

    ## Error Responses

    - **404 Not Found**: The domain does not exist or the user does not have access.
    - **422 Unprocessable Entity**: Invalid request body.

    Args:
        domain_id (str):
        body (UpdateDomainRequestBody): Request body for updating a domain's metadata.

            All fields are optional. Only provided fields will be updated.
            Geometry (features) and CRS cannot be modified after creation.

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
            body=body,
        )
    ).parsed
