from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_three_dep_point_cloud_request import (
    CreateThreeDepPointCloudRequest,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.point_cloud import PointCloud
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateThreeDepPointCloudRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/pointclouds/3dep".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PointCloud | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = PointCloud.from_dict(response.json())

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
) -> Response[HTTPValidationError | PointCloud | QuotaExceededDetail]:
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
    body: CreateThreeDepPointCloudRequest,
) -> Response[HTTPValidationError | PointCloud | QuotaExceededDetail]:
    """Create a point cloud from USGS 3DEP

     # Create a Point Cloud from USGS 3DEP

    Fetches public airborne lidar from the USGS 3D Elevation Program for this
    domain. The points are clipped to the domain, reprojected to the domain's
    coordinate reference system, and stored as a point cloud you can build on —
    most directly as a canopy height model, which in turn feeds a tree
    inventory.

    The point cloud is returned immediately with `status` = `pending` and is
    fetched in the background: `status` becomes `running`, then `completed` once
    the points are stored and `georeference` and `summary` are filled in — or
    `failed` if the fetch cannot be completed. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    3DEP is airborne, so the resulting point cloud is always type `als`. There
    is no acquisition type to choose.

    ## Choosing acquisitions

    3DEP is published as separate surveys, which overlap and differ in age and
    point density. By default the backend prefers a single survey that covers
    the whole domain, and otherwise combines the fewest surveys that fill it —
    each additional survey introduces a seam between flights of different dates
    and densities. Pass `datasets` to pin the fetch to specific surveys
    instead; check the coverage endpoint first to see what is available.

    Survey boundaries are irregular, so a domain is often covered to
    99-point-something percent rather than exactly 100. Any coverage above zero
    produces a point cloud, and the fraction actually covered is recorded on the
    result as `source.coverage_fraction` — check it if a gap would matter, since
    `summary.density` is measured over the points that exist and looks healthy
    either way. Use the coverage endpoint to see the shortfall before creating
    anything.

    ## Request Body

    - **name**: (optional) Human-readable name.
    - **description**: (optional) Longer free-text description.
    - **tags**: (optional) Tags for organizing and filtering.
    - **datasets**: (optional) Acquisition names to read, in priority order.
      Omit to choose automatically.

    ## Coordinate reference system

    Points are reprojected to the domain's CRS. Only horizontal coordinates are
    transformed — elevations are stored exactly as USGS published them, never
    converted between reference surfaces.

    ## Error Responses

    - **422**: No 3DEP lidar covers this domain, or a pinned acquisition is
      unknown or does not overlap the domain.
    - **429**: A quota was exceeded.
    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):
        body (CreateThreeDepPointCloudRequest): Request body for fetching a point cloud from USGS
            3DEP.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloud | QuotaExceededDetail]
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
    body: CreateThreeDepPointCloudRequest,
) -> HTTPValidationError | PointCloud | QuotaExceededDetail | None:
    """Create a point cloud from USGS 3DEP

     # Create a Point Cloud from USGS 3DEP

    Fetches public airborne lidar from the USGS 3D Elevation Program for this
    domain. The points are clipped to the domain, reprojected to the domain's
    coordinate reference system, and stored as a point cloud you can build on —
    most directly as a canopy height model, which in turn feeds a tree
    inventory.

    The point cloud is returned immediately with `status` = `pending` and is
    fetched in the background: `status` becomes `running`, then `completed` once
    the points are stored and `georeference` and `summary` are filled in — or
    `failed` if the fetch cannot be completed. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    3DEP is airborne, so the resulting point cloud is always type `als`. There
    is no acquisition type to choose.

    ## Choosing acquisitions

    3DEP is published as separate surveys, which overlap and differ in age and
    point density. By default the backend prefers a single survey that covers
    the whole domain, and otherwise combines the fewest surveys that fill it —
    each additional survey introduces a seam between flights of different dates
    and densities. Pass `datasets` to pin the fetch to specific surveys
    instead; check the coverage endpoint first to see what is available.

    Survey boundaries are irregular, so a domain is often covered to
    99-point-something percent rather than exactly 100. Any coverage above zero
    produces a point cloud, and the fraction actually covered is recorded on the
    result as `source.coverage_fraction` — check it if a gap would matter, since
    `summary.density` is measured over the points that exist and looks healthy
    either way. Use the coverage endpoint to see the shortfall before creating
    anything.

    ## Request Body

    - **name**: (optional) Human-readable name.
    - **description**: (optional) Longer free-text description.
    - **tags**: (optional) Tags for organizing and filtering.
    - **datasets**: (optional) Acquisition names to read, in priority order.
      Omit to choose automatically.

    ## Coordinate reference system

    Points are reprojected to the domain's CRS. Only horizontal coordinates are
    transformed — elevations are stored exactly as USGS published them, never
    converted between reference surfaces.

    ## Error Responses

    - **422**: No 3DEP lidar covers this domain, or a pinned acquisition is
      unknown or does not overlap the domain.
    - **429**: A quota was exceeded.
    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):
        body (CreateThreeDepPointCloudRequest): Request body for fetching a point cloud from USGS
            3DEP.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloud | QuotaExceededDetail
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
    body: CreateThreeDepPointCloudRequest,
) -> Response[HTTPValidationError | PointCloud | QuotaExceededDetail]:
    """Create a point cloud from USGS 3DEP

     # Create a Point Cloud from USGS 3DEP

    Fetches public airborne lidar from the USGS 3D Elevation Program for this
    domain. The points are clipped to the domain, reprojected to the domain's
    coordinate reference system, and stored as a point cloud you can build on —
    most directly as a canopy height model, which in turn feeds a tree
    inventory.

    The point cloud is returned immediately with `status` = `pending` and is
    fetched in the background: `status` becomes `running`, then `completed` once
    the points are stored and `georeference` and `summary` are filled in — or
    `failed` if the fetch cannot be completed. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    3DEP is airborne, so the resulting point cloud is always type `als`. There
    is no acquisition type to choose.

    ## Choosing acquisitions

    3DEP is published as separate surveys, which overlap and differ in age and
    point density. By default the backend prefers a single survey that covers
    the whole domain, and otherwise combines the fewest surveys that fill it —
    each additional survey introduces a seam between flights of different dates
    and densities. Pass `datasets` to pin the fetch to specific surveys
    instead; check the coverage endpoint first to see what is available.

    Survey boundaries are irregular, so a domain is often covered to
    99-point-something percent rather than exactly 100. Any coverage above zero
    produces a point cloud, and the fraction actually covered is recorded on the
    result as `source.coverage_fraction` — check it if a gap would matter, since
    `summary.density` is measured over the points that exist and looks healthy
    either way. Use the coverage endpoint to see the shortfall before creating
    anything.

    ## Request Body

    - **name**: (optional) Human-readable name.
    - **description**: (optional) Longer free-text description.
    - **tags**: (optional) Tags for organizing and filtering.
    - **datasets**: (optional) Acquisition names to read, in priority order.
      Omit to choose automatically.

    ## Coordinate reference system

    Points are reprojected to the domain's CRS. Only horizontal coordinates are
    transformed — elevations are stored exactly as USGS published them, never
    converted between reference surfaces.

    ## Error Responses

    - **422**: No 3DEP lidar covers this domain, or a pinned acquisition is
      unknown or does not overlap the domain.
    - **429**: A quota was exceeded.
    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):
        body (CreateThreeDepPointCloudRequest): Request body for fetching a point cloud from USGS
            3DEP.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloud | QuotaExceededDetail]
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
    body: CreateThreeDepPointCloudRequest,
) -> HTTPValidationError | PointCloud | QuotaExceededDetail | None:
    """Create a point cloud from USGS 3DEP

     # Create a Point Cloud from USGS 3DEP

    Fetches public airborne lidar from the USGS 3D Elevation Program for this
    domain. The points are clipped to the domain, reprojected to the domain's
    coordinate reference system, and stored as a point cloud you can build on —
    most directly as a canopy height model, which in turn feeds a tree
    inventory.

    The point cloud is returned immediately with `status` = `pending` and is
    fetched in the background: `status` becomes `running`, then `completed` once
    the points are stored and `georeference` and `summary` are filled in — or
    `failed` if the fetch cannot be completed. Poll
    `GET /domains/{domain_id}/pointclouds/{id}` to follow progress.

    3DEP is airborne, so the resulting point cloud is always type `als`. There
    is no acquisition type to choose.

    ## Choosing acquisitions

    3DEP is published as separate surveys, which overlap and differ in age and
    point density. By default the backend prefers a single survey that covers
    the whole domain, and otherwise combines the fewest surveys that fill it —
    each additional survey introduces a seam between flights of different dates
    and densities. Pass `datasets` to pin the fetch to specific surveys
    instead; check the coverage endpoint first to see what is available.

    Survey boundaries are irregular, so a domain is often covered to
    99-point-something percent rather than exactly 100. Any coverage above zero
    produces a point cloud, and the fraction actually covered is recorded on the
    result as `source.coverage_fraction` — check it if a gap would matter, since
    `summary.density` is measured over the points that exist and looks healthy
    either way. Use the coverage endpoint to see the shortfall before creating
    anything.

    ## Request Body

    - **name**: (optional) Human-readable name.
    - **description**: (optional) Longer free-text description.
    - **tags**: (optional) Tags for organizing and filtering.
    - **datasets**: (optional) Acquisition names to read, in priority order.
      Omit to choose automatically.

    ## Coordinate reference system

    Points are reprojected to the domain's CRS. Only horizontal coordinates are
    transformed — elevations are stored exactly as USGS published them, never
    converted between reference surfaces.

    ## Error Responses

    - **422**: No 3DEP lidar covers this domain, or a pinned acquisition is
      unknown or does not overlap the domain.
    - **429**: A quota was exceeded.
    - **503**: The USGS 3DEP catalog is temporarily unreachable.

    Args:
        domain_id (str):
        body (CreateThreeDepPointCloudRequest): Request body for fetching a point cloud from USGS
            3DEP.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloud | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
