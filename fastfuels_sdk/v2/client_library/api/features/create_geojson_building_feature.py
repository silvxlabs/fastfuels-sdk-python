from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_geojson_feature_request import CreateGeojsonFeatureRequest
from ...models.feature import Feature
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateGeojsonFeatureRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/domains/{domain_id}/features/building/geojson".format(
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
    body: CreateGeojsonFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Upload a building feature as GeoJSON

     # Upload Building Feature

    Creates a building feature from your own building footprint polygons, such as surveyed buildings
    missing from Overture Maps. The feature is used
    the same way as one from `/building/overture`.

    The polygons are reprojected to the domain CRS and clipped to the domain,
    plus `extent_buffer_m`.

    ## Request Body

    The body **is** a GeoJSON FeatureCollection, with resource metadata as
    top-level fields:

    - **features**: (array) At least one Feature with a `Polygon` or
      `MultiPolygon` geometry. `properties` are optional and are stored as
      columns; each property must have one type across all features.
    - **crs**: (object, optional) The GeoJSON `crs` block. Any CRS is
      accepted. When omitted, coordinates are read as `EPSG:4326`.
    - **name**: (string, optional) Name of the feature.
    - **description**: (string, optional) Description.
    - **tags**: (array of strings, optional) Searchable tags.
    - **extent_buffer_m**: (number, optional) Distance in meters to expand the
      domain extent before clipping. Range: 0–100. Default: 0.

    Returns 422 if a geometry is invalid or no polygon intersects the domain.

    ## Response

    Returns the created Feature with status `\"completed\"`.

    Args:
        domain_id (str):
        body (CreateGeojsonFeatureRequest): Request body for uploading a road, water or building
            feature.

            The body **is** the GeoJSON FeatureCollection, as for ``POST /domains`` and
            layerset uploads, extended with the resource-metadata fields. ``name``
            overrides the optional GeoJSON ``name`` member and is the resource name.

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
    body: CreateGeojsonFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Upload a building feature as GeoJSON

     # Upload Building Feature

    Creates a building feature from your own building footprint polygons, such as surveyed buildings
    missing from Overture Maps. The feature is used
    the same way as one from `/building/overture`.

    The polygons are reprojected to the domain CRS and clipped to the domain,
    plus `extent_buffer_m`.

    ## Request Body

    The body **is** a GeoJSON FeatureCollection, with resource metadata as
    top-level fields:

    - **features**: (array) At least one Feature with a `Polygon` or
      `MultiPolygon` geometry. `properties` are optional and are stored as
      columns; each property must have one type across all features.
    - **crs**: (object, optional) The GeoJSON `crs` block. Any CRS is
      accepted. When omitted, coordinates are read as `EPSG:4326`.
    - **name**: (string, optional) Name of the feature.
    - **description**: (string, optional) Description.
    - **tags**: (array of strings, optional) Searchable tags.
    - **extent_buffer_m**: (number, optional) Distance in meters to expand the
      domain extent before clipping. Range: 0–100. Default: 0.

    Returns 422 if a geometry is invalid or no polygon intersects the domain.

    ## Response

    Returns the created Feature with status `\"completed\"`.

    Args:
        domain_id (str):
        body (CreateGeojsonFeatureRequest): Request body for uploading a road, water or building
            feature.

            The body **is** the GeoJSON FeatureCollection, as for ``POST /domains`` and
            layerset uploads, extended with the resource-metadata fields. ``name``
            overrides the optional GeoJSON ``name`` member and is the resource name.

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
    body: CreateGeojsonFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Upload a building feature as GeoJSON

     # Upload Building Feature

    Creates a building feature from your own building footprint polygons, such as surveyed buildings
    missing from Overture Maps. The feature is used
    the same way as one from `/building/overture`.

    The polygons are reprojected to the domain CRS and clipped to the domain,
    plus `extent_buffer_m`.

    ## Request Body

    The body **is** a GeoJSON FeatureCollection, with resource metadata as
    top-level fields:

    - **features**: (array) At least one Feature with a `Polygon` or
      `MultiPolygon` geometry. `properties` are optional and are stored as
      columns; each property must have one type across all features.
    - **crs**: (object, optional) The GeoJSON `crs` block. Any CRS is
      accepted. When omitted, coordinates are read as `EPSG:4326`.
    - **name**: (string, optional) Name of the feature.
    - **description**: (string, optional) Description.
    - **tags**: (array of strings, optional) Searchable tags.
    - **extent_buffer_m**: (number, optional) Distance in meters to expand the
      domain extent before clipping. Range: 0–100. Default: 0.

    Returns 422 if a geometry is invalid or no polygon intersects the domain.

    ## Response

    Returns the created Feature with status `\"completed\"`.

    Args:
        domain_id (str):
        body (CreateGeojsonFeatureRequest): Request body for uploading a road, water or building
            feature.

            The body **is** the GeoJSON FeatureCollection, as for ``POST /domains`` and
            layerset uploads, extended with the resource-metadata fields. ``name``
            overrides the optional GeoJSON ``name`` member and is the resource name.

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
    body: CreateGeojsonFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Upload a building feature as GeoJSON

     # Upload Building Feature

    Creates a building feature from your own building footprint polygons, such as surveyed buildings
    missing from Overture Maps. The feature is used
    the same way as one from `/building/overture`.

    The polygons are reprojected to the domain CRS and clipped to the domain,
    plus `extent_buffer_m`.

    ## Request Body

    The body **is** a GeoJSON FeatureCollection, with resource metadata as
    top-level fields:

    - **features**: (array) At least one Feature with a `Polygon` or
      `MultiPolygon` geometry. `properties` are optional and are stored as
      columns; each property must have one type across all features.
    - **crs**: (object, optional) The GeoJSON `crs` block. Any CRS is
      accepted. When omitted, coordinates are read as `EPSG:4326`.
    - **name**: (string, optional) Name of the feature.
    - **description**: (string, optional) Description.
    - **tags**: (array of strings, optional) Searchable tags.
    - **extent_buffer_m**: (number, optional) Distance in meters to expand the
      domain extent before clipping. Range: 0–100. Default: 0.

    Returns 422 if a geometry is invalid or no polygon intersects the domain.

    ## Response

    Returns the created Feature with status `\"completed\"`.

    Args:
        domain_id (str):
        body (CreateGeojsonFeatureRequest): Request body for uploading a road, water or building
            feature.

            The body **is** the GeoJSON FeatureCollection, as for ``POST /domains`` and
            layerset uploads, extended with the resource-metadata fields. ``name``
            overrides the optional GeoJSON ``name`` member and is the resource name.

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
