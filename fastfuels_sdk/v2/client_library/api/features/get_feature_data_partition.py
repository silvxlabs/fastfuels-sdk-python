from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    feature_id: str,
    partition_index: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/features/{feature_id}/data/{partition_index}".format(
            domain_id=quote(str(domain_id), safe=""),
            feature_id=quote(str(feature_id), safe=""),
            partition_index=quote(str(partition_index), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    feature_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Get one partition of feature data as GeoJSON

     # Get Feature Data Partition

    Returns one partition of a completed feature's data as a self-contained
    GeoJSON `FeatureCollection`. To stream the full collection, first call
    `GET /domains/{domain_id}/features/{feature_id}/data/metadata` to
    discover `partition_count`, then GET this endpoint for each
    `partition_index` from `0` to `partition_count - 1`. The concatenated
    `features` arrays reproduce the source feature list in source order.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.
    - **partition_index**: Zero-indexed partition number. Must be `< partition_count`
      from `/data/metadata`.

    ## Response

    `application/geo+json` body — a valid GeoJSON `FeatureCollection`
    containing up to `partition_size` features. Each feature's `properties`
    and `geometry` round-trip from the source GeoParquet via geopandas.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **413 Content Too Large**: Serialized partition exceeds the 30 MB
      response cap. Partition size is fixed server-side and cannot be
      adjusted by re-creating the feature; contact
      `support.fastfuels@silvxlabs.com` so the partition size can be
      reduced for your feature.
    - **422 Unprocessable Entity**: `partition_index` is past the last
      partition, the feature is not in `completed` status, or the
      underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):
        partition_index (int): Zero-indexed partition number. Valid range is `0` ≤
            `partition_index` < `partition_count` from `GET /data/metadata`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        feature_id=feature_id,
        partition_index=partition_index,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    feature_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Get one partition of feature data as GeoJSON

     # Get Feature Data Partition

    Returns one partition of a completed feature's data as a self-contained
    GeoJSON `FeatureCollection`. To stream the full collection, first call
    `GET /domains/{domain_id}/features/{feature_id}/data/metadata` to
    discover `partition_count`, then GET this endpoint for each
    `partition_index` from `0` to `partition_count - 1`. The concatenated
    `features` arrays reproduce the source feature list in source order.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.
    - **partition_index**: Zero-indexed partition number. Must be `< partition_count`
      from `/data/metadata`.

    ## Response

    `application/geo+json` body — a valid GeoJSON `FeatureCollection`
    containing up to `partition_size` features. Each feature's `properties`
    and `geometry` round-trip from the source GeoParquet via geopandas.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **413 Content Too Large**: Serialized partition exceeds the 30 MB
      response cap. Partition size is fixed server-side and cannot be
      adjusted by re-creating the feature; contact
      `support.fastfuels@silvxlabs.com` so the partition size can be
      reduced for your feature.
    - **422 Unprocessable Entity**: `partition_index` is past the last
      partition, the feature is not in `completed` status, or the
      underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):
        partition_index (int): Zero-indexed partition number. Valid range is `0` ≤
            `partition_index` < `partition_count` from `GET /data/metadata`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        feature_id=feature_id,
        partition_index=partition_index,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    feature_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Get one partition of feature data as GeoJSON

     # Get Feature Data Partition

    Returns one partition of a completed feature's data as a self-contained
    GeoJSON `FeatureCollection`. To stream the full collection, first call
    `GET /domains/{domain_id}/features/{feature_id}/data/metadata` to
    discover `partition_count`, then GET this endpoint for each
    `partition_index` from `0` to `partition_count - 1`. The concatenated
    `features` arrays reproduce the source feature list in source order.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.
    - **partition_index**: Zero-indexed partition number. Must be `< partition_count`
      from `/data/metadata`.

    ## Response

    `application/geo+json` body — a valid GeoJSON `FeatureCollection`
    containing up to `partition_size` features. Each feature's `properties`
    and `geometry` round-trip from the source GeoParquet via geopandas.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **413 Content Too Large**: Serialized partition exceeds the 30 MB
      response cap. Partition size is fixed server-side and cannot be
      adjusted by re-creating the feature; contact
      `support.fastfuels@silvxlabs.com` so the partition size can be
      reduced for your feature.
    - **422 Unprocessable Entity**: `partition_index` is past the last
      partition, the feature is not in `completed` status, or the
      underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):
        partition_index (int): Zero-indexed partition number. Valid range is `0` ≤
            `partition_index` < `partition_count` from `GET /data/metadata`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        feature_id=feature_id,
        partition_index=partition_index,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    feature_id: str,
    partition_index: int,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Get one partition of feature data as GeoJSON

     # Get Feature Data Partition

    Returns one partition of a completed feature's data as a self-contained
    GeoJSON `FeatureCollection`. To stream the full collection, first call
    `GET /domains/{domain_id}/features/{feature_id}/data/metadata` to
    discover `partition_count`, then GET this endpoint for each
    `partition_index` from `0` to `partition_count - 1`. The concatenated
    `features` arrays reproduce the source feature list in source order.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.
    - **partition_index**: Zero-indexed partition number. Must be `< partition_count`
      from `/data/metadata`.

    ## Response

    `application/geo+json` body — a valid GeoJSON `FeatureCollection`
    containing up to `partition_size` features. Each feature's `properties`
    and `geometry` round-trip from the source GeoParquet via geopandas.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **413 Content Too Large**: Serialized partition exceeds the 30 MB
      response cap. Partition size is fixed server-side and cannot be
      adjusted by re-creating the feature; contact
      `support.fastfuels@silvxlabs.com` so the partition size can be
      reduced for your feature.
    - **422 Unprocessable Entity**: `partition_index` is past the last
      partition, the feature is not in `completed` status, or the
      underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):
        partition_index (int): Zero-indexed partition number. Valid range is `0` ≤
            `partition_index` < `partition_count` from `GET /data/metadata`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            feature_id=feature_id,
            partition_index=partition_index,
            client=client,
        )
    ).parsed
