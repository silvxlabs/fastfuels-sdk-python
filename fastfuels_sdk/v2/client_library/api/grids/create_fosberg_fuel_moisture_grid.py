from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_fosberg_fuel_moisture_request import (
    CreateFosbergFuelMoistureRequest,
)
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateFosbergFuelMoistureRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/fuel-moisture/dead/fosberg".format(
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
    body: CreateFosbergFuelMoistureRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a Fosberg 1-hour dead fuel moisture grid

     # Create Fosberg 1-hour Dead Fuel Moisture Grid

    Creates a grid with a single continuous band, `fuel_moisture.dead.1hr`
    (percent), computed with the Fosberg & Deeming (1971) 1-hour dead fuel
    moisture model.

    The grid is derived from two completed source grids in the same domain:

    - **Topography** — supplies the `slope` and `aspect` bands (both degrees).
    - **Leaflux irradiance** — supplies `irradiance.surface.relative`, from
      which per-cell shading is derived as `1 - irradiance.surface.relative`.

    The remaining inputs are scalar weather/scenario parameters:
    `dry_bulb_temp` (°F), `relative_humidity` (%), `time` (local HHMM,
    0800-1959), `month`, and `elevation` (site position relative to the
    reference weather station).

    The output inherits the topography grid's domain, CRS, transform, and
    georeference. Keeping `time`/`month` consistent with the sun position that
    produced the irradiance grid is the caller's responsibility.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend
    computes the moisture surface and updates status to \"completed\".

    Args:
        domain_id (str):
        body (CreateFosbergFuelMoistureRequest): Request body for a Fosberg 1-hour dead fuel
            moisture content grid.

            Does not extend CreateSourceGridRequestBase: this is a grid -> grid
            derivation with no external raster and no alignment input. The output
            inherits the topography grid's domain, CRS, transform, and georeference.

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
    body: CreateFosbergFuelMoistureRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a Fosberg 1-hour dead fuel moisture grid

     # Create Fosberg 1-hour Dead Fuel Moisture Grid

    Creates a grid with a single continuous band, `fuel_moisture.dead.1hr`
    (percent), computed with the Fosberg & Deeming (1971) 1-hour dead fuel
    moisture model.

    The grid is derived from two completed source grids in the same domain:

    - **Topography** — supplies the `slope` and `aspect` bands (both degrees).
    - **Leaflux irradiance** — supplies `irradiance.surface.relative`, from
      which per-cell shading is derived as `1 - irradiance.surface.relative`.

    The remaining inputs are scalar weather/scenario parameters:
    `dry_bulb_temp` (°F), `relative_humidity` (%), `time` (local HHMM,
    0800-1959), `month`, and `elevation` (site position relative to the
    reference weather station).

    The output inherits the topography grid's domain, CRS, transform, and
    georeference. Keeping `time`/`month` consistent with the sun position that
    produced the irradiance grid is the caller's responsibility.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend
    computes the moisture surface and updates status to \"completed\".

    Args:
        domain_id (str):
        body (CreateFosbergFuelMoistureRequest): Request body for a Fosberg 1-hour dead fuel
            moisture content grid.

            Does not extend CreateSourceGridRequestBase: this is a grid -> grid
            derivation with no external raster and no alignment input. The output
            inherits the topography grid's domain, CRS, transform, and georeference.

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
    body: CreateFosbergFuelMoistureRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a Fosberg 1-hour dead fuel moisture grid

     # Create Fosberg 1-hour Dead Fuel Moisture Grid

    Creates a grid with a single continuous band, `fuel_moisture.dead.1hr`
    (percent), computed with the Fosberg & Deeming (1971) 1-hour dead fuel
    moisture model.

    The grid is derived from two completed source grids in the same domain:

    - **Topography** — supplies the `slope` and `aspect` bands (both degrees).
    - **Leaflux irradiance** — supplies `irradiance.surface.relative`, from
      which per-cell shading is derived as `1 - irradiance.surface.relative`.

    The remaining inputs are scalar weather/scenario parameters:
    `dry_bulb_temp` (°F), `relative_humidity` (%), `time` (local HHMM,
    0800-1959), `month`, and `elevation` (site position relative to the
    reference weather station).

    The output inherits the topography grid's domain, CRS, transform, and
    georeference. Keeping `time`/`month` consistent with the sun position that
    produced the irradiance grid is the caller's responsibility.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend
    computes the moisture surface and updates status to \"completed\".

    Args:
        domain_id (str):
        body (CreateFosbergFuelMoistureRequest): Request body for a Fosberg 1-hour dead fuel
            moisture content grid.

            Does not extend CreateSourceGridRequestBase: this is a grid -> grid
            derivation with no external raster and no alignment input. The output
            inherits the topography grid's domain, CRS, transform, and georeference.

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
    body: CreateFosbergFuelMoistureRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a Fosberg 1-hour dead fuel moisture grid

     # Create Fosberg 1-hour Dead Fuel Moisture Grid

    Creates a grid with a single continuous band, `fuel_moisture.dead.1hr`
    (percent), computed with the Fosberg & Deeming (1971) 1-hour dead fuel
    moisture model.

    The grid is derived from two completed source grids in the same domain:

    - **Topography** — supplies the `slope` and `aspect` bands (both degrees).
    - **Leaflux irradiance** — supplies `irradiance.surface.relative`, from
      which per-cell shading is derived as `1 - irradiance.surface.relative`.

    The remaining inputs are scalar weather/scenario parameters:
    `dry_bulb_temp` (°F), `relative_humidity` (%), `time` (local HHMM,
    0800-1959), `month`, and `elevation` (site position relative to the
    reference weather station).

    The output inherits the topography grid's domain, CRS, transform, and
    georeference. Keeping `time`/`month` consistent with the sun position that
    produced the irradiance grid is the caller's responsibility.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend
    computes the moisture surface and updates status to \"completed\".

    Args:
        domain_id (str):
        body (CreateFosbergFuelMoistureRequest): Request body for a Fosberg 1-hour dead fuel
            moisture content grid.

            Does not extend CreateSourceGridRequestBase: this is a grid -> grid
            derivation with no external raster and no alignment input. The output
            inherits the topography grid's domain, CRS, transform, and georeference.

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
