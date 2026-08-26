from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.point_cloud_tile_data_response import PointCloudTileDataResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    point_cloud_id: str,
    tile_x: int,
    tile_y: int,
    *,
    lod: int | None | Unset = UNSET,
    classes: None | str | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_lod: int | None | Unset
    if isinstance(lod, Unset):
        json_lod = UNSET
    else:
        json_lod = lod
    params["lod"] = json_lod

    json_classes: None | str | Unset
    if isinstance(classes, Unset):
        json_classes = UNSET
    else:
        json_classes = classes
    params["classes"] = json_classes

    json_columns: None | str | Unset
    if isinstance(columns, Unset):
        json_columns = UNSET
    else:
        json_columns = columns
    params["columns"] = json_columns

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/pointclouds/{point_cloud_id}/data/{tile_x}/{tile_y}".format(
            domain_id=quote(str(domain_id), safe=""),
            point_cloud_id=quote(str(point_cloud_id), safe=""),
            tile_x=quote(str(tile_x), safe=""),
            tile_y=quote(str(tile_y), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PointCloudTileDataResponse | None:
    if response.status_code == 200:
        response_200 = PointCloudTileDataResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PointCloudTileDataResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    point_cloud_id: str,
    tile_x: int,
    tile_y: int,
    *,
    client: AuthenticatedClient,
    lod: int | None | Unset = UNSET,
    classes: None | str | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PointCloudTileDataResponse]:
    r"""Get point-cloud tile data (JSON)

     # Get Point-Cloud Tile Data as JSON

    Returns selected columns from one occupied point-cloud tile as columnar
    JSON. Use this representation for inspection, small previews, and clients
    that do not need the more compact binary response.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first. Its `tiles` array supplies valid tile coordinates and exact
    cumulative point counts, while its `columns` object supplies the available
    names and dtypes.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response. They are indices in the point cloud's own tiling,
      not projected map coordinates.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile. Valid values are `0` through `lod_levels - 1` from the metadata
      response.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Duplicate values are ignored. Omit it to retain
      every classification.
    - **columns**: Optional comma-separated column projection in the desired
      response order, for example `?columns=X,Y,Z`. Omit it to return all
      public stored columns.

    ## Response

    The response is columnar: arrays in `data` have equal length and values at
    the same array index describe the same point.

    For example, this is the complete response for tile `(-1, 0)` from the
    `static-test-blackfoot-3dep` point cloud with
    `?lod=5&classes=1,2&columns=X,Y,Z,classification`:

    ```json
    {
      \"tile_x\": -1,
      \"tile_y\": 0,
      \"bounds\": [
        293711.08485993545,
        5198981.669894749,
        294094.99218481116,
        5199365.577219625
      ],
      \"lod\": 5,
      \"classes\": [1, 2],
      \"scales\": [0.001, 0.001, 0.001],
      \"offsets\": [294094.0, 5198981.0, 0.0],
      \"columns\": {
        \"X\": \"int32\",
        \"Y\": \"int32\",
        \"Z\": \"int32\",
        \"classification\": \"uint8\"
      },
      \"data\": {
        \"X\": [992, 992],
        \"Y\": [346497, 64586],
        \"Z\": [1077190, 1051360],
        \"classification\": [1, 2]
      }
    }
    ```

    `X`, `Y`, and `Z` remain stored integers so the response is exact and does
    not expand them to float64. Decode coordinate axis `i` with:

    `coordinate = stored_integer * scales[i] + offsets[i]`

    The echoed `lod`, `classes`, `columns`, and tile bounds make the response
    self-describing. When `classes` was omitted, the response field is `null`.

    JSON responses are capped at 1,000,000 numeric values, calculated as rows
    multiplied by selected columns. If a request is too large, lower `lod`,
    select fewer classes or columns, or use the `/binary` endpoint.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected rows and columns exceed the JSON
      response limit.
    - **422 Unprocessable Entity**: The cloud is not completed; the tile, LOD,
      class, or column selection is invalid; or stored data is unreadable or
      inconsistent with its index.

    Args:
        domain_id (str):
        point_cloud_id (str):
        tile_x (int): Horizontal tile index from `GET /data/metadata`.
        tile_y (int): Vertical tile index from `GET /data/metadata`.
        lod (int | None | Unset): Inclusive LOD ceiling. Omit to read the complete tile. Valid
            values are `0` through `lod_levels - 1` from `/data/metadata`.
        classes (None | str | Unset): Comma-separated ASPRS classification codes to retain, such
            as `2,5`. Omit to retain every class.
        columns (None | str | Unset): Comma-separated stored columns to return, such as `X,Y,Z`.
            Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudTileDataResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
        tile_x=tile_x,
        tile_y=tile_y,
        lod=lod,
        classes=classes,
        columns=columns,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    point_cloud_id: str,
    tile_x: int,
    tile_y: int,
    *,
    client: AuthenticatedClient,
    lod: int | None | Unset = UNSET,
    classes: None | str | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> HTTPValidationError | PointCloudTileDataResponse | None:
    r"""Get point-cloud tile data (JSON)

     # Get Point-Cloud Tile Data as JSON

    Returns selected columns from one occupied point-cloud tile as columnar
    JSON. Use this representation for inspection, small previews, and clients
    that do not need the more compact binary response.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first. Its `tiles` array supplies valid tile coordinates and exact
    cumulative point counts, while its `columns` object supplies the available
    names and dtypes.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response. They are indices in the point cloud's own tiling,
      not projected map coordinates.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile. Valid values are `0` through `lod_levels - 1` from the metadata
      response.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Duplicate values are ignored. Omit it to retain
      every classification.
    - **columns**: Optional comma-separated column projection in the desired
      response order, for example `?columns=X,Y,Z`. Omit it to return all
      public stored columns.

    ## Response

    The response is columnar: arrays in `data` have equal length and values at
    the same array index describe the same point.

    For example, this is the complete response for tile `(-1, 0)` from the
    `static-test-blackfoot-3dep` point cloud with
    `?lod=5&classes=1,2&columns=X,Y,Z,classification`:

    ```json
    {
      \"tile_x\": -1,
      \"tile_y\": 0,
      \"bounds\": [
        293711.08485993545,
        5198981.669894749,
        294094.99218481116,
        5199365.577219625
      ],
      \"lod\": 5,
      \"classes\": [1, 2],
      \"scales\": [0.001, 0.001, 0.001],
      \"offsets\": [294094.0, 5198981.0, 0.0],
      \"columns\": {
        \"X\": \"int32\",
        \"Y\": \"int32\",
        \"Z\": \"int32\",
        \"classification\": \"uint8\"
      },
      \"data\": {
        \"X\": [992, 992],
        \"Y\": [346497, 64586],
        \"Z\": [1077190, 1051360],
        \"classification\": [1, 2]
      }
    }
    ```

    `X`, `Y`, and `Z` remain stored integers so the response is exact and does
    not expand them to float64. Decode coordinate axis `i` with:

    `coordinate = stored_integer * scales[i] + offsets[i]`

    The echoed `lod`, `classes`, `columns`, and tile bounds make the response
    self-describing. When `classes` was omitted, the response field is `null`.

    JSON responses are capped at 1,000,000 numeric values, calculated as rows
    multiplied by selected columns. If a request is too large, lower `lod`,
    select fewer classes or columns, or use the `/binary` endpoint.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected rows and columns exceed the JSON
      response limit.
    - **422 Unprocessable Entity**: The cloud is not completed; the tile, LOD,
      class, or column selection is invalid; or stored data is unreadable or
      inconsistent with its index.

    Args:
        domain_id (str):
        point_cloud_id (str):
        tile_x (int): Horizontal tile index from `GET /data/metadata`.
        tile_y (int): Vertical tile index from `GET /data/metadata`.
        lod (int | None | Unset): Inclusive LOD ceiling. Omit to read the complete tile. Valid
            values are `0` through `lod_levels - 1` from `/data/metadata`.
        classes (None | str | Unset): Comma-separated ASPRS classification codes to retain, such
            as `2,5`. Omit to retain every class.
        columns (None | str | Unset): Comma-separated stored columns to return, such as `X,Y,Z`.
            Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudTileDataResponse
    """

    return sync_detailed(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
        tile_x=tile_x,
        tile_y=tile_y,
        client=client,
        lod=lod,
        classes=classes,
        columns=columns,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    point_cloud_id: str,
    tile_x: int,
    tile_y: int,
    *,
    client: AuthenticatedClient,
    lod: int | None | Unset = UNSET,
    classes: None | str | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PointCloudTileDataResponse]:
    r"""Get point-cloud tile data (JSON)

     # Get Point-Cloud Tile Data as JSON

    Returns selected columns from one occupied point-cloud tile as columnar
    JSON. Use this representation for inspection, small previews, and clients
    that do not need the more compact binary response.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first. Its `tiles` array supplies valid tile coordinates and exact
    cumulative point counts, while its `columns` object supplies the available
    names and dtypes.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response. They are indices in the point cloud's own tiling,
      not projected map coordinates.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile. Valid values are `0` through `lod_levels - 1` from the metadata
      response.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Duplicate values are ignored. Omit it to retain
      every classification.
    - **columns**: Optional comma-separated column projection in the desired
      response order, for example `?columns=X,Y,Z`. Omit it to return all
      public stored columns.

    ## Response

    The response is columnar: arrays in `data` have equal length and values at
    the same array index describe the same point.

    For example, this is the complete response for tile `(-1, 0)` from the
    `static-test-blackfoot-3dep` point cloud with
    `?lod=5&classes=1,2&columns=X,Y,Z,classification`:

    ```json
    {
      \"tile_x\": -1,
      \"tile_y\": 0,
      \"bounds\": [
        293711.08485993545,
        5198981.669894749,
        294094.99218481116,
        5199365.577219625
      ],
      \"lod\": 5,
      \"classes\": [1, 2],
      \"scales\": [0.001, 0.001, 0.001],
      \"offsets\": [294094.0, 5198981.0, 0.0],
      \"columns\": {
        \"X\": \"int32\",
        \"Y\": \"int32\",
        \"Z\": \"int32\",
        \"classification\": \"uint8\"
      },
      \"data\": {
        \"X\": [992, 992],
        \"Y\": [346497, 64586],
        \"Z\": [1077190, 1051360],
        \"classification\": [1, 2]
      }
    }
    ```

    `X`, `Y`, and `Z` remain stored integers so the response is exact and does
    not expand them to float64. Decode coordinate axis `i` with:

    `coordinate = stored_integer * scales[i] + offsets[i]`

    The echoed `lod`, `classes`, `columns`, and tile bounds make the response
    self-describing. When `classes` was omitted, the response field is `null`.

    JSON responses are capped at 1,000,000 numeric values, calculated as rows
    multiplied by selected columns. If a request is too large, lower `lod`,
    select fewer classes or columns, or use the `/binary` endpoint.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected rows and columns exceed the JSON
      response limit.
    - **422 Unprocessable Entity**: The cloud is not completed; the tile, LOD,
      class, or column selection is invalid; or stored data is unreadable or
      inconsistent with its index.

    Args:
        domain_id (str):
        point_cloud_id (str):
        tile_x (int): Horizontal tile index from `GET /data/metadata`.
        tile_y (int): Vertical tile index from `GET /data/metadata`.
        lod (int | None | Unset): Inclusive LOD ceiling. Omit to read the complete tile. Valid
            values are `0` through `lod_levels - 1` from `/data/metadata`.
        classes (None | str | Unset): Comma-separated ASPRS classification codes to retain, such
            as `2,5`. Omit to retain every class.
        columns (None | str | Unset): Comma-separated stored columns to return, such as `X,Y,Z`.
            Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PointCloudTileDataResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        point_cloud_id=point_cloud_id,
        tile_x=tile_x,
        tile_y=tile_y,
        lod=lod,
        classes=classes,
        columns=columns,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    point_cloud_id: str,
    tile_x: int,
    tile_y: int,
    *,
    client: AuthenticatedClient,
    lod: int | None | Unset = UNSET,
    classes: None | str | Unset = UNSET,
    columns: None | str | Unset = UNSET,
) -> HTTPValidationError | PointCloudTileDataResponse | None:
    r"""Get point-cloud tile data (JSON)

     # Get Point-Cloud Tile Data as JSON

    Returns selected columns from one occupied point-cloud tile as columnar
    JSON. Use this representation for inspection, small previews, and clients
    that do not need the more compact binary response.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first. Its `tiles` array supplies valid tile coordinates and exact
    cumulative point counts, while its `columns` object supplies the available
    names and dtypes.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response. They are indices in the point cloud's own tiling,
      not projected map coordinates.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile. Valid values are `0` through `lod_levels - 1` from the metadata
      response.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Duplicate values are ignored. Omit it to retain
      every classification.
    - **columns**: Optional comma-separated column projection in the desired
      response order, for example `?columns=X,Y,Z`. Omit it to return all
      public stored columns.

    ## Response

    The response is columnar: arrays in `data` have equal length and values at
    the same array index describe the same point.

    For example, this is the complete response for tile `(-1, 0)` from the
    `static-test-blackfoot-3dep` point cloud with
    `?lod=5&classes=1,2&columns=X,Y,Z,classification`:

    ```json
    {
      \"tile_x\": -1,
      \"tile_y\": 0,
      \"bounds\": [
        293711.08485993545,
        5198981.669894749,
        294094.99218481116,
        5199365.577219625
      ],
      \"lod\": 5,
      \"classes\": [1, 2],
      \"scales\": [0.001, 0.001, 0.001],
      \"offsets\": [294094.0, 5198981.0, 0.0],
      \"columns\": {
        \"X\": \"int32\",
        \"Y\": \"int32\",
        \"Z\": \"int32\",
        \"classification\": \"uint8\"
      },
      \"data\": {
        \"X\": [992, 992],
        \"Y\": [346497, 64586],
        \"Z\": [1077190, 1051360],
        \"classification\": [1, 2]
      }
    }
    ```

    `X`, `Y`, and `Z` remain stored integers so the response is exact and does
    not expand them to float64. Decode coordinate axis `i` with:

    `coordinate = stored_integer * scales[i] + offsets[i]`

    The echoed `lod`, `classes`, `columns`, and tile bounds make the response
    self-describing. When `classes` was omitted, the response field is `null`.

    JSON responses are capped at 1,000,000 numeric values, calculated as rows
    multiplied by selected columns. If a request is too large, lower `lod`,
    select fewer classes or columns, or use the `/binary` endpoint.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected rows and columns exceed the JSON
      response limit.
    - **422 Unprocessable Entity**: The cloud is not completed; the tile, LOD,
      class, or column selection is invalid; or stored data is unreadable or
      inconsistent with its index.

    Args:
        domain_id (str):
        point_cloud_id (str):
        tile_x (int): Horizontal tile index from `GET /data/metadata`.
        tile_y (int): Vertical tile index from `GET /data/metadata`.
        lod (int | None | Unset): Inclusive LOD ceiling. Omit to read the complete tile. Valid
            values are `0` through `lod_levels - 1` from `/data/metadata`.
        classes (None | str | Unset): Comma-separated ASPRS classification codes to retain, such
            as `2,5`. Omit to retain every class.
        columns (None | str | Unset): Comma-separated stored columns to return, such as `X,Y,Z`.
            Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PointCloudTileDataResponse
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            point_cloud_id=point_cloud_id,
            tile_x=tile_x,
            tile_y=tile_y,
            client=client,
            lod=lod,
            classes=classes,
            columns=columns,
        )
    ).parsed
