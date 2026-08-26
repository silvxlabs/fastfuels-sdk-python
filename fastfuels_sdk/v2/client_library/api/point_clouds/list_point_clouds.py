from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_point_clouds_response import ListPointCloudsResponse
from ...models.point_cloud_sort_field import PointCloudSortField
from ...models.point_cloud_type import PointCloudType
from ...models.sort_order import SortOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    *,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: None | PointCloudSortField | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: None | PointCloudType | Unset = UNSET,
    source: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["size"] = size

    json_sort_by: None | str | Unset
    if isinstance(sort_by, Unset):
        json_sort_by = UNSET
    elif isinstance(sort_by, PointCloudSortField):
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
    elif isinstance(type_, PointCloudType):
        json_type_ = type_.value
    else:
        json_type_ = type_
    params["type"] = json_type_

    json_source: None | str | Unset
    if isinstance(source, Unset):
        json_source = UNSET
    else:
        json_source = source
    params["source"] = json_source

    json_tag: None | str | Unset
    if isinstance(tag, Unset):
        json_tag = UNSET
    else:
        json_tag = tag
    params["tag"] = json_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/pointclouds".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListPointCloudsResponse | None:
    if response.status_code == 200:
        response_200 = ListPointCloudsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListPointCloudsResponse]:
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
    sort_by: None | PointCloudSortField | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: None | PointCloudType | Unset = UNSET,
    source: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListPointCloudsResponse]:
    """List point clouds in a domain

     # List Point Clouds in a Domain

    Returns a paginated list of point clouds owned by the authenticated caller
    within one domain.

    ## Path Parameters

    - **domain_id**: Domain whose point clouds should be listed.

    ## Query Parameters

    - **page**: Zero-indexed page number. Defaults to `0`.
    - **size**: Results per page, from `1` through `1000`. Defaults to `100`.
    - **sort_by**: Sort by `created_on`, `modified_on`, or `name`.
    - **sort_order**: Sort in `ascending` or `descending` order.
    - **type**: Keep only airborne (`als`) or terrestrial (`tls`) clouds.
    - **source**: Keep only clouds from a source such as `3dep` or `upload`.
    - **tag**: Keep only clouds whose `tags` array contains this value.

    ## Response

    A standard paginated response. `point_clouds` contains the resources on the
    requested page; `current_page`, `page_size`, and `total_items` describe the
    page and the complete filtered result set.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or is not accessible to the
      caller.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of point clouds to retrieve per page. Default: 100.
        sort_by (None | PointCloudSortField | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (None | PointCloudType | Unset): Filter point clouds by acquisition type (`als` or
            `tls`).
        source (None | str | Unset): Filter point clouds by source name (for example, `3dep`).
        tag (None | str | Unset): Filter point clouds that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListPointCloudsResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        type_=type_,
        source=source,
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
    sort_by: None | PointCloudSortField | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: None | PointCloudType | Unset = UNSET,
    source: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> HTTPValidationError | ListPointCloudsResponse | None:
    """List point clouds in a domain

     # List Point Clouds in a Domain

    Returns a paginated list of point clouds owned by the authenticated caller
    within one domain.

    ## Path Parameters

    - **domain_id**: Domain whose point clouds should be listed.

    ## Query Parameters

    - **page**: Zero-indexed page number. Defaults to `0`.
    - **size**: Results per page, from `1` through `1000`. Defaults to `100`.
    - **sort_by**: Sort by `created_on`, `modified_on`, or `name`.
    - **sort_order**: Sort in `ascending` or `descending` order.
    - **type**: Keep only airborne (`als`) or terrestrial (`tls`) clouds.
    - **source**: Keep only clouds from a source such as `3dep` or `upload`.
    - **tag**: Keep only clouds whose `tags` array contains this value.

    ## Response

    A standard paginated response. `point_clouds` contains the resources on the
    requested page; `current_page`, `page_size`, and `total_items` describe the
    page and the complete filtered result set.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or is not accessible to the
      caller.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of point clouds to retrieve per page. Default: 100.
        sort_by (None | PointCloudSortField | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (None | PointCloudType | Unset): Filter point clouds by acquisition type (`als` or
            `tls`).
        source (None | str | Unset): Filter point clouds by source name (for example, `3dep`).
        tag (None | str | Unset): Filter point clouds that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListPointCloudsResponse
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        type_=type_,
        source=source,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: None | PointCloudSortField | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: None | PointCloudType | Unset = UNSET,
    source: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListPointCloudsResponse]:
    """List point clouds in a domain

     # List Point Clouds in a Domain

    Returns a paginated list of point clouds owned by the authenticated caller
    within one domain.

    ## Path Parameters

    - **domain_id**: Domain whose point clouds should be listed.

    ## Query Parameters

    - **page**: Zero-indexed page number. Defaults to `0`.
    - **size**: Results per page, from `1` through `1000`. Defaults to `100`.
    - **sort_by**: Sort by `created_on`, `modified_on`, or `name`.
    - **sort_order**: Sort in `ascending` or `descending` order.
    - **type**: Keep only airborne (`als`) or terrestrial (`tls`) clouds.
    - **source**: Keep only clouds from a source such as `3dep` or `upload`.
    - **tag**: Keep only clouds whose `tags` array contains this value.

    ## Response

    A standard paginated response. `point_clouds` contains the resources on the
    requested page; `current_page`, `page_size`, and `total_items` describe the
    page and the complete filtered result set.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or is not accessible to the
      caller.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of point clouds to retrieve per page. Default: 100.
        sort_by (None | PointCloudSortField | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (None | PointCloudType | Unset): Filter point clouds by acquisition type (`als` or
            `tls`).
        source (None | str | Unset): Filter point clouds by source name (for example, `3dep`).
        tag (None | str | Unset): Filter point clouds that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListPointCloudsResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        type_=type_,
        source=source,
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
    sort_by: None | PointCloudSortField | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    type_: None | PointCloudType | Unset = UNSET,
    source: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> HTTPValidationError | ListPointCloudsResponse | None:
    """List point clouds in a domain

     # List Point Clouds in a Domain

    Returns a paginated list of point clouds owned by the authenticated caller
    within one domain.

    ## Path Parameters

    - **domain_id**: Domain whose point clouds should be listed.

    ## Query Parameters

    - **page**: Zero-indexed page number. Defaults to `0`.
    - **size**: Results per page, from `1` through `1000`. Defaults to `100`.
    - **sort_by**: Sort by `created_on`, `modified_on`, or `name`.
    - **sort_order**: Sort in `ascending` or `descending` order.
    - **type**: Keep only airborne (`als`) or terrestrial (`tls`) clouds.
    - **source**: Keep only clouds from a source such as `3dep` or `upload`.
    - **tag**: Keep only clouds whose `tags` array contains this value.

    ## Response

    A standard paginated response. `point_clouds` contains the resources on the
    requested page; `current_page`, `page_size`, and `total_items` describe the
    page and the complete filtered result set.

    ## Error Responses

    - **404 Not Found**: The domain does not exist or is not accessible to the
      caller.

    Args:
        domain_id (str):
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of point clouds to retrieve per page. Default: 100.
        sort_by (None | PointCloudSortField | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        type_ (None | PointCloudType | Unset): Filter point clouds by acquisition type (`als` or
            `tls`).
        source (None | str | Unset): Filter point clouds by source name (for example, `3dep`).
        tag (None | str | Unset): Filter point clouds that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListPointCloudsResponse
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
            source=source,
            tag=tag,
        )
    ).parsed
