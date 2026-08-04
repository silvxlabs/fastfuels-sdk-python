from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_domain_request_body import CreateDomainRequestBody
from ...models.domain import Domain
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: CreateDomainRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/preview",
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
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
) -> Response[Domain | HTTPValidationError]:
    r"""Preview a domain without persisting it

     # Preview Domain Endpoint

    Runs the same validation and projection pipeline as `POST /v2/domains` but
    returns the resulting `Domain` resource without writing to Firestore. Use
    this to let users inspect the projected, padded bounding box before committing
    to a create.

    ## Request Body

    Identical to `POST /v2/domains`. See that endpoint for full documentation.

    ## Response

    Returns the same `Domain` response model as create, with:

    - **id**: Always `\"preview\"` — not a real domain identifier.
    - **created_on** / **modified_on**: Set to the current request time (not persisted).
    - **features**: A single `\"domain\"` feature (the working extent),
      identical to what create would return.
    - **bbox**: Bounding box of the `\"domain\"` feature.
    - **crs**: Projected CRS, identical to what create would return.

    ## Error Responses

    Same 422 error responses as `POST /v2/domains`:

    - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
    - \"Invalid geometry. The feature must have an area greater than zero.\"
    - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
    - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
) -> Domain | HTTPValidationError | None:
    r"""Preview a domain without persisting it

     # Preview Domain Endpoint

    Runs the same validation and projection pipeline as `POST /v2/domains` but
    returns the resulting `Domain` resource without writing to Firestore. Use
    this to let users inspect the projected, padded bounding box before committing
    to a create.

    ## Request Body

    Identical to `POST /v2/domains`. See that endpoint for full documentation.

    ## Response

    Returns the same `Domain` response model as create, with:

    - **id**: Always `\"preview\"` — not a real domain identifier.
    - **created_on** / **modified_on**: Set to the current request time (not persisted).
    - **features**: A single `\"domain\"` feature (the working extent),
      identical to what create would return.
    - **bbox**: Bounding box of the `\"domain\"` feature.
    - **crs**: Projected CRS, identical to what create would return.

    ## Error Responses

    Same 422 error responses as `POST /v2/domains`:

    - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
    - \"Invalid geometry. The feature must have an area greater than zero.\"
    - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
    - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Domain | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
) -> Response[Domain | HTTPValidationError]:
    r"""Preview a domain without persisting it

     # Preview Domain Endpoint

    Runs the same validation and projection pipeline as `POST /v2/domains` but
    returns the resulting `Domain` resource without writing to Firestore. Use
    this to let users inspect the projected, padded bounding box before committing
    to a create.

    ## Request Body

    Identical to `POST /v2/domains`. See that endpoint for full documentation.

    ## Response

    Returns the same `Domain` response model as create, with:

    - **id**: Always `\"preview\"` — not a real domain identifier.
    - **created_on** / **modified_on**: Set to the current request time (not persisted).
    - **features**: A single `\"domain\"` feature (the working extent),
      identical to what create would return.
    - **bbox**: Bounding box of the `\"domain\"` feature.
    - **crs**: Projected CRS, identical to what create would return.

    ## Error Responses

    Same 422 error responses as `POST /v2/domains`:

    - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
    - \"Invalid geometry. The feature must have an area greater than zero.\"
    - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
    - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
) -> Domain | HTTPValidationError | None:
    r"""Preview a domain without persisting it

     # Preview Domain Endpoint

    Runs the same validation and projection pipeline as `POST /v2/domains` but
    returns the resulting `Domain` resource without writing to Firestore. Use
    this to let users inspect the projected, padded bounding box before committing
    to a create.

    ## Request Body

    Identical to `POST /v2/domains`. See that endpoint for full documentation.

    ## Response

    Returns the same `Domain` response model as create, with:

    - **id**: Always `\"preview\"` — not a real domain identifier.
    - **created_on** / **modified_on**: Set to the current request time (not persisted).
    - **features**: A single `\"domain\"` feature (the working extent),
      identical to what create would return.
    - **bbox**: Bounding box of the `\"domain\"` feature.
    - **crs**: Projected CRS, identical to what create would return.

    ## Error Responses

    Same 422 error responses as `POST /v2/domains`:

    - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
    - \"Invalid geometry. The feature must have an area greater than zero.\"
    - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
    - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Domain | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
