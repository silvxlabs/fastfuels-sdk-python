from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_fccs_lookup_request import CreateFccsLookupRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateFccsLookupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/lookup/fccs".format(
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
    body: CreateFccsLookupRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid by looking up FCCS fuel parameters

     # Create FCCS Lookup Grid

    Converts FCCS fuelbed codes to fuel parameters using the FOFEM FCCS
    fuelbed lookup table (see the
    [FOFEM/SpatialFOFEM FCCS lookup table](https://www.landfire.gov/sites/default/files/CSV/SpatialFOFEM
    _FCCS_Formatted_TS_06-27-24.csv),
    the USDA Forest Service data source this endpoint converts).

    Takes a source grid containing categorical FCCS codes (from
    `/grids/fccs/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FCCS codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.litter`, `fuel_load.duff` - Ground fuel loads (kg/m**2)
      - `duff_depth` - Duff layer depth (m)
      - `fuel_load.live_shrub`, `fuel_load.live_herb` - Live surface fuel loads (kg/m**2)
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.1000hr_sound`, `fuel_load.1000hr_rotten` - Dead fuel loads, >3in. diameter (kg/m**2)
      - `fuel_load.live_foliage`, `fuel_load.live_branch` - Live crown fuel loads (kg/m**2)
    - **source_band**: (optional) Band in source grid containing FCCS codes. Defaults to `\"fccs\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Band Coverage

    These 12 bands are a starting subset of what FOFEM provides, not the
    full table. `fuel_load.1000hr_sound` and `fuel_load.1000hr_rotten`
    are each calculated by summing three FOFEM size-class columns
    (3-9 in., 9-20 in., 20+ in.) rather than mapping to a single source
    column. FOFEM also provides finer sound/rotten size-class
    breakdowns, a cover-group code, and emission factors that aren't
    exposed as bands here — additional bands can be added on request.

    ## Valid FCCS Codes

    Each `FCCS` code is a synthetic key: `base * 10_000 + suffix`, where
    `base` is the `FCCSID` fuelbed number and the 3-digit `suffix`
    encodes an FCCS Potential rating (Fire Behavior / Crown Fire /
    Available Fuel Potential, each a 0-9 digit) per the [Fuel Characteristic
    Classification System Version 3.0: Technical Documentation (PNW-
    GTR-887)](https://www.fs.usda.gov/pnw/pubs/pnw_gtr887.pdf).

    The source grid must contain FCCS codes whose base fuelbed number matches
    a recognized `FCCSID`. A code with a valid base but no matching row in the
    FOFEM lookup table is not an error. It's a fuelbed/fire-potential combination
    the table doesn't cover, so its output is `NaN` for every band, and a
    progress warning lists these codes.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - All output values are in metric units (converted from FOFEM imperial
      values).

    Args:
        domain_id (str):
        body (CreateFccsLookupRequest): Request to create a grid by looking up FCCS fuel
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
    body: CreateFccsLookupRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid by looking up FCCS fuel parameters

     # Create FCCS Lookup Grid

    Converts FCCS fuelbed codes to fuel parameters using the FOFEM FCCS
    fuelbed lookup table (see the
    [FOFEM/SpatialFOFEM FCCS lookup table](https://www.landfire.gov/sites/default/files/CSV/SpatialFOFEM
    _FCCS_Formatted_TS_06-27-24.csv),
    the USDA Forest Service data source this endpoint converts).

    Takes a source grid containing categorical FCCS codes (from
    `/grids/fccs/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FCCS codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.litter`, `fuel_load.duff` - Ground fuel loads (kg/m**2)
      - `duff_depth` - Duff layer depth (m)
      - `fuel_load.live_shrub`, `fuel_load.live_herb` - Live surface fuel loads (kg/m**2)
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.1000hr_sound`, `fuel_load.1000hr_rotten` - Dead fuel loads, >3in. diameter (kg/m**2)
      - `fuel_load.live_foliage`, `fuel_load.live_branch` - Live crown fuel loads (kg/m**2)
    - **source_band**: (optional) Band in source grid containing FCCS codes. Defaults to `\"fccs\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Band Coverage

    These 12 bands are a starting subset of what FOFEM provides, not the
    full table. `fuel_load.1000hr_sound` and `fuel_load.1000hr_rotten`
    are each calculated by summing three FOFEM size-class columns
    (3-9 in., 9-20 in., 20+ in.) rather than mapping to a single source
    column. FOFEM also provides finer sound/rotten size-class
    breakdowns, a cover-group code, and emission factors that aren't
    exposed as bands here — additional bands can be added on request.

    ## Valid FCCS Codes

    Each `FCCS` code is a synthetic key: `base * 10_000 + suffix`, where
    `base` is the `FCCSID` fuelbed number and the 3-digit `suffix`
    encodes an FCCS Potential rating (Fire Behavior / Crown Fire /
    Available Fuel Potential, each a 0-9 digit) per the [Fuel Characteristic
    Classification System Version 3.0: Technical Documentation (PNW-
    GTR-887)](https://www.fs.usda.gov/pnw/pubs/pnw_gtr887.pdf).

    The source grid must contain FCCS codes whose base fuelbed number matches
    a recognized `FCCSID`. A code with a valid base but no matching row in the
    FOFEM lookup table is not an error. It's a fuelbed/fire-potential combination
    the table doesn't cover, so its output is `NaN` for every band, and a
    progress warning lists these codes.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - All output values are in metric units (converted from FOFEM imperial
      values).

    Args:
        domain_id (str):
        body (CreateFccsLookupRequest): Request to create a grid by looking up FCCS fuel
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
    body: CreateFccsLookupRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid by looking up FCCS fuel parameters

     # Create FCCS Lookup Grid

    Converts FCCS fuelbed codes to fuel parameters using the FOFEM FCCS
    fuelbed lookup table (see the
    [FOFEM/SpatialFOFEM FCCS lookup table](https://www.landfire.gov/sites/default/files/CSV/SpatialFOFEM
    _FCCS_Formatted_TS_06-27-24.csv),
    the USDA Forest Service data source this endpoint converts).

    Takes a source grid containing categorical FCCS codes (from
    `/grids/fccs/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FCCS codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.litter`, `fuel_load.duff` - Ground fuel loads (kg/m**2)
      - `duff_depth` - Duff layer depth (m)
      - `fuel_load.live_shrub`, `fuel_load.live_herb` - Live surface fuel loads (kg/m**2)
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.1000hr_sound`, `fuel_load.1000hr_rotten` - Dead fuel loads, >3in. diameter (kg/m**2)
      - `fuel_load.live_foliage`, `fuel_load.live_branch` - Live crown fuel loads (kg/m**2)
    - **source_band**: (optional) Band in source grid containing FCCS codes. Defaults to `\"fccs\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Band Coverage

    These 12 bands are a starting subset of what FOFEM provides, not the
    full table. `fuel_load.1000hr_sound` and `fuel_load.1000hr_rotten`
    are each calculated by summing three FOFEM size-class columns
    (3-9 in., 9-20 in., 20+ in.) rather than mapping to a single source
    column. FOFEM also provides finer sound/rotten size-class
    breakdowns, a cover-group code, and emission factors that aren't
    exposed as bands here — additional bands can be added on request.

    ## Valid FCCS Codes

    Each `FCCS` code is a synthetic key: `base * 10_000 + suffix`, where
    `base` is the `FCCSID` fuelbed number and the 3-digit `suffix`
    encodes an FCCS Potential rating (Fire Behavior / Crown Fire /
    Available Fuel Potential, each a 0-9 digit) per the [Fuel Characteristic
    Classification System Version 3.0: Technical Documentation (PNW-
    GTR-887)](https://www.fs.usda.gov/pnw/pubs/pnw_gtr887.pdf).

    The source grid must contain FCCS codes whose base fuelbed number matches
    a recognized `FCCSID`. A code with a valid base but no matching row in the
    FOFEM lookup table is not an error. It's a fuelbed/fire-potential combination
    the table doesn't cover, so its output is `NaN` for every band, and a
    progress warning lists these codes.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - All output values are in metric units (converted from FOFEM imperial
      values).

    Args:
        domain_id (str):
        body (CreateFccsLookupRequest): Request to create a grid by looking up FCCS fuel
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
    body: CreateFccsLookupRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid by looking up FCCS fuel parameters

     # Create FCCS Lookup Grid

    Converts FCCS fuelbed codes to fuel parameters using the FOFEM FCCS
    fuelbed lookup table (see the
    [FOFEM/SpatialFOFEM FCCS lookup table](https://www.landfire.gov/sites/default/files/CSV/SpatialFOFEM
    _FCCS_Formatted_TS_06-27-24.csv),
    the USDA Forest Service data source this endpoint converts).

    Takes a source grid containing categorical FCCS codes (from
    `/grids/fccs/landfire`) and produces a new grid with the requested
    continuous fuel parameters.

    ## Request Body

    - **source_grid_id**: (required) Grid containing FCCS codes.
    - **bands**: (required) Bands to look up. Valid values:
      - `fuel_load.litter`, `fuel_load.duff` - Ground fuel loads (kg/m**2)
      - `duff_depth` - Duff layer depth (m)
      - `fuel_load.live_shrub`, `fuel_load.live_herb` - Live surface fuel loads (kg/m**2)
      - `fuel_load.1hr`, `fuel_load.10hr`, `fuel_load.100hr` - Dead fuel loads (kg/m**2)
      - `fuel_load.1000hr_sound`, `fuel_load.1000hr_rotten` - Dead fuel loads, >3in. diameter (kg/m**2)
      - `fuel_load.live_foliage`, `fuel_load.live_branch` - Live crown fuel loads (kg/m**2)
    - **source_band**: (optional) Band in source grid containing FCCS codes. Defaults to `\"fccs\"`.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Band Coverage

    These 12 bands are a starting subset of what FOFEM provides, not the
    full table. `fuel_load.1000hr_sound` and `fuel_load.1000hr_rotten`
    are each calculated by summing three FOFEM size-class columns
    (3-9 in., 9-20 in., 20+ in.) rather than mapping to a single source
    column. FOFEM also provides finer sound/rotten size-class
    breakdowns, a cover-group code, and emission factors that aren't
    exposed as bands here — additional bands can be added on request.

    ## Valid FCCS Codes

    Each `FCCS` code is a synthetic key: `base * 10_000 + suffix`, where
    `base` is the `FCCSID` fuelbed number and the 3-digit `suffix`
    encodes an FCCS Potential rating (Fire Behavior / Crown Fire /
    Available Fuel Potential, each a 0-9 digit) per the [Fuel Characteristic
    Classification System Version 3.0: Technical Documentation (PNW-
    GTR-887)](https://www.fs.usda.gov/pnw/pubs/pnw_gtr887.pdf).

    The source grid must contain FCCS codes whose base fuelbed number matches
    a recognized `FCCSID`. A code with a valid base but no matching row in the
    FOFEM lookup table is not an error. It's a fuelbed/fire-potential combination
    the table doesn't cover, so its output is `NaN` for every band, and a
    progress warning lists these codes.

    ## Response

    Returns the created Grid with status \"pending\". The backend applies the
    lookup transformation and updates status to \"completed\" when ready.

    ## Notes

    - Domain is propagated from the source grid (derived grids carry the
      same domain reference as their source).
    - The output grid inherits georeference from the source grid.
    - All output values are in metric units (converted from FOFEM imperial
      values).

    Args:
        domain_id (str):
        body (CreateFccsLookupRequest): Request to create a grid by looking up FCCS fuel
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
