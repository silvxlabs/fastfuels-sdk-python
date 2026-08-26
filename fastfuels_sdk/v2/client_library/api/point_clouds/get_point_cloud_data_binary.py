from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
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
        "url": "/domains/{domain_id}/pointclouds/{point_cloud_id}/data/{tile_x}/{tile_y}/binary".format(
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
) -> HTTPValidationError | str | None:
    if response.status_code == 200:
        response_200 = cast(str, response.content)
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
) -> Response[HTTPValidationError | str]:
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
) -> Response[HTTPValidationError | str]:
    """Get point-cloud tile data (binary)

     # Get Point-Cloud Tile Data as Binary

    Returns selected columns from one occupied point-cloud tile as raw
    little-endian typed arrays. This is the compact counterpart to the JSON
    endpoint and is intended for clients that can construct NumPy, JavaScript,
    Rust, or C/C++ typed arrays directly from response bytes.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first to discover valid tiles, cumulative LOD costs, available columns, and
    coordinate scaling.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Omit it for all classes.
    - **columns**: Optional comma-separated column projection in the exact
      desired block order, for example `?columns=X,Y,Z`. Omit it for all public
      stored columns.

    ## Response Body

    The body is one contiguous column block after another in `X-Data-Columns`
    order. Every block contains `X-Data-Count` values and uses the corresponding
    dtype in `X-Data-Dtypes`. All multi-byte values are little-endian.

    For example, these headers:

    ```text
    X-Data-Columns: X,Z,classification
    X-Data-Dtypes: int32,int32,uint8
    X-Data-Count: 1000
    ```

    describe `4000` bytes of X values, followed by `4000` bytes of Z values,
    followed by `1000` classification bytes. In general, each block occupies:

    `X-Data-Count * sizeof(corresponding dtype)`

    Slice the body at the cumulative block sizes. Values with the same position
    within each block describe the same point.

    ## Response Headers

    - **X-Data-Columns**: Comma-separated column block order.
    - **X-Data-Dtypes**: Comma-separated NumPy dtype for each column block.
    - **X-Data-Count**: Number of values in every block.
    - **X-Data-Tile**: Requested tile as `tile_x,tile_y`.
    - **X-Data-Bounds**: Horizontal tile bounds as
      `min_x,min_y,max_x,max_y`.
    - **X-Data-LOD**: Inclusive LOD ceiling used for the response.
    - **X-Data-Classes**: Comma-separated selected ASPRS classes, or `all` when
      no class filter was supplied.
    - **X-Data-Scales** and **X-Data-Offsets**: X/Y/Z coordinate encoding.
      Decode coordinate axis `i` with
      `stored_integer * scale[i] + offset[i]`.

    These headers are exposed through CORS, so browser JavaScript can read them.

    Binary responses are capped at 30 MiB. If a request is too large, lower
    `lod` or select fewer classes or columns.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected binary column blocks exceed the
      30 MiB response limit.
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
        columns (None | str | Unset): Comma-separated stored columns in the desired binary block
            order, such as `X,Y,Z`. Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | str]
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
) -> HTTPValidationError | str | None:
    """Get point-cloud tile data (binary)

     # Get Point-Cloud Tile Data as Binary

    Returns selected columns from one occupied point-cloud tile as raw
    little-endian typed arrays. This is the compact counterpart to the JSON
    endpoint and is intended for clients that can construct NumPy, JavaScript,
    Rust, or C/C++ typed arrays directly from response bytes.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first to discover valid tiles, cumulative LOD costs, available columns, and
    coordinate scaling.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Omit it for all classes.
    - **columns**: Optional comma-separated column projection in the exact
      desired block order, for example `?columns=X,Y,Z`. Omit it for all public
      stored columns.

    ## Response Body

    The body is one contiguous column block after another in `X-Data-Columns`
    order. Every block contains `X-Data-Count` values and uses the corresponding
    dtype in `X-Data-Dtypes`. All multi-byte values are little-endian.

    For example, these headers:

    ```text
    X-Data-Columns: X,Z,classification
    X-Data-Dtypes: int32,int32,uint8
    X-Data-Count: 1000
    ```

    describe `4000` bytes of X values, followed by `4000` bytes of Z values,
    followed by `1000` classification bytes. In general, each block occupies:

    `X-Data-Count * sizeof(corresponding dtype)`

    Slice the body at the cumulative block sizes. Values with the same position
    within each block describe the same point.

    ## Response Headers

    - **X-Data-Columns**: Comma-separated column block order.
    - **X-Data-Dtypes**: Comma-separated NumPy dtype for each column block.
    - **X-Data-Count**: Number of values in every block.
    - **X-Data-Tile**: Requested tile as `tile_x,tile_y`.
    - **X-Data-Bounds**: Horizontal tile bounds as
      `min_x,min_y,max_x,max_y`.
    - **X-Data-LOD**: Inclusive LOD ceiling used for the response.
    - **X-Data-Classes**: Comma-separated selected ASPRS classes, or `all` when
      no class filter was supplied.
    - **X-Data-Scales** and **X-Data-Offsets**: X/Y/Z coordinate encoding.
      Decode coordinate axis `i` with
      `stored_integer * scale[i] + offset[i]`.

    These headers are exposed through CORS, so browser JavaScript can read them.

    Binary responses are capped at 30 MiB. If a request is too large, lower
    `lod` or select fewer classes or columns.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected binary column blocks exceed the
      30 MiB response limit.
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
        columns (None | str | Unset): Comma-separated stored columns in the desired binary block
            order, such as `X,Y,Z`. Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | str
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
) -> Response[HTTPValidationError | str]:
    """Get point-cloud tile data (binary)

     # Get Point-Cloud Tile Data as Binary

    Returns selected columns from one occupied point-cloud tile as raw
    little-endian typed arrays. This is the compact counterpart to the JSON
    endpoint and is intended for clients that can construct NumPy, JavaScript,
    Rust, or C/C++ typed arrays directly from response bytes.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first to discover valid tiles, cumulative LOD costs, available columns, and
    coordinate scaling.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Omit it for all classes.
    - **columns**: Optional comma-separated column projection in the exact
      desired block order, for example `?columns=X,Y,Z`. Omit it for all public
      stored columns.

    ## Response Body

    The body is one contiguous column block after another in `X-Data-Columns`
    order. Every block contains `X-Data-Count` values and uses the corresponding
    dtype in `X-Data-Dtypes`. All multi-byte values are little-endian.

    For example, these headers:

    ```text
    X-Data-Columns: X,Z,classification
    X-Data-Dtypes: int32,int32,uint8
    X-Data-Count: 1000
    ```

    describe `4000` bytes of X values, followed by `4000` bytes of Z values,
    followed by `1000` classification bytes. In general, each block occupies:

    `X-Data-Count * sizeof(corresponding dtype)`

    Slice the body at the cumulative block sizes. Values with the same position
    within each block describe the same point.

    ## Response Headers

    - **X-Data-Columns**: Comma-separated column block order.
    - **X-Data-Dtypes**: Comma-separated NumPy dtype for each column block.
    - **X-Data-Count**: Number of values in every block.
    - **X-Data-Tile**: Requested tile as `tile_x,tile_y`.
    - **X-Data-Bounds**: Horizontal tile bounds as
      `min_x,min_y,max_x,max_y`.
    - **X-Data-LOD**: Inclusive LOD ceiling used for the response.
    - **X-Data-Classes**: Comma-separated selected ASPRS classes, or `all` when
      no class filter was supplied.
    - **X-Data-Scales** and **X-Data-Offsets**: X/Y/Z coordinate encoding.
      Decode coordinate axis `i` with
      `stored_integer * scale[i] + offset[i]`.

    These headers are exposed through CORS, so browser JavaScript can read them.

    Binary responses are capped at 30 MiB. If a request is too large, lower
    `lod` or select fewer classes or columns.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected binary column blocks exceed the
      30 MiB response limit.
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
        columns (None | str | Unset): Comma-separated stored columns in the desired binary block
            order, such as `X,Y,Z`. Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | str]
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
) -> HTTPValidationError | str | None:
    """Get point-cloud tile data (binary)

     # Get Point-Cloud Tile Data as Binary

    Returns selected columns from one occupied point-cloud tile as raw
    little-endian typed arrays. This is the compact counterpart to the JSON
    endpoint and is intended for clients that can construct NumPy, JavaScript,
    Rust, or C/C++ typed arrays directly from response bytes.

    Call `GET /domains/{domain_id}/pointclouds/{point_cloud_id}/data/metadata`
    first to discover valid tiles, cumulative LOD costs, available columns, and
    coordinate scaling.

    ## Path Parameters

    - **domain_id**: Domain the point cloud belongs to.
    - **point_cloud_id**: Unique point-cloud identifier.
    - **tile_x** and **tile_y**: Integer coordinates of an occupied tile from
      the metadata response.

    ## Query Parameters

    - **lod**: Inclusive LOD ceiling. `lod=0` returns the coarsest sample;
      `lod=k` returns levels `0` through `k`; omitting it returns the complete
      tile.
    - **classes**: Optional comma-separated ASPRS classification filter, for
      example `?classes=2,5`. Omit it for all classes.
    - **columns**: Optional comma-separated column projection in the exact
      desired block order, for example `?columns=X,Y,Z`. Omit it for all public
      stored columns.

    ## Response Body

    The body is one contiguous column block after another in `X-Data-Columns`
    order. Every block contains `X-Data-Count` values and uses the corresponding
    dtype in `X-Data-Dtypes`. All multi-byte values are little-endian.

    For example, these headers:

    ```text
    X-Data-Columns: X,Z,classification
    X-Data-Dtypes: int32,int32,uint8
    X-Data-Count: 1000
    ```

    describe `4000` bytes of X values, followed by `4000` bytes of Z values,
    followed by `1000` classification bytes. In general, each block occupies:

    `X-Data-Count * sizeof(corresponding dtype)`

    Slice the body at the cumulative block sizes. Values with the same position
    within each block describe the same point.

    ## Response Headers

    - **X-Data-Columns**: Comma-separated column block order.
    - **X-Data-Dtypes**: Comma-separated NumPy dtype for each column block.
    - **X-Data-Count**: Number of values in every block.
    - **X-Data-Tile**: Requested tile as `tile_x,tile_y`.
    - **X-Data-Bounds**: Horizontal tile bounds as
      `min_x,min_y,max_x,max_y`.
    - **X-Data-LOD**: Inclusive LOD ceiling used for the response.
    - **X-Data-Classes**: Comma-separated selected ASPRS classes, or `all` when
      no class filter was supplied.
    - **X-Data-Scales** and **X-Data-Offsets**: X/Y/Z coordinate encoding.
      Decode coordinate axis `i` with
      `stored_integer * scale[i] + offset[i]`.

    These headers are exposed through CORS, so browser JavaScript can read them.

    Binary responses are capped at 30 MiB. If a request is too large, lower
    `lod` or select fewer classes or columns.

    ## Error Responses

    - **404 Not Found**: The point cloud does not exist, belongs to another
      domain, or is not accessible to the caller.
    - **413 Content Too Large**: The selected binary column blocks exceed the
      30 MiB response limit.
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
        columns (None | str | Unset): Comma-separated stored columns in the desired binary block
            order, such as `X,Y,Z`. Omit to return every public stored column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | str
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
