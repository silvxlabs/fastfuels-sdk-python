from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_fbfm_13_lookup_request import CreateFbfm13LookupRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateFbfm13LookupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/lookup/fbfm13".format(
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
    body: CreateFbfm13LookupRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid by looking up FBFM13 fuel parameters

     # Create FBFM13 Lookup Grid

    Converts Anderson 13 fuel model codes to fuel parameters using the
    Anderson 13 lookup table.

    Takes a source grid containing categorical FBFM13 codes (from
    `/grids/fbfm13/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM13 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_foliage` - Live foliage fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_foliage` - Live foliage fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM13 codes. Defaults to `\"fbfm13\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM13 Codes

    The source grid must contain only valid Anderson 13 fuel model codes.
    The 18 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **Anderson 13 models**: 1–13

    If any cell in the source grid contains a code not in this set (including 0
    or nodata), the job will fail with an `INVALID_FBFM_CODES` error listing
    the invalid codes found.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - Non-burnable codes (91-99) produce zero values for all bands.
    - Fuel parameter values are from Anderson, Hal E. 1982. *Aids to
      determining fuel models for estimating fire behavior.* USDA Forest
      Service General Technical Report INT-122.
    - All output values are in metric units (converted from Anderson 13 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm13LookupRequest): Request to create a grid by looking up FBFM13 fuel
            parameters.

            Unlike entry-point grid creation requests, domain_id is not required
            because derived grids carry the same domain reference as their source.

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
    body: CreateFbfm13LookupRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid by looking up FBFM13 fuel parameters

     # Create FBFM13 Lookup Grid

    Converts Anderson 13 fuel model codes to fuel parameters using the
    Anderson 13 lookup table.

    Takes a source grid containing categorical FBFM13 codes (from
    `/grids/fbfm13/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM13 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_foliage` - Live foliage fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_foliage` - Live foliage fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM13 codes. Defaults to `\"fbfm13\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM13 Codes

    The source grid must contain only valid Anderson 13 fuel model codes.
    The 18 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **Anderson 13 models**: 1–13

    If any cell in the source grid contains a code not in this set (including 0
    or nodata), the job will fail with an `INVALID_FBFM_CODES` error listing
    the invalid codes found.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - Non-burnable codes (91-99) produce zero values for all bands.
    - Fuel parameter values are from Anderson, Hal E. 1982. *Aids to
      determining fuel models for estimating fire behavior.* USDA Forest
      Service General Technical Report INT-122.
    - All output values are in metric units (converted from Anderson 13 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm13LookupRequest): Request to create a grid by looking up FBFM13 fuel
            parameters.

            Unlike entry-point grid creation requests, domain_id is not required
            because derived grids carry the same domain reference as their source.

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
    body: CreateFbfm13LookupRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid by looking up FBFM13 fuel parameters

     # Create FBFM13 Lookup Grid

    Converts Anderson 13 fuel model codes to fuel parameters using the
    Anderson 13 lookup table.

    Takes a source grid containing categorical FBFM13 codes (from
    `/grids/fbfm13/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM13 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_foliage` - Live foliage fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_foliage` - Live foliage fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM13 codes. Defaults to `\"fbfm13\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM13 Codes

    The source grid must contain only valid Anderson 13 fuel model codes.
    The 18 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **Anderson 13 models**: 1–13

    If any cell in the source grid contains a code not in this set (including 0
    or nodata), the job will fail with an `INVALID_FBFM_CODES` error listing
    the invalid codes found.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - Non-burnable codes (91-99) produce zero values for all bands.
    - Fuel parameter values are from Anderson, Hal E. 1982. *Aids to
      determining fuel models for estimating fire behavior.* USDA Forest
      Service General Technical Report INT-122.
    - All output values are in metric units (converted from Anderson 13 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm13LookupRequest): Request to create a grid by looking up FBFM13 fuel
            parameters.

            Unlike entry-point grid creation requests, domain_id is not required
            because derived grids carry the same domain reference as their source.

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
    body: CreateFbfm13LookupRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid by looking up FBFM13 fuel parameters

     # Create FBFM13 Lookup Grid

    Converts Anderson 13 fuel model codes to fuel parameters using the
    Anderson 13 lookup table.

    Takes a source grid containing categorical FBFM13 codes (from
    `/grids/fbfm13/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM13 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_foliage` - Live foliage fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_foliage` - Live foliage fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM13 codes. Defaults to `\"fbfm13\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM13 Codes

    The source grid must contain only valid Anderson 13 fuel model codes.
    The 18 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **Anderson 13 models**: 1–13

    If any cell in the source grid contains a code not in this set (including 0
    or nodata), the job will fail with an `INVALID_FBFM_CODES` error listing
    the invalid codes found.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - Non-burnable codes (91-99) produce zero values for all bands.
    - Fuel parameter values are from Anderson, Hal E. 1982. *Aids to
      determining fuel models for estimating fire behavior.* USDA Forest
      Service General Technical Report INT-122.
    - All output values are in metric units (converted from Anderson 13 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm13LookupRequest): Request to create a grid by looking up FBFM13 fuel
            parameters.

            Unlike entry-point grid creation requests, domain_id is not required
            because derived grids carry the same domain reference as their source.

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
