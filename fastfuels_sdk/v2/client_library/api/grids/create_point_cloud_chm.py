from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_point_cloud_chm_request import CreatePointCloudChmRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreatePointCloudChmRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/canopy/point_cloud".format(
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
    body: CreatePointCloudChmRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a CHM grid from a point cloud

     # Create a CHM Grid from a Point Cloud

    Creates a grid with canopy height data rasterized from a point cloud. Each
    cell holds the greatest height above ground of any return that falls in it.

    The resulting grid carries the same `chm` band as the Meta, NAIP, and
    LANDFIRE canopy sources, so it can be used anywhere they can — including as
    the source for individual tree detection
    (`POST /domains/{domain_id}/inventories/tree/chm`).

    ## Ground

    Canopy height is height above ground, so the ground surface underneath
    matters. When the point cloud carries ASPRS ground classification
    (class 2), those returns define the ground. When it does not — an upload
    may carry no classification at all — the ground surface is derived from the
    data.

    Which path was taken, and how well the data constrained it, is recorded on
    the completed grid under `source.ground`. Derived ground is accurate in
    forested terrain and degrades over wide areas with no ground returns, such
    as large building footprints or very dense canopy;
    `source.ground.ground_coverage` and `source.ground.max_ground_distance_m`
    are what reveal that.

    ## Request Body

    - **source_point_cloud_id**: The point cloud to rasterize. Must be airborne
      (`type: als`), `completed`, and in this domain.
    - **alignment**: (optional) Output lattice. Against the domain
      (`target: \"domain\"`, the default) `resolution` defaults to 1 m — unlike
      the raster-backed canopy sources there is no source pixel size to
      inherit. Against another grid (`target: \"grid\"`) omitting `resolution`
      matches that grid cell-for-cell, and the output covers the target's
      extent rather than the domain's; giving one keeps the target's origin at
      the new cell size. The target grid must be in this domain's CRS.
      `target: \"native\"` is not supported — a point cloud has no pixel anchor
      to preserve.
    - **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    build the grid and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreatePointCloudChmRequest): Request to create a canopy height model grid from a
            point cloud.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

            The point cloud must be airborne (`type: als`) and `completed`. Cell size
            comes from `alignment.resolution`, defaulting to 1 m — unlike the
            raster-backed canopy sources there is no source pixel size to inherit.

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
    body: CreatePointCloudChmRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a CHM grid from a point cloud

     # Create a CHM Grid from a Point Cloud

    Creates a grid with canopy height data rasterized from a point cloud. Each
    cell holds the greatest height above ground of any return that falls in it.

    The resulting grid carries the same `chm` band as the Meta, NAIP, and
    LANDFIRE canopy sources, so it can be used anywhere they can — including as
    the source for individual tree detection
    (`POST /domains/{domain_id}/inventories/tree/chm`).

    ## Ground

    Canopy height is height above ground, so the ground surface underneath
    matters. When the point cloud carries ASPRS ground classification
    (class 2), those returns define the ground. When it does not — an upload
    may carry no classification at all — the ground surface is derived from the
    data.

    Which path was taken, and how well the data constrained it, is recorded on
    the completed grid under `source.ground`. Derived ground is accurate in
    forested terrain and degrades over wide areas with no ground returns, such
    as large building footprints or very dense canopy;
    `source.ground.ground_coverage` and `source.ground.max_ground_distance_m`
    are what reveal that.

    ## Request Body

    - **source_point_cloud_id**: The point cloud to rasterize. Must be airborne
      (`type: als`), `completed`, and in this domain.
    - **alignment**: (optional) Output lattice. Against the domain
      (`target: \"domain\"`, the default) `resolution` defaults to 1 m — unlike
      the raster-backed canopy sources there is no source pixel size to
      inherit. Against another grid (`target: \"grid\"`) omitting `resolution`
      matches that grid cell-for-cell, and the output covers the target's
      extent rather than the domain's; giving one keeps the target's origin at
      the new cell size. The target grid must be in this domain's CRS.
      `target: \"native\"` is not supported — a point cloud has no pixel anchor
      to preserve.
    - **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    build the grid and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreatePointCloudChmRequest): Request to create a canopy height model grid from a
            point cloud.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

            The point cloud must be airborne (`type: als`) and `completed`. Cell size
            comes from `alignment.resolution`, defaulting to 1 m — unlike the
            raster-backed canopy sources there is no source pixel size to inherit.

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
    body: CreatePointCloudChmRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a CHM grid from a point cloud

     # Create a CHM Grid from a Point Cloud

    Creates a grid with canopy height data rasterized from a point cloud. Each
    cell holds the greatest height above ground of any return that falls in it.

    The resulting grid carries the same `chm` band as the Meta, NAIP, and
    LANDFIRE canopy sources, so it can be used anywhere they can — including as
    the source for individual tree detection
    (`POST /domains/{domain_id}/inventories/tree/chm`).

    ## Ground

    Canopy height is height above ground, so the ground surface underneath
    matters. When the point cloud carries ASPRS ground classification
    (class 2), those returns define the ground. When it does not — an upload
    may carry no classification at all — the ground surface is derived from the
    data.

    Which path was taken, and how well the data constrained it, is recorded on
    the completed grid under `source.ground`. Derived ground is accurate in
    forested terrain and degrades over wide areas with no ground returns, such
    as large building footprints or very dense canopy;
    `source.ground.ground_coverage` and `source.ground.max_ground_distance_m`
    are what reveal that.

    ## Request Body

    - **source_point_cloud_id**: The point cloud to rasterize. Must be airborne
      (`type: als`), `completed`, and in this domain.
    - **alignment**: (optional) Output lattice. Against the domain
      (`target: \"domain\"`, the default) `resolution` defaults to 1 m — unlike
      the raster-backed canopy sources there is no source pixel size to
      inherit. Against another grid (`target: \"grid\"`) omitting `resolution`
      matches that grid cell-for-cell, and the output covers the target's
      extent rather than the domain's; giving one keeps the target's origin at
      the new cell size. The target grid must be in this domain's CRS.
      `target: \"native\"` is not supported — a point cloud has no pixel anchor
      to preserve.
    - **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    build the grid and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreatePointCloudChmRequest): Request to create a canopy height model grid from a
            point cloud.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

            The point cloud must be airborne (`type: als`) and `completed`. Cell size
            comes from `alignment.resolution`, defaulting to 1 m — unlike the
            raster-backed canopy sources there is no source pixel size to inherit.

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
    body: CreatePointCloudChmRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a CHM grid from a point cloud

     # Create a CHM Grid from a Point Cloud

    Creates a grid with canopy height data rasterized from a point cloud. Each
    cell holds the greatest height above ground of any return that falls in it.

    The resulting grid carries the same `chm` band as the Meta, NAIP, and
    LANDFIRE canopy sources, so it can be used anywhere they can — including as
    the source for individual tree detection
    (`POST /domains/{domain_id}/inventories/tree/chm`).

    ## Ground

    Canopy height is height above ground, so the ground surface underneath
    matters. When the point cloud carries ASPRS ground classification
    (class 2), those returns define the ground. When it does not — an upload
    may carry no classification at all — the ground surface is derived from the
    data.

    Which path was taken, and how well the data constrained it, is recorded on
    the completed grid under `source.ground`. Derived ground is accurate in
    forested terrain and degrades over wide areas with no ground returns, such
    as large building footprints or very dense canopy;
    `source.ground.ground_coverage` and `source.ground.max_ground_distance_m`
    are what reveal that.

    ## Request Body

    - **source_point_cloud_id**: The point cloud to rasterize. Must be airborne
      (`type: als`), `completed`, and in this domain.
    - **alignment**: (optional) Output lattice. Against the domain
      (`target: \"domain\"`, the default) `resolution` defaults to 1 m — unlike
      the raster-backed canopy sources there is no source pixel size to
      inherit. Against another grid (`target: \"grid\"`) omitting `resolution`
      matches that grid cell-for-cell, and the output covers the target's
      extent rather than the domain's; giving one keeps the target's origin at
      the new cell size. The target grid must be in this domain's CRS.
      `target: \"native\"` is not supported — a point cloud has no pixel anchor
      to preserve.
    - **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Grid resource with status \"pending\". The backend will
    build the grid and update status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreatePointCloudChmRequest): Request to create a canopy height model grid from a
            point cloud.

            Returns a grid with a single continuous band:
            - chm: Canopy height in meters

            The point cloud must be airborne (`type: als`) and `completed`. Cell size
            comes from `alignment.resolution`, defaulting to 1 m — unlike the
            raster-backed canopy sources there is no source pixel size to inherit.

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
