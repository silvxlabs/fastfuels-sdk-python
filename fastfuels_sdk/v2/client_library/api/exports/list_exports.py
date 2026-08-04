from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export_sort_field import ExportSortField
from ...models.http_validation_error import HTTPValidationError
from ...models.list_exports_response import ListExportsResponse
from ...models.sort_order import SortOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: ExportSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    domain_id: None | str | Unset = UNSET,
    source_name: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["size"] = size

    json_sort_by: None | str | Unset
    if isinstance(sort_by, Unset):
        json_sort_by = UNSET
    elif isinstance(sort_by, ExportSortField):
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

    json_domain_id: None | str | Unset
    if isinstance(domain_id, Unset):
        json_domain_id = UNSET
    else:
        json_domain_id = domain_id
    params["domain_id"] = json_domain_id

    json_source_name: None | str | Unset
    if isinstance(source_name, Unset):
        json_source_name = UNSET
    else:
        json_source_name = source_name
    params["source_name"] = json_source_name

    json_tag: None | str | Unset
    if isinstance(tag, Unset):
        json_tag = UNSET
    else:
        json_tag = tag
    params["tag"] = json_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/exports",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListExportsResponse | None:
    if response.status_code == 200:
        response_200 = ListExportsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListExportsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: ExportSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    domain_id: None | str | Unset = UNSET,
    source_name: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListExportsResponse]:
    """List all exports

     # List Exports Endpoint

    Retrieves a paginated list of all exports belonging to the authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **domain_id**: (string, optional) Filter by source domain.
    - **source_name**: (string, optional) Filter by export format (e.g., `geotiff`).
    - **tag**: (string, optional) Filter exports that contain this tag.

    ## Response

    Returns a paginated list of exports with metadata.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of exports to retrieve per page. Default: 100.
        sort_by (ExportSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        domain_id (None | str | Unset): Filter exports by domain ID.
        source_name (None | str | Unset): Filter exports by source format (e.g., 'geotiff').
        tag (None | str | Unset): Filter exports that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListExportsResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        domain_id=domain_id,
        source_name=source_name,
        tag=tag,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: ExportSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    domain_id: None | str | Unset = UNSET,
    source_name: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> HTTPValidationError | ListExportsResponse | None:
    """List all exports

     # List Exports Endpoint

    Retrieves a paginated list of all exports belonging to the authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **domain_id**: (string, optional) Filter by source domain.
    - **source_name**: (string, optional) Filter by export format (e.g., `geotiff`).
    - **tag**: (string, optional) Filter exports that contain this tag.

    ## Response

    Returns a paginated list of exports with metadata.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of exports to retrieve per page. Default: 100.
        sort_by (ExportSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        domain_id (None | str | Unset): Filter exports by domain ID.
        source_name (None | str | Unset): Filter exports by source format (e.g., 'geotiff').
        tag (None | str | Unset): Filter exports that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListExportsResponse
    """

    return sync_detailed(
        client=client,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        domain_id=domain_id,
        source_name=source_name,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: ExportSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    domain_id: None | str | Unset = UNSET,
    source_name: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListExportsResponse]:
    """List all exports

     # List Exports Endpoint

    Retrieves a paginated list of all exports belonging to the authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **domain_id**: (string, optional) Filter by source domain.
    - **source_name**: (string, optional) Filter by export format (e.g., `geotiff`).
    - **tag**: (string, optional) Filter exports that contain this tag.

    ## Response

    Returns a paginated list of exports with metadata.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of exports to retrieve per page. Default: 100.
        sort_by (ExportSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        domain_id (None | str | Unset): Filter exports by domain ID.
        source_name (None | str | Unset): Filter exports by source format (e.g., 'geotiff').
        tag (None | str | Unset): Filter exports that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListExportsResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
        domain_id=domain_id,
        source_name=source_name,
        tag=tag,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: ExportSortField | None | Unset = UNSET,
    sort_order: None | SortOrder | Unset = UNSET,
    domain_id: None | str | Unset = UNSET,
    source_name: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
) -> HTTPValidationError | ListExportsResponse | None:
    """List all exports

     # List Exports Endpoint

    Retrieves a paginated list of all exports belonging to the authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) Page number (zero-indexed). Default: 0.
    - **size**: (integer, optional) Items per page (1-1000). Default: 100.
    - **sort_by**: (string, optional) Field to sort by: `created_on`, `modified_on`, `name`.
    - **sort_order**: (string, optional) Sort direction: `ascending`, `descending`.
    - **domain_id**: (string, optional) Filter by source domain.
    - **source_name**: (string, optional) Filter by export format (e.g., `geotiff`).
    - **tag**: (string, optional) Filter exports that contain this tag.

    ## Response

    Returns a paginated list of exports with metadata.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of exports to retrieve per page. Default: 100.
        sort_by (ExportSortField | None | Unset): The field to sort results by.
        sort_order (None | SortOrder | Unset): The order to sort results (ascending or
            descending).
        domain_id (None | str | Unset): Filter exports by domain ID.
        source_name (None | str | Unset): Filter exports by source format (e.g., 'geotiff').
        tag (None | str | Unset): Filter exports that contain this tag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListExportsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order,
            domain_id=domain_id,
            source_name=source_name,
            tag=tag,
        )
    ).parsed
