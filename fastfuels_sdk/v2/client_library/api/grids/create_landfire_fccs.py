from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_landfire_fccs_request import CreateLandfireFccsRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateLandfireFccsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/fccs/landfire".format(
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
    body: CreateLandfireFccsRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from LANDFIRE FCCS

     # Create LANDFIRE FCCS Grid

    Creates a grid with FCCS fuelbed IDs from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fccs`) with fuel
    classification system fuelbed IDs (e.g., 26, 598, 34721).

    To convert fuelbed IDs to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fccs` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2023\".
    - **remove_bare_ground**: (optional) Remove bare ground cells (fuelbed ID 0),
                              replaced by neighboring majority. Default: False.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireFccsRequest): Request to create a grid from LANDFIRE FCCS.

            Returns a single-band grid with categorical fuelbed IDs.
            To convert IDs to fuel parameters, use /grids/lookup/fccs.

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
    body: CreateLandfireFccsRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from LANDFIRE FCCS

     # Create LANDFIRE FCCS Grid

    Creates a grid with FCCS fuelbed IDs from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fccs`) with fuel
    classification system fuelbed IDs (e.g., 26, 598, 34721).

    To convert fuelbed IDs to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fccs` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2023\".
    - **remove_bare_ground**: (optional) Remove bare ground cells (fuelbed ID 0),
                              replaced by neighboring majority. Default: False.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireFccsRequest): Request to create a grid from LANDFIRE FCCS.

            Returns a single-band grid with categorical fuelbed IDs.
            To convert IDs to fuel parameters, use /grids/lookup/fccs.

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
    body: CreateLandfireFccsRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a grid from LANDFIRE FCCS

     # Create LANDFIRE FCCS Grid

    Creates a grid with FCCS fuelbed IDs from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fccs`) with fuel
    classification system fuelbed IDs (e.g., 26, 598, 34721).

    To convert fuelbed IDs to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fccs` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2023\".
    - **remove_bare_ground**: (optional) Remove bare ground cells (fuelbed ID 0),
                              replaced by neighboring majority. Default: False.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireFccsRequest): Request to create a grid from LANDFIRE FCCS.

            Returns a single-band grid with categorical fuelbed IDs.
            To convert IDs to fuel parameters, use /grids/lookup/fccs.

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
    body: CreateLandfireFccsRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a grid from LANDFIRE FCCS

     # Create LANDFIRE FCCS Grid

    Creates a grid with FCCS fuelbed IDs from LANDFIRE at 30m resolution.

    The grid contains a single categorical band (`fccs`) with fuel
    classification system fuelbed IDs (e.g., 26, 598, 34721).

    To convert fuelbed IDs to fuel parameters (fuel loads, SAV, depth),
    use the `/grids/lookup/fccs` endpoint.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) LANDFIRE version. Default: \"2023\".
    - **remove_bare_ground**: (optional) Remove bare ground cells (fuelbed ID 0),
                              replaced by neighboring majority. Default: False.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateLandfireFccsRequest): Request to create a grid from LANDFIRE FCCS.

            Returns a single-band grid with categorical fuelbed IDs.
            To convert IDs to fuel parameters, use /grids/lookup/fccs.

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
