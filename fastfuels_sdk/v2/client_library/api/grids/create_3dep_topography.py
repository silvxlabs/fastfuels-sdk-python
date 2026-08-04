from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_three_dep_topography_request import (
    CreateThreeDepTopographyRequest,
)
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateThreeDepTopographyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/topography/3dep".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = Grid.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = QuotaExceededDetail.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
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
    body: CreateThreeDepTopographyRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from 3DEP topographic data

     # Create 3DEP Topography Grid

    Creates a grid with topographic data from USGS 3DEP at selectable resolution.

    Available resolutions:
    - **1m**: Seamless 1-meter (S1M). Coverage varies by region; areas without
      S1M data will return a COVERAGE_ERROR.
    - **10m**: 1/3 arc-second seamless (default)
    - **30m**: 1 arc-second seamless

    Available bands:
    - **elevation**: meters above sea level (default)
    - **slope**: degrees (0-90)
    - **aspect**: degrees clockwise from north (0-360)

    Slope and aspect are computed locally from the DEM using Horn's method.

    ## Request Body

    - **source_resolution**: (optional) Source product family in meters:
      1, 10, or 30. Default: 10. To change the *output* cell size, set
      ``alignment.resolution``.
    - **bands**: (optional) Which bands to include. Default: elevation only.
    - **alignment**: (optional) Output alignment target. See alignment docs.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateThreeDepTopographyRequest): Request to create a grid from 3DEP topographic
            data.

            Returns a grid with one or more continuous bands: elevation (m),
            slope (degrees), and/or aspect (degrees).

            `source_resolution` selects the 3DEP product family (1m, 10m, or 30m).
            To change the *output* cell size, set ``alignment.resolution`` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateThreeDepTopographyRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from 3DEP topographic data

     # Create 3DEP Topography Grid

    Creates a grid with topographic data from USGS 3DEP at selectable resolution.

    Available resolutions:
    - **1m**: Seamless 1-meter (S1M). Coverage varies by region; areas without
      S1M data will return a COVERAGE_ERROR.
    - **10m**: 1/3 arc-second seamless (default)
    - **30m**: 1 arc-second seamless

    Available bands:
    - **elevation**: meters above sea level (default)
    - **slope**: degrees (0-90)
    - **aspect**: degrees clockwise from north (0-360)

    Slope and aspect are computed locally from the DEM using Horn's method.

    ## Request Body

    - **source_resolution**: (optional) Source product family in meters:
      1, 10, or 30. Default: 10. To change the *output* cell size, set
      ``alignment.resolution``.
    - **bands**: (optional) Which bands to include. Default: elevation only.
    - **alignment**: (optional) Output alignment target. See alignment docs.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateThreeDepTopographyRequest): Request to create a grid from 3DEP topographic
            data.

            Returns a grid with one or more continuous bands: elevation (m),
            slope (degrees), and/or aspect (degrees).

            `source_resolution` selects the 3DEP product family (1m, 10m, or 30m).
            To change the *output* cell size, set ``alignment.resolution`` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError | QuotaExceededDetail
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
    body: CreateThreeDepTopographyRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from 3DEP topographic data

     # Create 3DEP Topography Grid

    Creates a grid with topographic data from USGS 3DEP at selectable resolution.

    Available resolutions:
    - **1m**: Seamless 1-meter (S1M). Coverage varies by region; areas without
      S1M data will return a COVERAGE_ERROR.
    - **10m**: 1/3 arc-second seamless (default)
    - **30m**: 1 arc-second seamless

    Available bands:
    - **elevation**: meters above sea level (default)
    - **slope**: degrees (0-90)
    - **aspect**: degrees clockwise from north (0-360)

    Slope and aspect are computed locally from the DEM using Horn's method.

    ## Request Body

    - **source_resolution**: (optional) Source product family in meters:
      1, 10, or 30. Default: 10. To change the *output* cell size, set
      ``alignment.resolution``.
    - **bands**: (optional) Which bands to include. Default: elevation only.
    - **alignment**: (optional) Output alignment target. See alignment docs.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateThreeDepTopographyRequest): Request to create a grid from 3DEP topographic
            data.

            Returns a grid with one or more continuous bands: elevation (m),
            slope (degrees), and/or aspect (degrees).

            `source_resolution` selects the 3DEP product family (1m, 10m, or 30m).
            To change the *output* cell size, set ``alignment.resolution`` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateThreeDepTopographyRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from 3DEP topographic data

     # Create 3DEP Topography Grid

    Creates a grid with topographic data from USGS 3DEP at selectable resolution.

    Available resolutions:
    - **1m**: Seamless 1-meter (S1M). Coverage varies by region; areas without
      S1M data will return a COVERAGE_ERROR.
    - **10m**: 1/3 arc-second seamless (default)
    - **30m**: 1 arc-second seamless

    Available bands:
    - **elevation**: meters above sea level (default)
    - **slope**: degrees (0-90)
    - **aspect**: degrees clockwise from north (0-360)

    Slope and aspect are computed locally from the DEM using Horn's method.

    ## Request Body

    - **source_resolution**: (optional) Source product family in meters:
      1, 10, or 30. Default: 10. To change the *output* cell size, set
      ``alignment.resolution``.
    - **bands**: (optional) Which bands to include. Default: elevation only.
    - **alignment**: (optional) Output alignment target. See alignment docs.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateThreeDepTopographyRequest): Request to create a grid from 3DEP topographic
            data.

            Returns a grid with one or more continuous bands: elevation (m),
            slope (degrees), and/or aspect (degrees).

            `source_resolution` selects the 3DEP product family (1m, 10m, or 30m).
            To change the *output* cell size, set ``alignment.resolution`` instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
