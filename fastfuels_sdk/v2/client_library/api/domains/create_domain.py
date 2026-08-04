from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.domain import Domain
from ...models.geo_json_feature_collection import GeoJsonFeatureCollection
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    *,
    body: GeoJsonFeatureCollection,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Domain | HTTPValidationError | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = Domain.from_dict(response.json())

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
) -> Response[Domain | HTTPValidationError | QuotaExceededDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: GeoJsonFeatureCollection,
) -> Response[Domain | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a new domain

     # Create Domain Endpoint

    This endpoint creates a new domain resource based on a spatial extent and
    additional details provided by the user. The domain resource acts as the
    spatial container for all other resources that create data within the system.

    ## What is a Domain Resource?

    A domain resource is a spatial container that represents a specific geographical
    area. It includes metadata such as the name, description, creation date, and the
    spatial extent defined by geographic coordinates. Domains are used to organize
    and manage spatial data and operations within a defined area.

    ## Request Body

    The request body must be a GeoJSON FeatureCollection as defined by the
    [GeoJSON specification (RFC 7946)](https://datatracker.ietf.org/doc/html/rfc7946).

    ### Required Fields

    - **type**: (string) Must be \"FeatureCollection\".
    - **features**: (array) An array of Feature objects. Each Feature must have:
      - **type**: (string) Must be \"Feature\".
      - **geometry**: (GeoJSON Geometry) A geometry object (typically Polygon).
        - **type**: (string) Must be a valid GeoJSON type, e.g., \"Polygon\".
        - **coordinates**: (array) An array of coordinates defining the geometry.

    ### Optional Fields

    - **name**: (string) The name of the domain. Default: empty string.
    - **description**: (string) A brief description of the domain. Default: empty string.
    - **tags**: (array of strings) Tags for organizing and filtering domains.
    - **crs**: (object) The coordinate reference system. Default: EPSG:4326 (WGS84).
      - **type**: (string) Must be \"name\".
      - **properties**: (object) Contains the CRS details.
        - **name**: (string) The CRS identifier, e.g., \"EPSG:4326\", \"EPSG:5070\",
          or URN format \"urn:ogc:def:crs:EPSG::32611\".
    - **pad_to_resolution**: (number) Optional resolution in meters to snap the
      domain bounding box to. When set, the bounding box (the \"domain\" feature)
      is snapped outward to the nearest multiple of this value. Grids whose
      resolutions divide evenly into this value will produce identical, aligned
      footprints on this domain. Useful for compositional workflows where
      multiple grids at different resolutions need to share an extent.
    - **style**: (object) Optional visual style for rendering the domain on a
      map. Sub-fields: `stroke_color`, `stroke_opacity` (0-1), `stroke_width`
      (>= 0), `fill_color`, `fill_opacity` (0-1). Color strings accept any
      format the renderer understands (hex, named, `rgb()`, ...) and are
      capped at 64 characters.

    ## Response

    On successful creation, returns the domain resource with:

    - **id**: (string) A unique 32-character hex identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) A single feature named `\"domain\"` — a polygon
      covering the working extent (bounding box of the input, possibly
      padded). This is what griddle, standgen, and exporter use as the
      authoritative spatial extent.
    - **bbox**: (array) Standard GeoJSON bbox `[minx, miny, maxx, maxy]` in the
      domain's projected CRS. Equals the bounds of the \"domain\" feature.
    - **pad_to_resolution**: (number, optional) The padding value, if set.

    ## CRS Handling

    The API handles coordinate reference systems as follows:

    1. **Geographic CRS (e.g., EPSG:4326)**: Automatically projected to the
       appropriate UTM zone based on the geometry's centroid. The response CRS
       will be the UTM zone (e.g., EPSG:32611 for UTM Zone 11N).

    2. **Projected CRS (e.g., EPSG:5070, EPSG:32611)**: Used as-is without
       reprojection. The response CRS will match the input CRS.

    ## Validation

    The following validations are performed:

    1. **CRS Validation**: Must be a valid EPSG code or URN format.
    2. **Area Validation**: Geometry must have non-zero area (no points or lines).
    3. **Location**: Geometry must be entirely within CONUS (Continental US).
       Validated against the original input polygon (not the padded bbox).
    4. **Size Limit**: The working extent (possibly padded bbox) must be less
       than 16 square kilometers.

    ## Important Notes

    1. **FeatureCollection Only**: Unlike v1, this endpoint only accepts
       FeatureCollection input, not individual Feature objects. Wrap single
       features in a FeatureCollection.

    2. **Working-Extent Output**: The created domain stores a single \"domain\"
       feature — the bounding box of the input geometry, which is the working
       extent used by all downstream services. The submitted geometry itself
       is not stored.

    3. **Projection**: Geographic coordinates are always projected to a suitable
       UTM zone for accurate area calculations and grid operations.

    4. **Maximum Area**: The 16 sq km limit ensures reasonable processing times.
       Contact support if you need larger domains.

    ## Error Responses

    - **422 Unprocessable Entity**:
      - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
      - \"Invalid geometry. The feature must have an area greater than zero.\"
      - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
      - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (GeoJsonFeatureCollection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: GeoJsonFeatureCollection,
) -> Domain | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a new domain

     # Create Domain Endpoint

    This endpoint creates a new domain resource based on a spatial extent and
    additional details provided by the user. The domain resource acts as the
    spatial container for all other resources that create data within the system.

    ## What is a Domain Resource?

    A domain resource is a spatial container that represents a specific geographical
    area. It includes metadata such as the name, description, creation date, and the
    spatial extent defined by geographic coordinates. Domains are used to organize
    and manage spatial data and operations within a defined area.

    ## Request Body

    The request body must be a GeoJSON FeatureCollection as defined by the
    [GeoJSON specification (RFC 7946)](https://datatracker.ietf.org/doc/html/rfc7946).

    ### Required Fields

    - **type**: (string) Must be \"FeatureCollection\".
    - **features**: (array) An array of Feature objects. Each Feature must have:
      - **type**: (string) Must be \"Feature\".
      - **geometry**: (GeoJSON Geometry) A geometry object (typically Polygon).
        - **type**: (string) Must be a valid GeoJSON type, e.g., \"Polygon\".
        - **coordinates**: (array) An array of coordinates defining the geometry.

    ### Optional Fields

    - **name**: (string) The name of the domain. Default: empty string.
    - **description**: (string) A brief description of the domain. Default: empty string.
    - **tags**: (array of strings) Tags for organizing and filtering domains.
    - **crs**: (object) The coordinate reference system. Default: EPSG:4326 (WGS84).
      - **type**: (string) Must be \"name\".
      - **properties**: (object) Contains the CRS details.
        - **name**: (string) The CRS identifier, e.g., \"EPSG:4326\", \"EPSG:5070\",
          or URN format \"urn:ogc:def:crs:EPSG::32611\".
    - **pad_to_resolution**: (number) Optional resolution in meters to snap the
      domain bounding box to. When set, the bounding box (the \"domain\" feature)
      is snapped outward to the nearest multiple of this value. Grids whose
      resolutions divide evenly into this value will produce identical, aligned
      footprints on this domain. Useful for compositional workflows where
      multiple grids at different resolutions need to share an extent.
    - **style**: (object) Optional visual style for rendering the domain on a
      map. Sub-fields: `stroke_color`, `stroke_opacity` (0-1), `stroke_width`
      (>= 0), `fill_color`, `fill_opacity` (0-1). Color strings accept any
      format the renderer understands (hex, named, `rgb()`, ...) and are
      capped at 64 characters.

    ## Response

    On successful creation, returns the domain resource with:

    - **id**: (string) A unique 32-character hex identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) A single feature named `\"domain\"` — a polygon
      covering the working extent (bounding box of the input, possibly
      padded). This is what griddle, standgen, and exporter use as the
      authoritative spatial extent.
    - **bbox**: (array) Standard GeoJSON bbox `[minx, miny, maxx, maxy]` in the
      domain's projected CRS. Equals the bounds of the \"domain\" feature.
    - **pad_to_resolution**: (number, optional) The padding value, if set.

    ## CRS Handling

    The API handles coordinate reference systems as follows:

    1. **Geographic CRS (e.g., EPSG:4326)**: Automatically projected to the
       appropriate UTM zone based on the geometry's centroid. The response CRS
       will be the UTM zone (e.g., EPSG:32611 for UTM Zone 11N).

    2. **Projected CRS (e.g., EPSG:5070, EPSG:32611)**: Used as-is without
       reprojection. The response CRS will match the input CRS.

    ## Validation

    The following validations are performed:

    1. **CRS Validation**: Must be a valid EPSG code or URN format.
    2. **Area Validation**: Geometry must have non-zero area (no points or lines).
    3. **Location**: Geometry must be entirely within CONUS (Continental US).
       Validated against the original input polygon (not the padded bbox).
    4. **Size Limit**: The working extent (possibly padded bbox) must be less
       than 16 square kilometers.

    ## Important Notes

    1. **FeatureCollection Only**: Unlike v1, this endpoint only accepts
       FeatureCollection input, not individual Feature objects. Wrap single
       features in a FeatureCollection.

    2. **Working-Extent Output**: The created domain stores a single \"domain\"
       feature — the bounding box of the input geometry, which is the working
       extent used by all downstream services. The submitted geometry itself
       is not stored.

    3. **Projection**: Geographic coordinates are always projected to a suitable
       UTM zone for accurate area calculations and grid operations.

    4. **Maximum Area**: The 16 sq km limit ensures reasonable processing times.
       Contact support if you need larger domains.

    ## Error Responses

    - **422 Unprocessable Entity**:
      - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
      - \"Invalid geometry. The feature must have an area greater than zero.\"
      - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
      - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (GeoJsonFeatureCollection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Domain | HTTPValidationError | QuotaExceededDetail
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: GeoJsonFeatureCollection,
) -> Response[Domain | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a new domain

     # Create Domain Endpoint

    This endpoint creates a new domain resource based on a spatial extent and
    additional details provided by the user. The domain resource acts as the
    spatial container for all other resources that create data within the system.

    ## What is a Domain Resource?

    A domain resource is a spatial container that represents a specific geographical
    area. It includes metadata such as the name, description, creation date, and the
    spatial extent defined by geographic coordinates. Domains are used to organize
    and manage spatial data and operations within a defined area.

    ## Request Body

    The request body must be a GeoJSON FeatureCollection as defined by the
    [GeoJSON specification (RFC 7946)](https://datatracker.ietf.org/doc/html/rfc7946).

    ### Required Fields

    - **type**: (string) Must be \"FeatureCollection\".
    - **features**: (array) An array of Feature objects. Each Feature must have:
      - **type**: (string) Must be \"Feature\".
      - **geometry**: (GeoJSON Geometry) A geometry object (typically Polygon).
        - **type**: (string) Must be a valid GeoJSON type, e.g., \"Polygon\".
        - **coordinates**: (array) An array of coordinates defining the geometry.

    ### Optional Fields

    - **name**: (string) The name of the domain. Default: empty string.
    - **description**: (string) A brief description of the domain. Default: empty string.
    - **tags**: (array of strings) Tags for organizing and filtering domains.
    - **crs**: (object) The coordinate reference system. Default: EPSG:4326 (WGS84).
      - **type**: (string) Must be \"name\".
      - **properties**: (object) Contains the CRS details.
        - **name**: (string) The CRS identifier, e.g., \"EPSG:4326\", \"EPSG:5070\",
          or URN format \"urn:ogc:def:crs:EPSG::32611\".
    - **pad_to_resolution**: (number) Optional resolution in meters to snap the
      domain bounding box to. When set, the bounding box (the \"domain\" feature)
      is snapped outward to the nearest multiple of this value. Grids whose
      resolutions divide evenly into this value will produce identical, aligned
      footprints on this domain. Useful for compositional workflows where
      multiple grids at different resolutions need to share an extent.
    - **style**: (object) Optional visual style for rendering the domain on a
      map. Sub-fields: `stroke_color`, `stroke_opacity` (0-1), `stroke_width`
      (>= 0), `fill_color`, `fill_opacity` (0-1). Color strings accept any
      format the renderer understands (hex, named, `rgb()`, ...) and are
      capped at 64 characters.

    ## Response

    On successful creation, returns the domain resource with:

    - **id**: (string) A unique 32-character hex identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) A single feature named `\"domain\"` — a polygon
      covering the working extent (bounding box of the input, possibly
      padded). This is what griddle, standgen, and exporter use as the
      authoritative spatial extent.
    - **bbox**: (array) Standard GeoJSON bbox `[minx, miny, maxx, maxy]` in the
      domain's projected CRS. Equals the bounds of the \"domain\" feature.
    - **pad_to_resolution**: (number, optional) The padding value, if set.

    ## CRS Handling

    The API handles coordinate reference systems as follows:

    1. **Geographic CRS (e.g., EPSG:4326)**: Automatically projected to the
       appropriate UTM zone based on the geometry's centroid. The response CRS
       will be the UTM zone (e.g., EPSG:32611 for UTM Zone 11N).

    2. **Projected CRS (e.g., EPSG:5070, EPSG:32611)**: Used as-is without
       reprojection. The response CRS will match the input CRS.

    ## Validation

    The following validations are performed:

    1. **CRS Validation**: Must be a valid EPSG code or URN format.
    2. **Area Validation**: Geometry must have non-zero area (no points or lines).
    3. **Location**: Geometry must be entirely within CONUS (Continental US).
       Validated against the original input polygon (not the padded bbox).
    4. **Size Limit**: The working extent (possibly padded bbox) must be less
       than 16 square kilometers.

    ## Important Notes

    1. **FeatureCollection Only**: Unlike v1, this endpoint only accepts
       FeatureCollection input, not individual Feature objects. Wrap single
       features in a FeatureCollection.

    2. **Working-Extent Output**: The created domain stores a single \"domain\"
       feature — the bounding box of the input geometry, which is the working
       extent used by all downstream services. The submitted geometry itself
       is not stored.

    3. **Projection**: Geographic coordinates are always projected to a suitable
       UTM zone for accurate area calculations and grid operations.

    4. **Maximum Area**: The 16 sq km limit ensures reasonable processing times.
       Contact support if you need larger domains.

    ## Error Responses

    - **422 Unprocessable Entity**:
      - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
      - \"Invalid geometry. The feature must have an area greater than zero.\"
      - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
      - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (GeoJsonFeatureCollection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Domain | HTTPValidationError | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: GeoJsonFeatureCollection,
) -> Domain | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a new domain

     # Create Domain Endpoint

    This endpoint creates a new domain resource based on a spatial extent and
    additional details provided by the user. The domain resource acts as the
    spatial container for all other resources that create data within the system.

    ## What is a Domain Resource?

    A domain resource is a spatial container that represents a specific geographical
    area. It includes metadata such as the name, description, creation date, and the
    spatial extent defined by geographic coordinates. Domains are used to organize
    and manage spatial data and operations within a defined area.

    ## Request Body

    The request body must be a GeoJSON FeatureCollection as defined by the
    [GeoJSON specification (RFC 7946)](https://datatracker.ietf.org/doc/html/rfc7946).

    ### Required Fields

    - **type**: (string) Must be \"FeatureCollection\".
    - **features**: (array) An array of Feature objects. Each Feature must have:
      - **type**: (string) Must be \"Feature\".
      - **geometry**: (GeoJSON Geometry) A geometry object (typically Polygon).
        - **type**: (string) Must be a valid GeoJSON type, e.g., \"Polygon\".
        - **coordinates**: (array) An array of coordinates defining the geometry.

    ### Optional Fields

    - **name**: (string) The name of the domain. Default: empty string.
    - **description**: (string) A brief description of the domain. Default: empty string.
    - **tags**: (array of strings) Tags for organizing and filtering domains.
    - **crs**: (object) The coordinate reference system. Default: EPSG:4326 (WGS84).
      - **type**: (string) Must be \"name\".
      - **properties**: (object) Contains the CRS details.
        - **name**: (string) The CRS identifier, e.g., \"EPSG:4326\", \"EPSG:5070\",
          or URN format \"urn:ogc:def:crs:EPSG::32611\".
    - **pad_to_resolution**: (number) Optional resolution in meters to snap the
      domain bounding box to. When set, the bounding box (the \"domain\" feature)
      is snapped outward to the nearest multiple of this value. Grids whose
      resolutions divide evenly into this value will produce identical, aligned
      footprints on this domain. Useful for compositional workflows where
      multiple grids at different resolutions need to share an extent.
    - **style**: (object) Optional visual style for rendering the domain on a
      map. Sub-fields: `stroke_color`, `stroke_opacity` (0-1), `stroke_width`
      (>= 0), `fill_color`, `fill_opacity` (0-1). Color strings accept any
      format the renderer understands (hex, named, `rgb()`, ...) and are
      capped at 64 characters.

    ## Response

    On successful creation, returns the domain resource with:

    - **id**: (string) A unique 32-character hex identifier for the domain.
    - **type**: (string) Always \"FeatureCollection\".
    - **name**: (string) The name of the domain.
    - **description**: (string) The description of the domain.
    - **created_on**: (datetime) When the domain was created.
    - **modified_on**: (datetime) When the domain was last modified.
    - **tags**: (array) The tags associated with the domain.
    - **crs**: (object) The coordinate reference system (always projected).
    - **features**: (array) A single feature named `\"domain\"` — a polygon
      covering the working extent (bounding box of the input, possibly
      padded). This is what griddle, standgen, and exporter use as the
      authoritative spatial extent.
    - **bbox**: (array) Standard GeoJSON bbox `[minx, miny, maxx, maxy]` in the
      domain's projected CRS. Equals the bounds of the \"domain\" feature.
    - **pad_to_resolution**: (number, optional) The padding value, if set.

    ## CRS Handling

    The API handles coordinate reference systems as follows:

    1. **Geographic CRS (e.g., EPSG:4326)**: Automatically projected to the
       appropriate UTM zone based on the geometry's centroid. The response CRS
       will be the UTM zone (e.g., EPSG:32611 for UTM Zone 11N).

    2. **Projected CRS (e.g., EPSG:5070, EPSG:32611)**: Used as-is without
       reprojection. The response CRS will match the input CRS.

    ## Validation

    The following validations are performed:

    1. **CRS Validation**: Must be a valid EPSG code or URN format.
    2. **Area Validation**: Geometry must have non-zero area (no points or lines).
    3. **Location**: Geometry must be entirely within CONUS (Continental US).
       Validated against the original input polygon (not the padded bbox).
    4. **Size Limit**: The working extent (possibly padded bbox) must be less
       than 16 square kilometers.

    ## Important Notes

    1. **FeatureCollection Only**: Unlike v1, this endpoint only accepts
       FeatureCollection input, not individual Feature objects. Wrap single
       features in a FeatureCollection.

    2. **Working-Extent Output**: The created domain stores a single \"domain\"
       feature — the bounding box of the input geometry, which is the working
       extent used by all downstream services. The submitted geometry itself
       is not stored.

    3. **Projection**: Geographic coordinates are always projected to a suitable
       UTM zone for accurate area calculations and grid operations.

    4. **Maximum Area**: The 16 sq km limit ensures reasonable processing times.
       Contact support if you need larger domains.

    ## Error Responses

    - **422 Unprocessable Entity**:
      - \"Invalid CRS '{crs}'. Must be a valid authority string (e.g., 'EPSG:4326').\"
      - \"Invalid geometry. The feature must have an area greater than zero.\"
      - \"Invalid spatial extent. Area must be less than 16 square kilometers.\"
      - \"Invalid spatial extent. The domain must be entirely within CONUS.\"

    Args:
        body (GeoJsonFeatureCollection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Domain | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
