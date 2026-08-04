from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_fbfm_40_lookup_request import CreateFbfm40LookupRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateFbfm40LookupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/lookup/fbfm40".format(
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
    body: CreateFbfm40LookupRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid by looking up FBFM40 fuel parameters

     # Create FBFM40 Lookup Grid

    Converts FBFM40 fuel model codes to fuel parameters using Scott-Burgan 40
    lookup tables.

    Takes a source grid containing categorical FBFM codes (from
    `/grids/fbfm40/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM40 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_herb`, `fuel_load.live_woody` - Live fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_herb`, `savr.live_woody` - Live fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM codes. Defaults to `\"fbfm\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM40 Codes

    The source grid must contain only valid Scott-Burgan 40 fuel model codes.
    The 46 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **GR** (grass): 101–109
    - **GS** (grass-shrub): 121–124
    - **SH** (shrub): 141–149
    - **TU** (timber-understory): 161–165
    - **TL** (timber litter): 181–189
    - **SB** (slash-blowdown): 201–204

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
    - Non-burnable codes (NB1–NB9) produce zero values for all bands.
    - All output values are in metric units (converted from SB40 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm40LookupRequest): Request to create a grid by looking up FBFM40 fuel
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
    body: CreateFbfm40LookupRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid by looking up FBFM40 fuel parameters

     # Create FBFM40 Lookup Grid

    Converts FBFM40 fuel model codes to fuel parameters using Scott-Burgan 40
    lookup tables.

    Takes a source grid containing categorical FBFM codes (from
    `/grids/fbfm40/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM40 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_herb`, `fuel_load.live_woody` - Live fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_herb`, `savr.live_woody` - Live fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM codes. Defaults to `\"fbfm\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM40 Codes

    The source grid must contain only valid Scott-Burgan 40 fuel model codes.
    The 46 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **GR** (grass): 101–109
    - **GS** (grass-shrub): 121–124
    - **SH** (shrub): 141–149
    - **TU** (timber-understory): 161–165
    - **TL** (timber litter): 181–189
    - **SB** (slash-blowdown): 201–204

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
    - Non-burnable codes (NB1–NB9) produce zero values for all bands.
    - All output values are in metric units (converted from SB40 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm40LookupRequest): Request to create a grid by looking up FBFM40 fuel
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
    body: CreateFbfm40LookupRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid by looking up FBFM40 fuel parameters

     # Create FBFM40 Lookup Grid

    Converts FBFM40 fuel model codes to fuel parameters using Scott-Burgan 40
    lookup tables.

    Takes a source grid containing categorical FBFM codes (from
    `/grids/fbfm40/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM40 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_herb`, `fuel_load.live_woody` - Live fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_herb`, `savr.live_woody` - Live fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM codes. Defaults to `\"fbfm\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM40 Codes

    The source grid must contain only valid Scott-Burgan 40 fuel model codes.
    The 46 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **GR** (grass): 101–109
    - **GS** (grass-shrub): 121–124
    - **SH** (shrub): 141–149
    - **TU** (timber-understory): 161–165
    - **TL** (timber litter): 181–189
    - **SB** (slash-blowdown): 201–204

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
    - Non-burnable codes (NB1–NB9) produce zero values for all bands.
    - All output values are in metric units (converted from SB40 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm40LookupRequest): Request to create a grid by looking up FBFM40 fuel
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
    body: CreateFbfm40LookupRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid by looking up FBFM40 fuel parameters

     # Create FBFM40 Lookup Grid

    Converts FBFM40 fuel model codes to fuel parameters using Scott-Burgan 40
    lookup tables.

    Takes a source grid containing categorical FBFM codes (from
    `/grids/fbfm40/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FBFM40 codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.live_herb`, `fuel_load.live_woody` - Live fuel loads (kg/m**2)
      - `savr.1hr`, `savr.10hr`, `savr.100hr` - Dead fuel SAV ratios (1/m)
      - `savr.live_herb`, `savr.live_woody` - Live fuel SAV ratios (1/m)
      - `fuel_depth` - Fuel bed depth (m)
    - **source_band**: (optional) Band in source grid containing FBFM codes. Defaults to `\"fbfm\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Valid FBFM40 Codes

    The source grid must contain only valid Scott-Burgan 40 fuel model codes.
    The 46 valid codes are:

    - **NB** (non-burnable): 91, 92, 93, 98, 99
    - **GR** (grass): 101–109
    - **GS** (grass-shrub): 121–124
    - **SH** (shrub): 141–149
    - **TU** (timber-understory): 161–165
    - **TL** (timber litter): 181–189
    - **SB** (slash-blowdown): 201–204

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
    - Non-burnable codes (NB1–NB9) produce zero values for all bands.
    - All output values are in metric units (converted from SB40 imperial values).

    Args:
        domain_id (str):
        body (CreateFbfm40LookupRequest): Request to create a grid by looking up FBFM40 fuel
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
