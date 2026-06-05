from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_tree_map_request import CreateTreeMapRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateTreeMapRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/pim/treemap".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Grid | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = Grid.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Grid | HTTPValidationError]:
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
    body: CreateTreeMapRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a grid from TreeMap

     # Create TreeMap Grid

    Creates a grid with plot imputation data from TreeMap at 30m resolution.

    Each pixel contains a plot ID that maps to FIA tree records. Available bands:
    - **tm_id**: TreeMap raster pixel values (small integers, 1-70K)
    - **plt_cn**: FIA plot condition number (large integers, derived from tree table)

    By default only `tm_id` is included. Use the `bands` field to also request
    `plt_cn`.

    ## Request Body

    - **bands**: (optional) Which bands to include. Default: [\"tm_id\"].
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) TreeMap version. Default: \"2022\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateTreeMapRequest): Request to create a grid from TreeMap.

            Returns a grid with one or two categorical bands:
            - tm_id: TreeMap raster pixel values (always available)
            - plt_cn: FIA plot condition number (optional, derived from tree table)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: CreateTreeMapRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a grid from TreeMap

     # Create TreeMap Grid

    Creates a grid with plot imputation data from TreeMap at 30m resolution.

    Each pixel contains a plot ID that maps to FIA tree records. Available bands:
    - **tm_id**: TreeMap raster pixel values (small integers, 1-70K)
    - **plt_cn**: FIA plot condition number (large integers, derived from tree table)

    By default only `tm_id` is included. Use the `bands` field to also request
    `plt_cn`.

    ## Request Body

    - **bands**: (optional) Which bands to include. Default: [\"tm_id\"].
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) TreeMap version. Default: \"2022\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateTreeMapRequest): Request to create a grid from TreeMap.

            Returns a grid with one or two categorical bands:
            - tm_id: TreeMap raster pixel values (always available)
            - plt_cn: FIA plot condition number (optional, derived from tree table)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
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
    body: CreateTreeMapRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a grid from TreeMap

     # Create TreeMap Grid

    Creates a grid with plot imputation data from TreeMap at 30m resolution.

    Each pixel contains a plot ID that maps to FIA tree records. Available bands:
    - **tm_id**: TreeMap raster pixel values (small integers, 1-70K)
    - **plt_cn**: FIA plot condition number (large integers, derived from tree table)

    By default only `tm_id` is included. Use the `bands` field to also request
    `plt_cn`.

    ## Request Body

    - **bands**: (optional) Which bands to include. Default: [\"tm_id\"].
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) TreeMap version. Default: \"2022\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateTreeMapRequest): Request to create a grid from TreeMap.

            Returns a grid with one or two categorical bands:
            - tm_id: TreeMap raster pixel values (always available)
            - plt_cn: FIA plot condition number (optional, derived from tree table)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: CreateTreeMapRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a grid from TreeMap

     # Create TreeMap Grid

    Creates a grid with plot imputation data from TreeMap at 30m resolution.

    Each pixel contains a plot ID that maps to FIA tree records. Available bands:
    - **tm_id**: TreeMap raster pixel values (small integers, 1-70K)
    - **plt_cn**: FIA plot condition number (large integers, derived from tree table)

    By default only `tm_id` is included. Use the `bands` field to also request
    `plt_cn`.

    ## Request Body

    - **bands**: (optional) Which bands to include. Default: [\"tm_id\"].
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) TreeMap version. Default: \"2022\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateTreeMapRequest): Request to create a grid from TreeMap.

            Returns a grid with one or two categorical bands:
            - tm_id: TreeMap raster pixel values (always available)
            - plt_cn: FIA plot condition number (optional, derived from tree table)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
