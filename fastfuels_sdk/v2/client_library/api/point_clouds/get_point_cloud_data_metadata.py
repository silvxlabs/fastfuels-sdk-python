from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.point_cloud_data_metadata import PointCloudDataMetadata
from ...types import Response


def _get_kwargs(
    domain_id: str,
    point_cloud_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata".format(
            domain_id=quote(str(domain_id), safe=""),
            point_cloud_id=quote(str(point_cloud_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PointCloudDataMetadata | None:
    if response.status_code == 200:
        response_200 = PointCloudDataMetadata.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | PointCloudDataMetadata]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | PointCloudDataMetadata]:
    """Get point-cloud tile metadata

     # Get Point-Cloud Data Metadata

    Returns the public read index for a completed point cloud without returning
    any point values. Call this endpoint first to discover the occupied tiles,
    stored columns and dtypes, coordinate encoding, and the number of points
    each level of detail (LOD) would return.

    A typical client workflow is:

    1. Read this metadata once.
    2. Select one of the entries in `tiles`.
    3. Choose an LOD whose cumulative point count fits the client workload.
    4. Request that tile from the JSON or binary data endpoint.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    - **tile_m**: Width and height of each tile in the units of `crs`.
    - **lod_levels**: Number of available cumulative LOD selections. The
      current format has six levels, numbered `0` through `5`.
    - **crs**: Coordinate reference system for the decoded point coordinates
      and all reported bounds.
    - **bounds**: Horizontal point-cloud extent as
      `[min_x, min_y, max_x, max_y]`.
    - **scales** and **offsets**: Three values in X/Y/Z order used to decode
      stored integer coordinates:

      `coordinate = stored_integer * scale + offset`

    - **columns**: Stored public column names mapped to their NumPy-compatible
      dtypes. `X`, `Y`, and `Z` are encoded integers; `classification` contains
      ASPRS classification codes. Other columns, such as `intensity`, are
      source-dependent.
    - **tiles**: Occupied tiles only. Empty positions in the tiling are omitted.
      Each entry contains its integer `tile_x` and `tile_y`, horizontal
      `bounds`, and `points_by_lod`.

    `points_by_lod[k]` is the number of rows returned by `lod=k` before an
    optional classification filter. Counts are cumulative: LOD 0 is the
    coarsest sample, each higher value includes every preceding level, and the
    final value is the complete tile. A sparse boundary tile may legitimately
    repeat counts across several LODs when it contains too few points to
    populate every level.

    Internal GCS object names, Parquet part paths, row-group offsets, and byte
    ranges are deliberately not part of the API response. The server uses that
    storage index to satisfy tile requests; clients only need this stable tile
    catalogue.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **422 Unprocessable Entity**: The point cloud is not completed, its
      resource metadata does not match its stored data, or the stored Parquet
      index is missing or malformed. Re-create the point cloud before retrying.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudDataMetadata]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PointCloudDataMetadata | None:
    """Get point-cloud tile metadata

     # Get Point-Cloud Data Metadata

    Returns the public read index for a completed point cloud without returning
    any point values. Call this endpoint first to discover the occupied tiles,
    stored columns and dtypes, coordinate encoding, and the number of points
    each level of detail (LOD) would return.

    A typical client workflow is:

    1. Read this metadata once.
    2. Select one of the entries in `tiles`.
    3. Choose an LOD whose cumulative point count fits the client workload.
    4. Request that tile from the JSON or binary data endpoint.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    - **tile_m**: Width and height of each tile in the units of `crs`.
    - **lod_levels**: Number of available cumulative LOD selections. The
      current format has six levels, numbered `0` through `5`.
    - **crs**: Coordinate reference system for the decoded point coordinates
      and all reported bounds.
    - **bounds**: Horizontal point-cloud extent as
      `[min_x, min_y, max_x, max_y]`.
    - **scales** and **offsets**: Three values in X/Y/Z order used to decode
      stored integer coordinates:

      `coordinate = stored_integer * scale + offset`

    - **columns**: Stored public column names mapped to their NumPy-compatible
      dtypes. `X`, `Y`, and `Z` are encoded integers; `classification` contains
      ASPRS classification codes. Other columns, such as `intensity`, are
      source-dependent.
    - **tiles**: Occupied tiles only. Empty positions in the tiling are omitted.
      Each entry contains its integer `tile_x` and `tile_y`, horizontal
      `bounds`, and `points_by_lod`.

    `points_by_lod[k]` is the number of rows returned by `lod=k` before an
    optional classification filter. Counts are cumulative: LOD 0 is the
    coarsest sample, each higher value includes every preceding level, and the
    final value is the complete tile. A sparse boundary tile may legitimately
    repeat counts across several LODs when it contains too few points to
    populate every level.

    Internal GCS object names, Parquet part paths, row-group offsets, and byte
    ranges are deliberately not part of the API response. The server uses that
    storage index to satisfy tile requests; clients only need this stable tile
    catalogue.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **422 Unprocessable Entity**: The point cloud is not completed, its
      resource metadata does not match its stored data, or the stored Parquet
      index is missing or malformed. Re-create the point cloud before retrying.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudDataMetadata
    """

    return sync_detailed(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | PointCloudDataMetadata]:
    """Get point-cloud tile metadata

     # Get Point-Cloud Data Metadata

    Returns the public read index for a completed point cloud without returning
    any point values. Call this endpoint first to discover the occupied tiles,
    stored columns and dtypes, coordinate encoding, and the number of points
    each level of detail (LOD) would return.

    A typical client workflow is:

    1. Read this metadata once.
    2. Select one of the entries in `tiles`.
    3. Choose an LOD whose cumulative point count fits the client workload.
    4. Request that tile from the JSON or binary data endpoint.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    - **tile_m**: Width and height of each tile in the units of `crs`.
    - **lod_levels**: Number of available cumulative LOD selections. The
      current format has six levels, numbered `0` through `5`.
    - **crs**: Coordinate reference system for the decoded point coordinates
      and all reported bounds.
    - **bounds**: Horizontal point-cloud extent as
      `[min_x, min_y, max_x, max_y]`.
    - **scales** and **offsets**: Three values in X/Y/Z order used to decode
      stored integer coordinates:

      `coordinate = stored_integer * scale + offset`

    - **columns**: Stored public column names mapped to their NumPy-compatible
      dtypes. `X`, `Y`, and `Z` are encoded integers; `classification` contains
      ASPRS classification codes. Other columns, such as `intensity`, are
      source-dependent.
    - **tiles**: Occupied tiles only. Empty positions in the tiling are omitted.
      Each entry contains its integer `tile_x` and `tile_y`, horizontal
      `bounds`, and `points_by_lod`.

    `points_by_lod[k]` is the number of rows returned by `lod=k` before an
    optional classification filter. Counts are cumulative: LOD 0 is the
    coarsest sample, each higher value includes every preceding level, and the
    final value is the complete tile. A sparse boundary tile may legitimately
    repeat counts across several LODs when it contains too few points to
    populate every level.

    Internal GCS object names, Parquet part paths, row-group offsets, and byte
    ranges are deliberately not part of the API response. The server uses that
    storage index to satisfy tile requests; clients only need this stable tile
    catalogue.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **422 Unprocessable Entity**: The point cloud is not completed, its
      resource metadata does not match its stored data, or the stored Parquet
      index is missing or malformed. Re-create the point cloud before retrying.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudDataMetadata]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    point_cloud_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PointCloudDataMetadata | None:
    """Get point-cloud tile metadata

     # Get Point-Cloud Data Metadata

    Returns the public read index for a completed point cloud without returning
    any point values. Call this endpoint first to discover the occupied tiles,
    stored columns and dtypes, coordinate encoding, and the number of points
    each level of detail (LOD) would return.

    A typical client workflow is:

    1. Read this metadata once.
    2. Select one of the entries in `tiles`.
    3. Choose an LOD whose cumulative point count fits the client workload.
    4. Request that tile from the JSON or binary data endpoint.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.

    ## Response

    - **tile_m**: Width and height of each tile in the units of `crs`.
    - **lod_levels**: Number of available cumulative LOD selections. The
      current format has six levels, numbered `0` through `5`.
    - **crs**: Coordinate reference system for the decoded point coordinates
      and all reported bounds.
    - **bounds**: Horizontal point-cloud extent as
      `[min_x, min_y, max_x, max_y]`.
    - **scales** and **offsets**: Three values in X/Y/Z order used to decode
      stored integer coordinates:

      `coordinate = stored_integer * scale + offset`

    - **columns**: Stored public column names mapped to their NumPy-compatible
      dtypes. `X`, `Y`, and `Z` are encoded integers; `classification` contains
      ASPRS classification codes. Other columns, such as `intensity`, are
      source-dependent.
    - **tiles**: Occupied tiles only. Empty positions in the tiling are omitted.
      Each entry contains its integer `tile_x` and `tile_y`, horizontal
      `bounds`, and `points_by_lod`.

    `points_by_lod[k]` is the number of rows returned by `lod=k` before an
    optional classification filter. Counts are cumulative: LOD 0 is the
    coarsest sample, each higher value includes every preceding level, and the
    final value is the complete tile. A sparse boundary tile may legitimately
    repeat counts across several LODs when it contains too few points to
    populate every level.

    Internal GCS object names, Parquet part paths, row-group offsets, and byte
    ranges are deliberately not part of the API response. The server uses that
    storage index to satisfy tile requests; clients only need this stable tile
    catalogue.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **422 Unprocessable Entity**: The point cloud is not completed, its
      resource metadata does not match its stored data, or the stored Parquet
      index is missing or malformed. Re-create the point cloud before retrying.

    Args:
        domain_id (str):
        point_cloud_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudDataMetadata
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            point_cloud_id=point_cloud_id,
            client=client,
        )
    ).parsed
