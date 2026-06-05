from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.domain_sort_field import DomainSortField
from ...models.domain_sort_order import DomainSortOrder
from ...models.http_validation_error import HTTPValidationError
from ...models.list_domains_response import ListDomainsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: DomainSortField | None | Unset = UNSET,
    sort_order: DomainSortOrder | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["size"] = size

    json_sort_by: None | str | Unset
    if isinstance(sort_by, Unset):
        json_sort_by = UNSET
    elif isinstance(sort_by, DomainSortField):
        json_sort_by = sort_by.value
    else:
        json_sort_by = sort_by
    params["sort_by"] = json_sort_by

    json_sort_order: None | str | Unset
    if isinstance(sort_order, Unset):
        json_sort_order = UNSET
    elif isinstance(sort_order, DomainSortOrder):
        json_sort_order = sort_order.value
    else:
        json_sort_order = sort_order
    params["sort_order"] = json_sort_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListDomainsResponse | None:
    if response.status_code == 200:
        response_200 = ListDomainsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListDomainsResponse]:
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
    sort_by: DomainSortField | None | Unset = UNSET,
    sort_order: DomainSortOrder | None | Unset = UNSET,
) -> Response[HTTPValidationError | ListDomainsResponse]:
    r"""List all domains

     # List Domains Endpoint

    This endpoint retrieves a paginated list of all domains belonging to the
    authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) The page number to retrieve. Zero-indexed,
      meaning the first page is `0`. Default: 0.
    - **size**: (integer, optional) The number of domains to retrieve per page.
      Must be between 1 and 1000. Default: 100.
    - **sort_by**: (string, optional) The field to sort results by. Valid values:
      - `created_on`: Sort by creation date.
      - `modified_on`: Sort by last modification date.
      - `name`: Sort alphabetically by name.
    - **sort_order**: (string, optional) The order to sort results. Valid values:
      - `ascending`: Sort in ascending order (A-Z, oldest first).
      - `descending`: Sort in descending order (Z-A, newest first).
      Default: descending when sort_by is specified.

    ## Response

    Returns a paginated list of domains with metadata:

    - **domains**: (array) List of domain resources for the current page.
      Each domain includes:
      - **id**: (string) The unique identifier for the domain.
      - **type**: (string) Always \"FeatureCollection\".
      - **name**: (string) The name of the domain.
      - **description**: (string) The description of the domain.
      - **created_on**: (datetime) When the domain was created.
      - **modified_on**: (datetime) When the domain was last modified.
      - **tags**: (array) The tags associated with the domain.
      - **crs**: (object) The coordinate reference system.
      - **features**: (array) The domain geometry features.
    - **current_page**: (integer) The current page number (zero-indexed).
    - **page_size**: (integer) The number of domains per page.
    - **total_items**: (integer) The total number of domains owned by the user.

    ## Pagination

    Use `page` and `size` parameters to navigate through large result sets:

    - First page: `?page=0&size=10`
    - Second page: `?page=1&size=10`
    - Calculate total pages: `ceil(total_items / page_size)`

    ## Sorting

    Combine `sort_by` and `sort_order` for custom ordering:

    - Newest first: `?sort_by=created_on&sort_order=descending`
    - Alphabetical: `?sort_by=name&sort_order=ascending`
    - Recently modified: `?sort_by=modified_on&sort_order=descending`

    ## Example Request

    ```http
    GET /v2/domains?page=0&size=10&sort_by=created_on&sort_order=descending
    ```

    ## Example Response

    ```json
    {
      \"domains\": [
        {
          \"id\": \"abc123...\",
          \"type\": \"FeatureCollection\",
          \"name\": \"My Domain\",
          \"description\": \"A test domain\",
          \"created_on\": \"2024-01-15T10:30:00\",
          \"modified_on\": \"2024-01-15T10:30:00\",
          \"tags\": [\"test\"],
          \"crs\": {\"type\": \"name\", \"properties\": {\"name\": \"EPSG:32611\"}},
          \"features\": [...]
        }
      ],
      \"current_page\": 0,
      \"page_size\": 10,
      \"total_items\": 42
    }
    ```

    ## Error Responses

    - **422 Unprocessable Entity**: Invalid query parameters.
      - Page must be a non-negative integer.
      - Size must be between 1 and 1000.
      - Invalid sort_by or sort_order values.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of domains to retrieve per page. Default: 100.
        sort_by (DomainSortField | None | Unset): The field to sort results by.
        sort_order (DomainSortOrder | None | Unset): The order to sort results (ascending or
            descending).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListDomainsResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
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
    sort_by: DomainSortField | None | Unset = UNSET,
    sort_order: DomainSortOrder | None | Unset = UNSET,
) -> HTTPValidationError | ListDomainsResponse | None:
    r"""List all domains

     # List Domains Endpoint

    This endpoint retrieves a paginated list of all domains belonging to the
    authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) The page number to retrieve. Zero-indexed,
      meaning the first page is `0`. Default: 0.
    - **size**: (integer, optional) The number of domains to retrieve per page.
      Must be between 1 and 1000. Default: 100.
    - **sort_by**: (string, optional) The field to sort results by. Valid values:
      - `created_on`: Sort by creation date.
      - `modified_on`: Sort by last modification date.
      - `name`: Sort alphabetically by name.
    - **sort_order**: (string, optional) The order to sort results. Valid values:
      - `ascending`: Sort in ascending order (A-Z, oldest first).
      - `descending`: Sort in descending order (Z-A, newest first).
      Default: descending when sort_by is specified.

    ## Response

    Returns a paginated list of domains with metadata:

    - **domains**: (array) List of domain resources for the current page.
      Each domain includes:
      - **id**: (string) The unique identifier for the domain.
      - **type**: (string) Always \"FeatureCollection\".
      - **name**: (string) The name of the domain.
      - **description**: (string) The description of the domain.
      - **created_on**: (datetime) When the domain was created.
      - **modified_on**: (datetime) When the domain was last modified.
      - **tags**: (array) The tags associated with the domain.
      - **crs**: (object) The coordinate reference system.
      - **features**: (array) The domain geometry features.
    - **current_page**: (integer) The current page number (zero-indexed).
    - **page_size**: (integer) The number of domains per page.
    - **total_items**: (integer) The total number of domains owned by the user.

    ## Pagination

    Use `page` and `size` parameters to navigate through large result sets:

    - First page: `?page=0&size=10`
    - Second page: `?page=1&size=10`
    - Calculate total pages: `ceil(total_items / page_size)`

    ## Sorting

    Combine `sort_by` and `sort_order` for custom ordering:

    - Newest first: `?sort_by=created_on&sort_order=descending`
    - Alphabetical: `?sort_by=name&sort_order=ascending`
    - Recently modified: `?sort_by=modified_on&sort_order=descending`

    ## Example Request

    ```http
    GET /v2/domains?page=0&size=10&sort_by=created_on&sort_order=descending
    ```

    ## Example Response

    ```json
    {
      \"domains\": [
        {
          \"id\": \"abc123...\",
          \"type\": \"FeatureCollection\",
          \"name\": \"My Domain\",
          \"description\": \"A test domain\",
          \"created_on\": \"2024-01-15T10:30:00\",
          \"modified_on\": \"2024-01-15T10:30:00\",
          \"tags\": [\"test\"],
          \"crs\": {\"type\": \"name\", \"properties\": {\"name\": \"EPSG:32611\"}},
          \"features\": [...]
        }
      ],
      \"current_page\": 0,
      \"page_size\": 10,
      \"total_items\": 42
    }
    ```

    ## Error Responses

    - **422 Unprocessable Entity**: Invalid query parameters.
      - Page must be a non-negative integer.
      - Size must be between 1 and 1000.
      - Invalid sort_by or sort_order values.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of domains to retrieve per page. Default: 100.
        sort_by (DomainSortField | None | Unset): The field to sort results by.
        sort_order (DomainSortOrder | None | Unset): The order to sort results (ascending or
            descending).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListDomainsResponse
    """

    return sync_detailed(
        client=client,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: DomainSortField | None | Unset = UNSET,
    sort_order: DomainSortOrder | None | Unset = UNSET,
) -> Response[HTTPValidationError | ListDomainsResponse]:
    r"""List all domains

     # List Domains Endpoint

    This endpoint retrieves a paginated list of all domains belonging to the
    authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) The page number to retrieve. Zero-indexed,
      meaning the first page is `0`. Default: 0.
    - **size**: (integer, optional) The number of domains to retrieve per page.
      Must be between 1 and 1000. Default: 100.
    - **sort_by**: (string, optional) The field to sort results by. Valid values:
      - `created_on`: Sort by creation date.
      - `modified_on`: Sort by last modification date.
      - `name`: Sort alphabetically by name.
    - **sort_order**: (string, optional) The order to sort results. Valid values:
      - `ascending`: Sort in ascending order (A-Z, oldest first).
      - `descending`: Sort in descending order (Z-A, newest first).
      Default: descending when sort_by is specified.

    ## Response

    Returns a paginated list of domains with metadata:

    - **domains**: (array) List of domain resources for the current page.
      Each domain includes:
      - **id**: (string) The unique identifier for the domain.
      - **type**: (string) Always \"FeatureCollection\".
      - **name**: (string) The name of the domain.
      - **description**: (string) The description of the domain.
      - **created_on**: (datetime) When the domain was created.
      - **modified_on**: (datetime) When the domain was last modified.
      - **tags**: (array) The tags associated with the domain.
      - **crs**: (object) The coordinate reference system.
      - **features**: (array) The domain geometry features.
    - **current_page**: (integer) The current page number (zero-indexed).
    - **page_size**: (integer) The number of domains per page.
    - **total_items**: (integer) The total number of domains owned by the user.

    ## Pagination

    Use `page` and `size` parameters to navigate through large result sets:

    - First page: `?page=0&size=10`
    - Second page: `?page=1&size=10`
    - Calculate total pages: `ceil(total_items / page_size)`

    ## Sorting

    Combine `sort_by` and `sort_order` for custom ordering:

    - Newest first: `?sort_by=created_on&sort_order=descending`
    - Alphabetical: `?sort_by=name&sort_order=ascending`
    - Recently modified: `?sort_by=modified_on&sort_order=descending`

    ## Example Request

    ```http
    GET /v2/domains?page=0&size=10&sort_by=created_on&sort_order=descending
    ```

    ## Example Response

    ```json
    {
      \"domains\": [
        {
          \"id\": \"abc123...\",
          \"type\": \"FeatureCollection\",
          \"name\": \"My Domain\",
          \"description\": \"A test domain\",
          \"created_on\": \"2024-01-15T10:30:00\",
          \"modified_on\": \"2024-01-15T10:30:00\",
          \"tags\": [\"test\"],
          \"crs\": {\"type\": \"name\", \"properties\": {\"name\": \"EPSG:32611\"}},
          \"features\": [...]
        }
      ],
      \"current_page\": 0,
      \"page_size\": 10,
      \"total_items\": 42
    }
    ```

    ## Error Responses

    - **422 Unprocessable Entity**: Invalid query parameters.
      - Page must be a non-negative integer.
      - Size must be between 1 and 1000.
      - Invalid sort_by or sort_order values.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of domains to retrieve per page. Default: 100.
        sort_by (DomainSortField | None | Unset): The field to sort results by.
        sort_order (DomainSortOrder | None | Unset): The order to sort results (ascending or
            descending).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListDomainsResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 0,
    size: int | Unset = 100,
    sort_by: DomainSortField | None | Unset = UNSET,
    sort_order: DomainSortOrder | None | Unset = UNSET,
) -> HTTPValidationError | ListDomainsResponse | None:
    r"""List all domains

     # List Domains Endpoint

    This endpoint retrieves a paginated list of all domains belonging to the
    authenticated user.

    ## Query Parameters

    - **page**: (integer, optional) The page number to retrieve. Zero-indexed,
      meaning the first page is `0`. Default: 0.
    - **size**: (integer, optional) The number of domains to retrieve per page.
      Must be between 1 and 1000. Default: 100.
    - **sort_by**: (string, optional) The field to sort results by. Valid values:
      - `created_on`: Sort by creation date.
      - `modified_on`: Sort by last modification date.
      - `name`: Sort alphabetically by name.
    - **sort_order**: (string, optional) The order to sort results. Valid values:
      - `ascending`: Sort in ascending order (A-Z, oldest first).
      - `descending`: Sort in descending order (Z-A, newest first).
      Default: descending when sort_by is specified.

    ## Response

    Returns a paginated list of domains with metadata:

    - **domains**: (array) List of domain resources for the current page.
      Each domain includes:
      - **id**: (string) The unique identifier for the domain.
      - **type**: (string) Always \"FeatureCollection\".
      - **name**: (string) The name of the domain.
      - **description**: (string) The description of the domain.
      - **created_on**: (datetime) When the domain was created.
      - **modified_on**: (datetime) When the domain was last modified.
      - **tags**: (array) The tags associated with the domain.
      - **crs**: (object) The coordinate reference system.
      - **features**: (array) The domain geometry features.
    - **current_page**: (integer) The current page number (zero-indexed).
    - **page_size**: (integer) The number of domains per page.
    - **total_items**: (integer) The total number of domains owned by the user.

    ## Pagination

    Use `page` and `size` parameters to navigate through large result sets:

    - First page: `?page=0&size=10`
    - Second page: `?page=1&size=10`
    - Calculate total pages: `ceil(total_items / page_size)`

    ## Sorting

    Combine `sort_by` and `sort_order` for custom ordering:

    - Newest first: `?sort_by=created_on&sort_order=descending`
    - Alphabetical: `?sort_by=name&sort_order=ascending`
    - Recently modified: `?sort_by=modified_on&sort_order=descending`

    ## Example Request

    ```http
    GET /v2/domains?page=0&size=10&sort_by=created_on&sort_order=descending
    ```

    ## Example Response

    ```json
    {
      \"domains\": [
        {
          \"id\": \"abc123...\",
          \"type\": \"FeatureCollection\",
          \"name\": \"My Domain\",
          \"description\": \"A test domain\",
          \"created_on\": \"2024-01-15T10:30:00\",
          \"modified_on\": \"2024-01-15T10:30:00\",
          \"tags\": [\"test\"],
          \"crs\": {\"type\": \"name\", \"properties\": {\"name\": \"EPSG:32611\"}},
          \"features\": [...]
        }
      ],
      \"current_page\": 0,
      \"page_size\": 10,
      \"total_items\": 42
    }
    ```

    ## Error Responses

    - **422 Unprocessable Entity**: Invalid query parameters.
      - Page must be a non-negative integer.
      - Size must be between 1 and 1000.
      - Invalid sort_by or sort_order values.

    Args:
        page (int | Unset): The page number to retrieve (zero-indexed). Default: 0.
        size (int | Unset): The number of domains to retrieve per page. Default: 100.
        sort_by (DomainSortField | None | Unset): The field to sort results by.
        sort_order (DomainSortOrder | None | Unset): The order to sort results (ascending or
            descending).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListDomainsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    ).parsed
