from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_osm_road_feature_request import CreateOsmRoadFeatureRequest
from ...models.feature import Feature
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateOsmRoadFeatureRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/features/road/osm".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = Feature.from_dict(response.json())

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
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
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
    body: CreateOsmRoadFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a road feature from OpenStreetMap

     # Create OSM Road Feature

    Generates a polygon representation of the road network within the specified
    domain using data from OpenStreetMap (OSM).

    The backend worker will:
    1. Fetch the bounding box for the target domain.
    2. Query OpenStreetMap for linear road segments (`highway=*`).
    3. Dynamically buffer the line strings into realistic polygon areas
       based on their specific OSM classification (e.g., motorways receive
       a wider buffer than residential streets or trails).
    4. Save the resulting GeoJSON to the features bucket.

    ## Request Body

    - **name**: (optional) Name for the road feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent outward before clipping fetched roads. Lets roads that exit the
      domain at the boundary extend slightly past the edge, providing context
      for visualization and downstream operations. Applied in the domain's
      projected CRS. If omitted, roads are clipped exactly to the domain
      boundary. Range: 0–100 meters.

    ## Response

    Returns the created Feature resource with status ``\"pending\"``. The
    backend worker will process the OSM extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateOsmRoadFeatureRequest): Request body for creating a road feature via
            OpenStreetMap.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Feature | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateOsmRoadFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a road feature from OpenStreetMap

     # Create OSM Road Feature

    Generates a polygon representation of the road network within the specified
    domain using data from OpenStreetMap (OSM).

    The backend worker will:
    1. Fetch the bounding box for the target domain.
    2. Query OpenStreetMap for linear road segments (`highway=*`).
    3. Dynamically buffer the line strings into realistic polygon areas
       based on their specific OSM classification (e.g., motorways receive
       a wider buffer than residential streets or trails).
    4. Save the resulting GeoJSON to the features bucket.

    ## Request Body

    - **name**: (optional) Name for the road feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent outward before clipping fetched roads. Lets roads that exit the
      domain at the boundary extend slightly past the edge, providing context
      for visualization and downstream operations. Applied in the domain's
      projected CRS. If omitted, roads are clipped exactly to the domain
      boundary. Range: 0–100 meters.

    ## Response

    Returns the created Feature resource with status ``\"pending\"``. The
    backend worker will process the OSM extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateOsmRoadFeatureRequest): Request body for creating a road feature via
            OpenStreetMap.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Feature | HTTPValidationError | QuotaExceededDetail
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
    body: CreateOsmRoadFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a road feature from OpenStreetMap

     # Create OSM Road Feature

    Generates a polygon representation of the road network within the specified
    domain using data from OpenStreetMap (OSM).

    The backend worker will:
    1. Fetch the bounding box for the target domain.
    2. Query OpenStreetMap for linear road segments (`highway=*`).
    3. Dynamically buffer the line strings into realistic polygon areas
       based on their specific OSM classification (e.g., motorways receive
       a wider buffer than residential streets or trails).
    4. Save the resulting GeoJSON to the features bucket.

    ## Request Body

    - **name**: (optional) Name for the road feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent outward before clipping fetched roads. Lets roads that exit the
      domain at the boundary extend slightly past the edge, providing context
      for visualization and downstream operations. Applied in the domain's
      projected CRS. If omitted, roads are clipped exactly to the domain
      boundary. Range: 0–100 meters.

    ## Response

    Returns the created Feature resource with status ``\"pending\"``. The
    backend worker will process the OSM extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateOsmRoadFeatureRequest): Request body for creating a road feature via
            OpenStreetMap.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Feature | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateOsmRoadFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a road feature from OpenStreetMap

     # Create OSM Road Feature

    Generates a polygon representation of the road network within the specified
    domain using data from OpenStreetMap (OSM).

    The backend worker will:
    1. Fetch the bounding box for the target domain.
    2. Query OpenStreetMap for linear road segments (`highway=*`).
    3. Dynamically buffer the line strings into realistic polygon areas
       based on their specific OSM classification (e.g., motorways receive
       a wider buffer than residential streets or trails).
    4. Save the resulting GeoJSON to the features bucket.

    ## Request Body

    - **name**: (optional) Name for the road feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent outward before clipping fetched roads. Lets roads that exit the
      domain at the boundary extend slightly past the edge, providing context
      for visualization and downstream operations. Applied in the domain's
      projected CRS. If omitted, roads are clipped exactly to the domain
      boundary. Range: 0–100 meters.

    ## Response

    Returns the created Feature resource with status ``\"pending\"``. The
    backend worker will process the OSM extraction asynchronously and update
    status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateOsmRoadFeatureRequest): Request body for creating a road feature via
            OpenStreetMap.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Feature | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
