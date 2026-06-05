from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_layerset_rasterize_request import CreateLayersetRasterizeRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateLayersetRasterizeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/rasterize/layerset".format(
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
    body: CreateLayersetRasterizeRequest,
) -> Response[Grid | HTTPValidationError]:
    """Create a grid by rasterizing a layerset

     # Create Layerset-Rasterized Grid

    Rasterizes a previously-uploaded fuelbed layerset into a grid aligned
    to the domain (default) or to a target grid.

    The `layerset_id` must reference a Feature uploaded for this domain via
    `POST /domains/{domain_id}/features/layerset` and owned by the caller.

    ## Request Body

    - **layerset_id**: (required) Feature ID of the layerset to rasterize.
    - **overlap_method**: (optional) Per-cell reduction when polygons of the
      same `fuel_type` overlap a single cell. One of `mean`, `max`, `min`.
      Default: `mean`. (Loading is always summed across overlapping polygons
      regardless of this setting.)
    - **alignment**: (optional) See alignment docs. Default: anchored to domain.
    - **extent_buffer_cells**: (optional) Buffer in result-grid cells around
      the domain extent. Cells inside the buffered extent that fall outside
      polygon coverage are populated with the rasterizer's fill value.
    - **name**, **description**, **tags**, **modifications**: standard grid metadata.

    ## Response

    Returns the created Grid resource with status `pending`. The backend
    fetches the layerset GeoJSON from GCS, rasterizes it, and updates the
    status to `completed` when ready.

    Args:
        domain_id (str):
        body (CreateLayersetRasterizeRequest): Request to create a grid by rasterizing a
            previously-uploaded layerset.

            The referenced layerset must be an existing Feature owned by the caller,
            uploaded via ``POST /domains/{id}/features/layerset``. The worker fetches
            the GeoJSON from GCS at job time; a fresh upload produces a new
            ``feature_id``, so the reference is effectively immutable.

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
    body: CreateLayersetRasterizeRequest,
) -> Grid | HTTPValidationError | None:
    """Create a grid by rasterizing a layerset

     # Create Layerset-Rasterized Grid

    Rasterizes a previously-uploaded fuelbed layerset into a grid aligned
    to the domain (default) or to a target grid.

    The `layerset_id` must reference a Feature uploaded for this domain via
    `POST /domains/{domain_id}/features/layerset` and owned by the caller.

    ## Request Body

    - **layerset_id**: (required) Feature ID of the layerset to rasterize.
    - **overlap_method**: (optional) Per-cell reduction when polygons of the
      same `fuel_type` overlap a single cell. One of `mean`, `max`, `min`.
      Default: `mean`. (Loading is always summed across overlapping polygons
      regardless of this setting.)
    - **alignment**: (optional) See alignment docs. Default: anchored to domain.
    - **extent_buffer_cells**: (optional) Buffer in result-grid cells around
      the domain extent. Cells inside the buffered extent that fall outside
      polygon coverage are populated with the rasterizer's fill value.
    - **name**, **description**, **tags**, **modifications**: standard grid metadata.

    ## Response

    Returns the created Grid resource with status `pending`. The backend
    fetches the layerset GeoJSON from GCS, rasterizes it, and updates the
    status to `completed` when ready.

    Args:
        domain_id (str):
        body (CreateLayersetRasterizeRequest): Request to create a grid by rasterizing a
            previously-uploaded layerset.

            The referenced layerset must be an existing Feature owned by the caller,
            uploaded via ``POST /domains/{id}/features/layerset``. The worker fetches
            the GeoJSON from GCS at job time; a fresh upload produces a new
            ``feature_id``, so the reference is effectively immutable.

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
    body: CreateLayersetRasterizeRequest,
) -> Response[Grid | HTTPValidationError]:
    """Create a grid by rasterizing a layerset

     # Create Layerset-Rasterized Grid

    Rasterizes a previously-uploaded fuelbed layerset into a grid aligned
    to the domain (default) or to a target grid.

    The `layerset_id` must reference a Feature uploaded for this domain via
    `POST /domains/{domain_id}/features/layerset` and owned by the caller.

    ## Request Body

    - **layerset_id**: (required) Feature ID of the layerset to rasterize.
    - **overlap_method**: (optional) Per-cell reduction when polygons of the
      same `fuel_type` overlap a single cell. One of `mean`, `max`, `min`.
      Default: `mean`. (Loading is always summed across overlapping polygons
      regardless of this setting.)
    - **alignment**: (optional) See alignment docs. Default: anchored to domain.
    - **extent_buffer_cells**: (optional) Buffer in result-grid cells around
      the domain extent. Cells inside the buffered extent that fall outside
      polygon coverage are populated with the rasterizer's fill value.
    - **name**, **description**, **tags**, **modifications**: standard grid metadata.

    ## Response

    Returns the created Grid resource with status `pending`. The backend
    fetches the layerset GeoJSON from GCS, rasterizes it, and updates the
    status to `completed` when ready.

    Args:
        domain_id (str):
        body (CreateLayersetRasterizeRequest): Request to create a grid by rasterizing a
            previously-uploaded layerset.

            The referenced layerset must be an existing Feature owned by the caller,
            uploaded via ``POST /domains/{id}/features/layerset``. The worker fetches
            the GeoJSON from GCS at job time; a fresh upload produces a new
            ``feature_id``, so the reference is effectively immutable.

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
    body: CreateLayersetRasterizeRequest,
) -> Grid | HTTPValidationError | None:
    """Create a grid by rasterizing a layerset

     # Create Layerset-Rasterized Grid

    Rasterizes a previously-uploaded fuelbed layerset into a grid aligned
    to the domain (default) or to a target grid.

    The `layerset_id` must reference a Feature uploaded for this domain via
    `POST /domains/{domain_id}/features/layerset` and owned by the caller.

    ## Request Body

    - **layerset_id**: (required) Feature ID of the layerset to rasterize.
    - **overlap_method**: (optional) Per-cell reduction when polygons of the
      same `fuel_type` overlap a single cell. One of `mean`, `max`, `min`.
      Default: `mean`. (Loading is always summed across overlapping polygons
      regardless of this setting.)
    - **alignment**: (optional) See alignment docs. Default: anchored to domain.
    - **extent_buffer_cells**: (optional) Buffer in result-grid cells around
      the domain extent. Cells inside the buffered extent that fall outside
      polygon coverage are populated with the rasterizer's fill value.
    - **name**, **description**, **tags**, **modifications**: standard grid metadata.

    ## Response

    Returns the created Grid resource with status `pending`. The backend
    fetches the layerset GeoJSON from GCS, rasterizes it, and updates the
    status to `completed` when ready.

    Args:
        domain_id (str):
        body (CreateLayersetRasterizeRequest): Request to create a grid by rasterizing a
            previously-uploaded layerset.

            The referenced layerset must be an existing Feature owned by the caller,
            uploaded via ``POST /domains/{id}/features/layerset``. The worker fetches
            the GeoJSON from GCS at job time; a fresh upload produces a new
            ``feature_id``, so the reference is effectively immutable.

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
