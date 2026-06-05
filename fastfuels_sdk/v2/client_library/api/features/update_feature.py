from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feature import Feature
from ...models.http_validation_error import HTTPValidationError
from ...models.update_feature_request_body import UpdateFeatureRequestBody
from ...types import Response


def _get_kwargs(
    domain_id: str,
    feature_id: str,
    *,
    body: UpdateFeatureRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/domains/{domain_id}/features/{feature_id}".format(
            domain_id=quote(str(domain_id), safe=""),
            feature_id=quote(str(feature_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Feature | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = Feature.from_dict(response.json())

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
) -> Response[Feature | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateFeatureRequestBody,
) -> Response[Feature | HTTPValidationError]:
    """Update a feature

     # Update Feature Endpoint

    Updates the metadata of an existing feature resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the feature belongs to.
    - **feature_id**: (string) The unique identifier of the feature.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the feature.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated feature resource.

    Args:
        domain_id (str):
        feature_id (str):
        body (UpdateFeatureRequestBody): Request body for updating feature metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Feature | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        feature_id=feature_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateFeatureRequestBody,
) -> Feature | HTTPValidationError | None:
    """Update a feature

     # Update Feature Endpoint

    Updates the metadata of an existing feature resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the feature belongs to.
    - **feature_id**: (string) The unique identifier of the feature.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the feature.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated feature resource.

    Args:
        domain_id (str):
        feature_id (str):
        body (UpdateFeatureRequestBody): Request body for updating feature metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Feature | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        feature_id=feature_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateFeatureRequestBody,
) -> Response[Feature | HTTPValidationError]:
    """Update a feature

     # Update Feature Endpoint

    Updates the metadata of an existing feature resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the feature belongs to.
    - **feature_id**: (string) The unique identifier of the feature.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the feature.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated feature resource.

    Args:
        domain_id (str):
        feature_id (str):
        body (UpdateFeatureRequestBody): Request body for updating feature metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Feature | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        feature_id=feature_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateFeatureRequestBody,
) -> Feature | HTTPValidationError | None:
    """Update a feature

     # Update Feature Endpoint

    Updates the metadata of an existing feature resource. Only the fields
    provided in the request body will be modified.

    ## Path Parameters

    - **domain_id**: (string) The domain the feature belongs to.
    - **feature_id**: (string) The unique identifier of the feature.

    ## Request Body

    All fields are optional:

    - **name**: (string) New name for the feature.
    - **description**: (string) New description.
    - **tags**: (array of strings) New tags (replaces existing).

    ## What Cannot Be Updated

    The following fields are immutable:

    - **id**, **domain_id**, **type**, **source**, **georeference**
    - **created_on** (creation timestamp is permanent)

    The **modified_on** field is automatically updated.

    ## Response

    Returns the updated feature resource.

    Args:
        domain_id (str):
        feature_id (str):
        body (UpdateFeatureRequestBody): Request body for updating feature metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Feature | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            feature_id=feature_id,
            client=client,
            body=body,
        )
    ).parsed
