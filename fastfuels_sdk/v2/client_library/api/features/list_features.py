from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feature_sort_field import FeatureSortField
from ...models.feature_type import FeatureType
from ...models.http_validation_error import HTTPValidationError
from ...models.list_features_response import ListFeaturesResponse
from ...models.sort_order import SortOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    *,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: FeatureSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: FeatureType | None | Unset = UNSET,
    product: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["size"] = size

    json_sort_by: None | str | Unset
    if isinstance(sort_by, Unset):
        json_sort_by = UNSET
    elif isinstance(sort_by, FeatureSortField):
        json_sort_by = sort_by.value
    else:
        json_sort_by = sort_by
    params["sort_by"] = json_sort_by

    json_sort_order: None | str | Unset
    if isinstance(sort_order, Unset):
        json_sort_order = UNSET
    elif isinstance(sort_order, SortOrder):
        json_sort_order = sort_order.value
    else:
        json_sort_order = sort_order
    params["sort_order"] = json_sort_order

    json_type_: None | str | Unset
    if isinstance(type_, Unset):
        json_type_ = UNSET
    elif isinstance(type_, FeatureType):
        json_type_ = type_.value
    else:
        json_type_ = type_
    params["type"] = json_type_

    json_product: None | str | Unset
    if isinstance(product, Unset):
        json_product = UNSET
    else:
        json_product = product
    params["product"] = json_product

    json_tag: None | str | Unset
    if isinstance(tag, Unset):
        json_tag = UNSET
    else:
        json_tag = tag
    params["tag"] = json_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/features".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListFeaturesResponse | None:
    if response.status_code == 200:
        response_200 = ListFeaturesResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListFeaturesResponse]:
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
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: FeatureSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: FeatureType | None | Unset = UNSET,
    product: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListFeaturesResponse]:
    """List all features

     # List Features Endpoint

    Retrieves a paginated list of all features within a domain belonging to
    the authenticated user.

    ## Path Parameters

    - **domain_id**: (string) The domain to list features for.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **type**: (string, optional) Filter by entity type (e.g., `road`).
    - **product**: (string, optional) Filter by source product (e.g., `osm`).
    - **tag**: (string, optional) Filter features that contain this tag.

    ## Response

    Returns a paginated list of features with metadata.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of features to retrieve per page. Default: 100.
        sort_by (FeatureSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (FeatureType | None | Unset): Filter features by entity type (e.g., 'road',
            'water').
        product (None | str | Unset): Filter features by source product (e.g., 'osm').
        tag (None | str | Unset): Filter features that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListFeaturesResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        type_=type_,
        product=product,
        tag=tag,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: FeatureSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: FeatureType | None | Unset = UNSET,
    product: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> HTTPValidationError | ListFeaturesResponse | None:
    """List all features

     # List Features Endpoint

    Retrieves a paginated list of all features within a domain belonging to
    the authenticated user.

    ## Path Parameters

    - **domain_id**: (string) The domain to list features for.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **type**: (string, optional) Filter by entity type (e.g., `road`).
    - **product**: (string, optional) Filter by source product (e.g., `osm`).
    - **tag**: (string, optional) Filter features that contain this tag.

    ## Response

    Returns a paginated list of features with metadata.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of features to retrieve per page. Default: 100.
        sort_by (FeatureSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (FeatureType | None | Unset): Filter features by entity type (e.g., 'road',
            'water').
        product (None | str | Unset): Filter features by source product (e.g., 'osm').
        tag (None | str | Unset): Filter features that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListFeaturesResponse
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        type_=type_,
        product=product,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: FeatureSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: FeatureType | None | Unset = UNSET,
    product: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListFeaturesResponse]:
    """List all features

     # List Features Endpoint

    Retrieves a paginated list of all features within a domain belonging to
    the authenticated user.

    ## Path Parameters

    - **domain_id**: (string) The domain to list features for.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **type**: (string, optional) Filter by entity type (e.g., `road`).
    - **product**: (string, optional) Filter by source product (e.g., `osm`).
    - **tag**: (string, optional) Filter features that contain this tag.

    ## Response

    Returns a paginated list of features with metadata.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of features to retrieve per page. Default: 100.
        sort_by (FeatureSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (FeatureType | None | Unset): Filter features by entity type (e.g., 'road',
            'water').
        product (None | str | Unset): Filter features by source product (e.g., 'osm').
        tag (None | str | Unset): Filter features that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListFeaturesResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        type_=type_,
        product=product,
        tag=tag,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: FeatureSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: FeatureType | None | Unset = UNSET,
    product: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> HTTPValidationError | ListFeaturesResponse | None:
    """List all features

     # List Features Endpoint

    Retrieves a paginated list of all features within a domain belonging to
    the authenticated user.

    ## Path Parameters

    - **domain_id**: (string) The domain to list features for.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **type**: (string, optional) Filter by entity type (e.g., `road`).
    - **product**: (string, optional) Filter by source product (e.g., `osm`).
    - **tag**: (string, optional) Filter features that contain this tag.

    ## Response

    Returns a paginated list of features with metadata.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of features to retrieve per page. Default: 100.
        sort_by (FeatureSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (FeatureType | None | Unset): Filter features by entity type (e.g., 'road',
            'water').
        product (None | str | Unset): Filter features by source product (e.g., 'osm').
        tag (None | str | Unset): Filter features that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListFeaturesResponse
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order,
            type_=type_,
            product=product,
            tag=tag,
        )
    ).parsed
