from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_meta_chm_request import CreateMetaChmRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateMetaChmRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/canopy/meta".format(
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
    body: CreateMetaChmRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a grid from Meta CHM

     # Create Meta CHM Grid

    Creates a grid with canopy height data from Meta's global canopy height
    model at ~1m resolution.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) Meta CHM version. Default: \"2\".
        - **1**: Tolan, J. et al. (2024). Very high resolution canopy height maps from RGB imagery.
        - **2**: Brandt, J. et al. (2026). CHMv2: Improvements in Global Canopy Height Mapping using
    DINOv3.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateMetaChmRequest): Request to create a grid from Meta CHM.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

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
    body: CreateMetaChmRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a grid from Meta CHM

     # Create Meta CHM Grid

    Creates a grid with canopy height data from Meta's global canopy height
    model at ~1m resolution.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) Meta CHM version. Default: \"2\".
        - **1**: Tolan, J. et al. (2024). Very high resolution canopy height maps from RGB imagery.
        - **2**: Brandt, J. et al. (2026). CHMv2: Improvements in Global Canopy Height Mapping using
    DINOv3.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateMetaChmRequest): Request to create a grid from Meta CHM.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

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
    body: CreateMetaChmRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a grid from Meta CHM

     # Create Meta CHM Grid

    Creates a grid with canopy height data from Meta's global canopy height
    model at ~1m resolution.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) Meta CHM version. Default: \"2\".
        - **1**: Tolan, J. et al. (2024). Very high resolution canopy height maps from RGB imagery.
        - **2**: Brandt, J. et al. (2026). CHMv2: Improvements in Global Canopy Height Mapping using
    DINOv3.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateMetaChmRequest): Request to create a grid from Meta CHM.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

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
    body: CreateMetaChmRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a grid from Meta CHM

     # Create Meta CHM Grid

    Creates a grid with canopy height data from Meta's global canopy height
    model at ~1m resolution.

    ## Request Body

    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.
    - **version**: (optional) Meta CHM version. Default: \"2\".
        - **1**: Tolan, J. et al. (2024). Very high resolution canopy height maps from RGB imagery.
        - **2**: Brandt, J. et al. (2026). CHMv2: Improvements in Global Canopy Height Mapping using
    DINOv3.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    fetch the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateMetaChmRequest): Request to create a grid from Meta CHM.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

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
