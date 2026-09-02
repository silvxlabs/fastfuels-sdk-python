from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_landfire_fbfm_40_request import CreateLandfireFbfm40Request
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateLandfireFbfm40Request,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/fbfm40/landfire".format(
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
    body: CreateLandfireFbfm40Request,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from LANDFIRE FBFM40

     # Create LANDFIRE FBFM40 Grid

    Creates a grid with FBFM40 fuel model codes from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fbfm`) with Scott-Burgan 40
    fuel model codes (e.g., GR1, TL3, SH5).

    To convert fuel model codes to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fbfm40` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2024\".
    - **season**: (optional) LANDFIRE Seasonal Fuels release: \"ES\" (early
      spring), \"SP\" (spring), \"SU\" (summer), or \"FA\" (fall).

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    The response `source` reports `year`: the calendar year the fuel data
    represents. For an annual grid this is the landscape vintage (same as
    `version`); for a seasonal grid it is the projected season year (e.g.
    `version` 2025 + `season` \"SP\" is spring 2026).

    Args:
        domain_id (str):
        body (CreateLandfireFbfm40Request): Request to create a grid from LANDFIRE FBFM40.

            Returns a single-band grid with categorical fuel model codes.
            To convert codes to fuel parameters, use /grids/lookup/fbfm40.

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
    body: CreateLandfireFbfm40Request,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from LANDFIRE FBFM40

     # Create LANDFIRE FBFM40 Grid

    Creates a grid with FBFM40 fuel model codes from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fbfm`) with Scott-Burgan 40
    fuel model codes (e.g., GR1, TL3, SH5).

    To convert fuel model codes to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fbfm40` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2024\".
    - **season**: (optional) LANDFIRE Seasonal Fuels release: \"ES\" (early
      spring), \"SP\" (spring), \"SU\" (summer), or \"FA\" (fall).

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    The response `source` reports `year`: the calendar year the fuel data
    represents. For an annual grid this is the landscape vintage (same as
    `version`); for a seasonal grid it is the projected season year (e.g.
    `version` 2025 + `season` \"SP\" is spring 2026).

    Args:
        domain_id (str):
        body (CreateLandfireFbfm40Request): Request to create a grid from LANDFIRE FBFM40.

            Returns a single-band grid with categorical fuel model codes.
            To convert codes to fuel parameters, use /grids/lookup/fbfm40.

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
    body: CreateLandfireFbfm40Request,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from LANDFIRE FBFM40

     # Create LANDFIRE FBFM40 Grid

    Creates a grid with FBFM40 fuel model codes from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fbfm`) with Scott-Burgan 40
    fuel model codes (e.g., GR1, TL3, SH5).

    To convert fuel model codes to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fbfm40` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2024\".
    - **season**: (optional) LANDFIRE Seasonal Fuels release: \"ES\" (early
      spring), \"SP\" (spring), \"SU\" (summer), or \"FA\" (fall).

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    The response `source` reports `year`: the calendar year the fuel data
    represents. For an annual grid this is the landscape vintage (same as
    `version`); for a seasonal grid it is the projected season year (e.g.
    `version` 2025 + `season` \"SP\" is spring 2026).

    Args:
        domain_id (str):
        body (CreateLandfireFbfm40Request): Request to create a grid from LANDFIRE FBFM40.

            Returns a single-band grid with categorical fuel model codes.
            To convert codes to fuel parameters, use /grids/lookup/fbfm40.

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
    body: CreateLandfireFbfm40Request,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from LANDFIRE FBFM40

     # Create LANDFIRE FBFM40 Grid

    Creates a grid with FBFM40 fuel model codes from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fbfm`) with Scott-Burgan 40
    fuel model codes (e.g., GR1, TL3, SH5).

    To convert fuel model codes to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fbfm40` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2024\".
    - **season**: (optional) LANDFIRE Seasonal Fuels release: \"ES\" (early
      spring), \"SP\" (spring), \"SU\" (summer), or \"FA\" (fall).

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    The response `source` reports `year`: the calendar year the fuel data
    represents. For an annual grid this is the landscape vintage (same as
    `version`); for a seasonal grid it is the projected season year (e.g.
    `version` 2025 + `season` \"SP\" is spring 2026).

    Args:
        domain_id (str):
        body (CreateLandfireFbfm40Request): Request to create a grid from LANDFIRE FBFM40.

            Returns a single-band grid with categorical fuel model codes.
            To convert codes to fuel parameters, use /grids/lookup/fbfm40.

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
