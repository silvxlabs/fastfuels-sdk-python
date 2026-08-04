from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_duet_request import CreateDuetRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateDuetRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/duet".format(
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
    body: CreateDuetRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a surface fuel grid with DUET

     # Create a DUET Surface Fuel Grid

    Runs DUET (Distribution of Understory using Elliptical Transport) over a 3D
    tree grid to produce 2D surface fuels. DUET drops leaf and needle litter
    from each tree's crown along wind-driven elliptical fall trajectories, then
    grows grass as a function of shade and litter cover — so litter accumulates
    under and downwind of crowns, and grass fills the gaps between them.

    ## What DUET does and does not give you

    DUET supplies the **spatial pattern** of surface fuels, keyed to real canopy
    structure. It does **not** supply physical magnitudes: raw DUET loadings are
    idiosyncratic to the model and should not be read as fuel loads or fed to a
    fire model as-is. Use `calibration` to impose magnitudes you trust — from
    field data, from the literature, or from an FBFM40 grid.

    ## Request Body

    - **source_grid_id**: (required) A completed 3D tree grid carrying the
      `bulk_density.foliage.live`, `spcd`, and `fuel_moisture.live` bands.
      Create one with `POST /grids/voxelize/inventory/tree`, requesting those
      three bands — `spcd` in particular is not voxelized by default.
    - **years_since_burn**: (required) Years of litter accumulation to simulate,
      1–100. DUET starts from the year of the last fire, with grass and litter
      consumed, so this is the stand's time since fire. It is the single most
      consequential parameter: a low value yields almost no litter because there
      has been no time for any to fall. It also drives runtime.
    - **wind_direction**: (optional) Degrees clockwise from north. Default 270.
    - **wind_variability**: (optional) Angular spread in degrees. Default 30.
    - **bands**: (optional) Output bands. Defaults to `fuel_load.grass` and
      `fuel_load.litter`. DUET separates fuels by type rather than size class,
      so bands are named for `grass`, `litter` (and its `litter.coniferous` /
      `litter.deciduous` parts), and `total`.
    - **calibration**: (optional) Per-parameter, per-fuel-type targets. Omit to
      store raw output.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Calibration

    Each of `fuel_load`, `fuel_depth`, and `fuel_moisture` is calibrated
    independently, and within each, per fuel type (`grass`, `coniferous`,
    `deciduous`, `litter`, or `all` — which is exclusive of the others). Methods:

    - `maxmin` — rescale to a target maximum and minimum. Best when fuel data
      are limited, or when their distribution does not resemble DUET's.
    - `meansd` — rescale to a target mean and standard deviation. Appropriate
      only when the targets come from a dataset large enough to approximate a
      normal distribution.
    - `constant` — assign a single value. Reasonable only when that is the only
      value available.

    Calibration rescales only cells that already carry fuel; cells DUET left
    empty stay empty. A consequence worth expecting: where cover is sparse, the
    domain-wide mean will sit well below a `meansd` target, because the target
    applies to the covered cells rather than to the domain.

    ## Response

    Returns the created Grid with status `\"pending\"` and `georeference: null`.
    Treevox runs DUET asynchronously and updates the grid to `\"completed\"` with
    a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateDuetRequest): Request body for creating a DUET surface fuel grid from a tree
            grid.

            Does not extend CreateGridRequestBase: like the 3D grids it derives from,
            DUET grids do not support modifications.

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
    body: CreateDuetRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a surface fuel grid with DUET

     # Create a DUET Surface Fuel Grid

    Runs DUET (Distribution of Understory using Elliptical Transport) over a 3D
    tree grid to produce 2D surface fuels. DUET drops leaf and needle litter
    from each tree's crown along wind-driven elliptical fall trajectories, then
    grows grass as a function of shade and litter cover — so litter accumulates
    under and downwind of crowns, and grass fills the gaps between them.

    ## What DUET does and does not give you

    DUET supplies the **spatial pattern** of surface fuels, keyed to real canopy
    structure. It does **not** supply physical magnitudes: raw DUET loadings are
    idiosyncratic to the model and should not be read as fuel loads or fed to a
    fire model as-is. Use `calibration` to impose magnitudes you trust — from
    field data, from the literature, or from an FBFM40 grid.

    ## Request Body

    - **source_grid_id**: (required) A completed 3D tree grid carrying the
      `bulk_density.foliage.live`, `spcd`, and `fuel_moisture.live` bands.
      Create one with `POST /grids/voxelize/inventory/tree`, requesting those
      three bands — `spcd` in particular is not voxelized by default.
    - **years_since_burn**: (required) Years of litter accumulation to simulate,
      1–100. DUET starts from the year of the last fire, with grass and litter
      consumed, so this is the stand's time since fire. It is the single most
      consequential parameter: a low value yields almost no litter because there
      has been no time for any to fall. It also drives runtime.
    - **wind_direction**: (optional) Degrees clockwise from north. Default 270.
    - **wind_variability**: (optional) Angular spread in degrees. Default 30.
    - **bands**: (optional) Output bands. Defaults to `fuel_load.grass` and
      `fuel_load.litter`. DUET separates fuels by type rather than size class,
      so bands are named for `grass`, `litter` (and its `litter.coniferous` /
      `litter.deciduous` parts), and `total`.
    - **calibration**: (optional) Per-parameter, per-fuel-type targets. Omit to
      store raw output.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Calibration

    Each of `fuel_load`, `fuel_depth`, and `fuel_moisture` is calibrated
    independently, and within each, per fuel type (`grass`, `coniferous`,
    `deciduous`, `litter`, or `all` — which is exclusive of the others). Methods:

    - `maxmin` — rescale to a target maximum and minimum. Best when fuel data
      are limited, or when their distribution does not resemble DUET's.
    - `meansd` — rescale to a target mean and standard deviation. Appropriate
      only when the targets come from a dataset large enough to approximate a
      normal distribution.
    - `constant` — assign a single value. Reasonable only when that is the only
      value available.

    Calibration rescales only cells that already carry fuel; cells DUET left
    empty stay empty. A consequence worth expecting: where cover is sparse, the
    domain-wide mean will sit well below a `meansd` target, because the target
    applies to the covered cells rather than to the domain.

    ## Response

    Returns the created Grid with status `\"pending\"` and `georeference: null`.
    Treevox runs DUET asynchronously and updates the grid to `\"completed\"` with
    a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateDuetRequest): Request body for creating a DUET surface fuel grid from a tree
            grid.

            Does not extend CreateGridRequestBase: like the 3D grids it derives from,
            DUET grids do not support modifications.

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
    body: CreateDuetRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a surface fuel grid with DUET

     # Create a DUET Surface Fuel Grid

    Runs DUET (Distribution of Understory using Elliptical Transport) over a 3D
    tree grid to produce 2D surface fuels. DUET drops leaf and needle litter
    from each tree's crown along wind-driven elliptical fall trajectories, then
    grows grass as a function of shade and litter cover — so litter accumulates
    under and downwind of crowns, and grass fills the gaps between them.

    ## What DUET does and does not give you

    DUET supplies the **spatial pattern** of surface fuels, keyed to real canopy
    structure. It does **not** supply physical magnitudes: raw DUET loadings are
    idiosyncratic to the model and should not be read as fuel loads or fed to a
    fire model as-is. Use `calibration` to impose magnitudes you trust — from
    field data, from the literature, or from an FBFM40 grid.

    ## Request Body

    - **source_grid_id**: (required) A completed 3D tree grid carrying the
      `bulk_density.foliage.live`, `spcd`, and `fuel_moisture.live` bands.
      Create one with `POST /grids/voxelize/inventory/tree`, requesting those
      three bands — `spcd` in particular is not voxelized by default.
    - **years_since_burn**: (required) Years of litter accumulation to simulate,
      1–100. DUET starts from the year of the last fire, with grass and litter
      consumed, so this is the stand's time since fire. It is the single most
      consequential parameter: a low value yields almost no litter because there
      has been no time for any to fall. It also drives runtime.
    - **wind_direction**: (optional) Degrees clockwise from north. Default 270.
    - **wind_variability**: (optional) Angular spread in degrees. Default 30.
    - **bands**: (optional) Output bands. Defaults to `fuel_load.grass` and
      `fuel_load.litter`. DUET separates fuels by type rather than size class,
      so bands are named for `grass`, `litter` (and its `litter.coniferous` /
      `litter.deciduous` parts), and `total`.
    - **calibration**: (optional) Per-parameter, per-fuel-type targets. Omit to
      store raw output.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Calibration

    Each of `fuel_load`, `fuel_depth`, and `fuel_moisture` is calibrated
    independently, and within each, per fuel type (`grass`, `coniferous`,
    `deciduous`, `litter`, or `all` — which is exclusive of the others). Methods:

    - `maxmin` — rescale to a target maximum and minimum. Best when fuel data
      are limited, or when their distribution does not resemble DUET's.
    - `meansd` — rescale to a target mean and standard deviation. Appropriate
      only when the targets come from a dataset large enough to approximate a
      normal distribution.
    - `constant` — assign a single value. Reasonable only when that is the only
      value available.

    Calibration rescales only cells that already carry fuel; cells DUET left
    empty stay empty. A consequence worth expecting: where cover is sparse, the
    domain-wide mean will sit well below a `meansd` target, because the target
    applies to the covered cells rather than to the domain.

    ## Response

    Returns the created Grid with status `\"pending\"` and `georeference: null`.
    Treevox runs DUET asynchronously and updates the grid to `\"completed\"` with
    a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateDuetRequest): Request body for creating a DUET surface fuel grid from a tree
            grid.

            Does not extend CreateGridRequestBase: like the 3D grids it derives from,
            DUET grids do not support modifications.

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
    body: CreateDuetRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a surface fuel grid with DUET

     # Create a DUET Surface Fuel Grid

    Runs DUET (Distribution of Understory using Elliptical Transport) over a 3D
    tree grid to produce 2D surface fuels. DUET drops leaf and needle litter
    from each tree's crown along wind-driven elliptical fall trajectories, then
    grows grass as a function of shade and litter cover — so litter accumulates
    under and downwind of crowns, and grass fills the gaps between them.

    ## What DUET does and does not give you

    DUET supplies the **spatial pattern** of surface fuels, keyed to real canopy
    structure. It does **not** supply physical magnitudes: raw DUET loadings are
    idiosyncratic to the model and should not be read as fuel loads or fed to a
    fire model as-is. Use `calibration` to impose magnitudes you trust — from
    field data, from the literature, or from an FBFM40 grid.

    ## Request Body

    - **source_grid_id**: (required) A completed 3D tree grid carrying the
      `bulk_density.foliage.live`, `spcd`, and `fuel_moisture.live` bands.
      Create one with `POST /grids/voxelize/inventory/tree`, requesting those
      three bands — `spcd` in particular is not voxelized by default.
    - **years_since_burn**: (required) Years of litter accumulation to simulate,
      1–100. DUET starts from the year of the last fire, with grass and litter
      consumed, so this is the stand's time since fire. It is the single most
      consequential parameter: a low value yields almost no litter because there
      has been no time for any to fall. It also drives runtime.
    - **wind_direction**: (optional) Degrees clockwise from north. Default 270.
    - **wind_variability**: (optional) Angular spread in degrees. Default 30.
    - **bands**: (optional) Output bands. Defaults to `fuel_load.grass` and
      `fuel_load.litter`. DUET separates fuels by type rather than size class,
      so bands are named for `grass`, `litter` (and its `litter.coniferous` /
      `litter.deciduous` parts), and `total`.
    - **calibration**: (optional) Per-parameter, per-fuel-type targets. Omit to
      store raw output.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Calibration

    Each of `fuel_load`, `fuel_depth`, and `fuel_moisture` is calibrated
    independently, and within each, per fuel type (`grass`, `coniferous`,
    `deciduous`, `litter`, or `all` — which is exclusive of the others). Methods:

    - `maxmin` — rescale to a target maximum and minimum. Best when fuel data
      are limited, or when their distribution does not resemble DUET's.
    - `meansd` — rescale to a target mean and standard deviation. Appropriate
      only when the targets come from a dataset large enough to approximate a
      normal distribution.
    - `constant` — assign a single value. Reasonable only when that is the only
      value available.

    Calibration rescales only cells that already carry fuel; cells DUET left
    empty stay empty. A consequence worth expecting: where cover is sparse, the
    domain-wide mean will sit well below a `meansd` target, because the target
    applies to the covered cells rather than to the domain.

    ## Response

    Returns the created Grid with status `\"pending\"` and `georeference: null`.
    Treevox runs DUET asynchronously and updates the grid to `\"completed\"` with
    a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateDuetRequest): Request body for creating a DUET surface fuel grid from a tree
            grid.

            Does not extend CreateGridRequestBase: like the 3D grids it derives from,
            DUET grids do not support modifications.

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
