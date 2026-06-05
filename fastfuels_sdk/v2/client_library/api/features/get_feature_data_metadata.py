from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feature_data_metadata import FeatureDataMetadata
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    feature_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/features/{feature_id}/data/metadata".format(
            domain_id=quote(str(domain_id), safe=""),
            feature_id=quote(str(feature_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FeatureDataMetadata | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = FeatureDataMetadata.from_dict(response.json())

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
) -> Response[FeatureDataMetadata | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[FeatureDataMetadata | HTTPValidationError]:
    r"""Get feature data partition layout

     # Get Feature Data Metadata

    Returns the partition layout for a completed feature's data blob. Use
    this to discover how many partitions exist before streaming them via
    `GET /domains/{domain_id}/features/{feature_id}/data/{partition_index}`.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.

    ## Response

    JSON object describing the partition layout of the underlying
    GeoParquet blob:

    ```json
    {
      \"total_features\": 5400,
      \"partition_count\": 6,
      \"partitions\": [
        {\"index\": 0, \"num_features\": 1000},
        {\"index\": 1, \"num_features\": 1000},
        {\"index\": 2, \"num_features\": 1000},
        {\"index\": 3, \"num_features\": 1000},
        {\"index\": 4, \"num_features\": 1000},
        {\"index\": 5, \"num_features\": 400}
      ]
    }
    ```

    - **total_features**: Total number of features across all partitions.
    - **partition_count**: Number of valid `partition_index` values. Iterate
      from `0` to `partition_count - 1` to retrieve every feature exactly
      once, in source order.
    - **partitions**: Per-partition row counts read directly from the
      GeoParquet footer. Sum of `num_features` equals `total_features`.

    A feature with zero features has `partition_count = 0` and an empty
    `partitions` list — no `/data/{partition_index}` calls are valid in
    that case.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **422 Unprocessable Entity**: Feature is not in `completed` status, or
      the underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FeatureDataMetadata | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        feature_id=feature_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
) -> FeatureDataMetadata | HTTPValidationError | None:
    r"""Get feature data partition layout

     # Get Feature Data Metadata

    Returns the partition layout for a completed feature's data blob. Use
    this to discover how many partitions exist before streaming them via
    `GET /domains/{domain_id}/features/{feature_id}/data/{partition_index}`.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.

    ## Response

    JSON object describing the partition layout of the underlying
    GeoParquet blob:

    ```json
    {
      \"total_features\": 5400,
      \"partition_count\": 6,
      \"partitions\": [
        {\"index\": 0, \"num_features\": 1000},
        {\"index\": 1, \"num_features\": 1000},
        {\"index\": 2, \"num_features\": 1000},
        {\"index\": 3, \"num_features\": 1000},
        {\"index\": 4, \"num_features\": 1000},
        {\"index\": 5, \"num_features\": 400}
      ]
    }
    ```

    - **total_features**: Total number of features across all partitions.
    - **partition_count**: Number of valid `partition_index` values. Iterate
      from `0` to `partition_count - 1` to retrieve every feature exactly
      once, in source order.
    - **partitions**: Per-partition row counts read directly from the
      GeoParquet footer. Sum of `num_features` equals `total_features`.

    A feature with zero features has `partition_count = 0` and an empty
    `partitions` list — no `/data/{partition_index}` calls are valid in
    that case.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **422 Unprocessable Entity**: Feature is not in `completed` status, or
      the underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FeatureDataMetadata | HTTPValidationError
    """

    return sync_detailed(
        domain_id=domain_id,
        feature_id=feature_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[FeatureDataMetadata | HTTPValidationError]:
    r"""Get feature data partition layout

     # Get Feature Data Metadata

    Returns the partition layout for a completed feature's data blob. Use
    this to discover how many partitions exist before streaming them via
    `GET /domains/{domain_id}/features/{feature_id}/data/{partition_index}`.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.

    ## Response

    JSON object describing the partition layout of the underlying
    GeoParquet blob:

    ```json
    {
      \"total_features\": 5400,
      \"partition_count\": 6,
      \"partitions\": [
        {\"index\": 0, \"num_features\": 1000},
        {\"index\": 1, \"num_features\": 1000},
        {\"index\": 2, \"num_features\": 1000},
        {\"index\": 3, \"num_features\": 1000},
        {\"index\": 4, \"num_features\": 1000},
        {\"index\": 5, \"num_features\": 400}
      ]
    }
    ```

    - **total_features**: Total number of features across all partitions.
    - **partition_count**: Number of valid `partition_index` values. Iterate
      from `0` to `partition_count - 1` to retrieve every feature exactly
      once, in source order.
    - **partitions**: Per-partition row counts read directly from the
      GeoParquet footer. Sum of `num_features` equals `total_features`.

    A feature with zero features has `partition_count = 0` and an empty
    `partitions` list — no `/data/{partition_index}` calls are valid in
    that case.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **422 Unprocessable Entity**: Feature is not in `completed` status, or
      the underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FeatureDataMetadata | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        feature_id=feature_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    feature_id: str,
    *,
    client: AuthenticatedClient,
) -> FeatureDataMetadata | HTTPValidationError | None:
    r"""Get feature data partition layout

     # Get Feature Data Metadata

    Returns the partition layout for a completed feature's data blob. Use
    this to discover how many partitions exist before streaming them via
    `GET /domains/{domain_id}/features/{feature_id}/data/{partition_index}`.

    ## Path Parameters

    - **domain_id**: The domain the feature belongs to.
    - **feature_id**: The unique identifier of the feature.

    ## Response

    JSON object describing the partition layout of the underlying
    GeoParquet blob:

    ```json
    {
      \"total_features\": 5400,
      \"partition_count\": 6,
      \"partitions\": [
        {\"index\": 0, \"num_features\": 1000},
        {\"index\": 1, \"num_features\": 1000},
        {\"index\": 2, \"num_features\": 1000},
        {\"index\": 3, \"num_features\": 1000},
        {\"index\": 4, \"num_features\": 1000},
        {\"index\": 5, \"num_features\": 400}
      ]
    }
    ```

    - **total_features**: Total number of features across all partitions.
    - **partition_count**: Number of valid `partition_index` values. Iterate
      from `0` to `partition_count - 1` to retrieve every feature exactly
      once, in source order.
    - **partitions**: Per-partition row counts read directly from the
      GeoParquet footer. Sum of `num_features` equals `total_features`.

    A feature with zero features has `partition_count = 0` and an empty
    `partitions` list — no `/data/{partition_index}` calls are valid in
    that case.

    ## Error Responses

    - **404 Not Found**: Feature does not exist or is not accessible to the
      caller.
    - **422 Unprocessable Entity**: Feature is not in `completed` status, or
      the underlying GeoParquet blob is missing / malformed.

    Args:
        domain_id (str):
        feature_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FeatureDataMetadata | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            feature_id=feature_id,
            client=client,
        )
    ).parsed
