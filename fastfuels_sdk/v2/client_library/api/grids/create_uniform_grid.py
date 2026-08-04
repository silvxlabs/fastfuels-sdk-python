from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_uniform_request import CreateUniformRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateUniformRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/uniform".format(
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
    body: CreateUniformRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a uniform (constant-value) grid

     # Create Uniform Grid

    Creates a grid where every cell is filled with a constant value for each
    specified band. Useful for fuel moisture scenarios, constant fuel loads,
    and other spatially-uniform inputs.

    ## Request Body

    - **resolution**: (required) Grid resolution in meters (>= 1). No default
      since uniform grids have no \"native resolution.\"
    - **bands**: (required) One or more bands, each with a key and value.
      Band keys must be unique.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Available Bands

    **Fuel moisture** (unit: %): `fuel_moisture.1hr`, `fuel_moisture.10hr`,
    `fuel_moisture.100hr`, `fuel_moisture.live_herb`, `fuel_moisture.live_woody`

    **Curing** (unit: %): `curing`

    **Fuel load** (unit: kg/m**2): `fuel_load.1hr`, `fuel_load.10hr`,
    `fuel_load.100hr`, `fuel_load.live_herb`, `fuel_load.live_woody`

    **Fuel depth** (unit: m): `fuel_depth`

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    generate the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateUniformRequest): Request to create a uniform (constant-value) grid.

            Each band fills the entire domain with a single value at the specified
            resolution. No default resolution — it must be explicitly provided since
            uniform grids have no "native resolution."

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
    body: CreateUniformRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a uniform (constant-value) grid

     # Create Uniform Grid

    Creates a grid where every cell is filled with a constant value for each
    specified band. Useful for fuel moisture scenarios, constant fuel loads,
    and other spatially-uniform inputs.

    ## Request Body

    - **resolution**: (required) Grid resolution in meters (>= 1). No default
      since uniform grids have no \"native resolution.\"
    - **bands**: (required) One or more bands, each with a key and value.
      Band keys must be unique.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Available Bands

    **Fuel moisture** (unit: %): `fuel_moisture.1hr`, `fuel_moisture.10hr`,
    `fuel_moisture.100hr`, `fuel_moisture.live_herb`, `fuel_moisture.live_woody`

    **Curing** (unit: %): `curing`

    **Fuel load** (unit: kg/m**2): `fuel_load.1hr`, `fuel_load.10hr`,
    `fuel_load.100hr`, `fuel_load.live_herb`, `fuel_load.live_woody`

    **Fuel depth** (unit: m): `fuel_depth`

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    generate the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateUniformRequest): Request to create a uniform (constant-value) grid.

            Each band fills the entire domain with a single value at the specified
            resolution. No default resolution — it must be explicitly provided since
            uniform grids have no "native resolution."

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
    body: CreateUniformRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a uniform (constant-value) grid

     # Create Uniform Grid

    Creates a grid where every cell is filled with a constant value for each
    specified band. Useful for fuel moisture scenarios, constant fuel loads,
    and other spatially-uniform inputs.

    ## Request Body

    - **resolution**: (required) Grid resolution in meters (>= 1). No default
      since uniform grids have no \"native resolution.\"
    - **bands**: (required) One or more bands, each with a key and value.
      Band keys must be unique.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Available Bands

    **Fuel moisture** (unit: %): `fuel_moisture.1hr`, `fuel_moisture.10hr`,
    `fuel_moisture.100hr`, `fuel_moisture.live_herb`, `fuel_moisture.live_woody`

    **Curing** (unit: %): `curing`

    **Fuel load** (unit: kg/m**2): `fuel_load.1hr`, `fuel_load.10hr`,
    `fuel_load.100hr`, `fuel_load.live_herb`, `fuel_load.live_woody`

    **Fuel depth** (unit: m): `fuel_depth`

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    generate the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateUniformRequest): Request to create a uniform (constant-value) grid.

            Each band fills the entire domain with a single value at the specified
            resolution. No default resolution — it must be explicitly provided since
            uniform grids have no "native resolution."

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
    body: CreateUniformRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a uniform (constant-value) grid

     # Create Uniform Grid

    Creates a grid where every cell is filled with a constant value for each
    specified band. Useful for fuel moisture scenarios, constant fuel loads,
    and other spatially-uniform inputs.

    ## Request Body

    - **resolution**: (required) Grid resolution in meters (>= 1). No default
      since uniform grids have no \"native resolution.\"
    - **bands**: (required) One or more bands, each with a key and value.
      Band keys must be unique.
    - **name**: (optional) Name for the grid.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing grids.

    ## Available Bands

    **Fuel moisture** (unit: %): `fuel_moisture.1hr`, `fuel_moisture.10hr`,
    `fuel_moisture.100hr`, `fuel_moisture.live_herb`, `fuel_moisture.live_woody`

    **Curing** (unit: %): `curing`

    **Fuel load** (unit: kg/m**2): `fuel_load.1hr`, `fuel_load.10hr`,
    `fuel_load.100hr`, `fuel_load.live_herb`, `fuel_load.live_woody`

    **Fuel depth** (unit: m): `fuel_depth`

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    generate the data and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateUniformRequest): Request to create a uniform (constant-value) grid.

            Each band fills the entire domain with a single value at the specified
            resolution. No default resolution — it must be explicitly provided since
            uniform grids have no "native resolution."

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
