from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_landfire_disturbance_request import (
    CreateLandfireDisturbanceRequest,
)
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateLandfireDisturbanceRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/disturbance/annual/landfire".format(
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
    body: CreateLandfireDisturbanceRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from LANDFIRE Limited Annual Disturbance

     # Create LANDFIRE Limited Annual Disturbance Grid

    Creates a grid with LANDFIRE Limited Annual Disturbance (LDist) codes,
    always fetched on demand from LANDFIRE Product Service at 30m resolution.

    The grid contains a single categorical band (`annual_disturbance`) with
    raw LDist codes.

    LDist is a single annual release with a \"first look\" at the disturbance and
    treatment events (fire, mechanical treatment, insects/disease), from that
    version's fiscal year, released the following January/February. See
    https://landfire.gov/disturbance/annualdisturbance for details.

    LANDFIRE's current-year fuels layers (FBFM40, FBFM13, FCCS) roll out
    region by region, with disturbance already incorporated wherever they've
    landed. LDist covers all of CONUS, so in regions where the rollout
    hasn't reached yet, you can pair LDist with the last complete  national
    fuels release to incorporate more recent disturbances. For example,
    if your region is still on LF2024 fuels because LF2025 hasn't reached it yet,
    pair LF2024 with LDist25 for a better estimate of current conditons.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2025\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireDisturbanceRequest): Request to create a grid from LANDFIRE Limited
            Annual Disturbance.

            Returns a single-band grid with categorical disturbance codes. Always
            fetched on demand from LANDFIRE Product Service.

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
    body: CreateLandfireDisturbanceRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from LANDFIRE Limited Annual Disturbance

     # Create LANDFIRE Limited Annual Disturbance Grid

    Creates a grid with LANDFIRE Limited Annual Disturbance (LDist) codes,
    always fetched on demand from LANDFIRE Product Service at 30m resolution.

    The grid contains a single categorical band (`annual_disturbance`) with
    raw LDist codes.

    LDist is a single annual release with a \"first look\" at the disturbance and
    treatment events (fire, mechanical treatment, insects/disease), from that
    version's fiscal year, released the following January/February. See
    https://landfire.gov/disturbance/annualdisturbance for details.

    LANDFIRE's current-year fuels layers (FBFM40, FBFM13, FCCS) roll out
    region by region, with disturbance already incorporated wherever they've
    landed. LDist covers all of CONUS, so in regions where the rollout
    hasn't reached yet, you can pair LDist with the last complete  national
    fuels release to incorporate more recent disturbances. For example,
    if your region is still on LF2024 fuels because LF2025 hasn't reached it yet,
    pair LF2024 with LDist25 for a better estimate of current conditons.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2025\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireDisturbanceRequest): Request to create a grid from LANDFIRE Limited
            Annual Disturbance.

            Returns a single-band grid with categorical disturbance codes. Always
            fetched on demand from LANDFIRE Product Service.

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
    body: CreateLandfireDisturbanceRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from LANDFIRE Limited Annual Disturbance

     # Create LANDFIRE Limited Annual Disturbance Grid

    Creates a grid with LANDFIRE Limited Annual Disturbance (LDist) codes,
    always fetched on demand from LANDFIRE Product Service at 30m resolution.

    The grid contains a single categorical band (`annual_disturbance`) with
    raw LDist codes.

    LDist is a single annual release with a \"first look\" at the disturbance and
    treatment events (fire, mechanical treatment, insects/disease), from that
    version's fiscal year, released the following January/February. See
    https://landfire.gov/disturbance/annualdisturbance for details.

    LANDFIRE's current-year fuels layers (FBFM40, FBFM13, FCCS) roll out
    region by region, with disturbance already incorporated wherever they've
    landed. LDist covers all of CONUS, so in regions where the rollout
    hasn't reached yet, you can pair LDist with the last complete  national
    fuels release to incorporate more recent disturbances. For example,
    if your region is still on LF2024 fuels because LF2025 hasn't reached it yet,
    pair LF2024 with LDist25 for a better estimate of current conditons.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2025\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireDisturbanceRequest): Request to create a grid from LANDFIRE Limited
            Annual Disturbance.

            Returns a single-band grid with categorical disturbance codes. Always
            fetched on demand from LANDFIRE Product Service.

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
    body: CreateLandfireDisturbanceRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from LANDFIRE Limited Annual Disturbance

     # Create LANDFIRE Limited Annual Disturbance Grid

    Creates a grid with LANDFIRE Limited Annual Disturbance (LDist) codes,
    always fetched on demand from LANDFIRE Product Service at 30m resolution.

    The grid contains a single categorical band (`annual_disturbance`) with
    raw LDist codes.

    LDist is a single annual release with a \"first look\" at the disturbance and
    treatment events (fire, mechanical treatment, insects/disease), from that
    version's fiscal year, released the following January/February. See
    https://landfire.gov/disturbance/annualdisturbance for details.

    LANDFIRE's current-year fuels layers (FBFM40, FBFM13, FCCS) roll out
    region by region, with disturbance already incorporated wherever they've
    landed. LDist covers all of CONUS, so in regions where the rollout
    hasn't reached yet, you can pair LDist with the last complete  national
    fuels release to incorporate more recent disturbances. For example,
    if your region is still on LF2024 fuels because LF2025 hasn't reached it yet,
    pair LF2024 with LDist25 for a better estimate of current conditons.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2025\".

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireDisturbanceRequest): Request to create a grid from LANDFIRE Limited
            Annual Disturbance.

            Returns a single-band grid with categorical disturbance codes. Always
            fetched on demand from LANDFIRE Product Service.

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
