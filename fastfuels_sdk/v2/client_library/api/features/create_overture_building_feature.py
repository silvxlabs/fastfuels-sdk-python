from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_overture_building_feature_request import (
    CreateOvertureBuildingFeatureRequest,
)
from ...models.feature import Feature
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateOvertureBuildingFeatureRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/domains/{domain_id}/features/building/overture".format(
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
    body: CreateOvertureBuildingFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a building feature from Overture Maps

     # Create Overture Building Feature

    Creates building footprint polygons for the domain from the
    [Overture Maps](https://overturemaps.org) buildings dataset, which combines
    OpenStreetMap and Microsoft ML Buildings footprints.

    Data comes from the latest Overture release. The release used is recorded
    in `source.release` once the feature completes.

    ## Request Body

    - **name**: (optional) Name for the building feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent before clipping buildings. Range: 0–100. Default: 0.

    ## Response

    Returns the created Feature with status `\"pending\"`; status changes to
    `\"completed\"` when the buildings are ready.

    Each building has:

    - **height**: building height in meters, or null if unknown.
    - **height_source**: dataset that supplied the height, or null.
    - **source_dataset**: dataset that supplied the footprint, e.g.
      `OpenStreetMap` or `Microsoft ML Buildings`.

    The feature's `attributions` list Overture Maps and each upstream dataset
    its buildings came from. The data is licensed under ODbL; reproduce each
    `citation` wherever you use or share it.

    Args:
        domain_id (str):
        body (CreateOvertureBuildingFeatureRequest): Request body for creating a building feature
            via Overture Maps.

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
    body: CreateOvertureBuildingFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a building feature from Overture Maps

     # Create Overture Building Feature

    Creates building footprint polygons for the domain from the
    [Overture Maps](https://overturemaps.org) buildings dataset, which combines
    OpenStreetMap and Microsoft ML Buildings footprints.

    Data comes from the latest Overture release. The release used is recorded
    in `source.release` once the feature completes.

    ## Request Body

    - **name**: (optional) Name for the building feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent before clipping buildings. Range: 0–100. Default: 0.

    ## Response

    Returns the created Feature with status `\"pending\"`; status changes to
    `\"completed\"` when the buildings are ready.

    Each building has:

    - **height**: building height in meters, or null if unknown.
    - **height_source**: dataset that supplied the height, or null.
    - **source_dataset**: dataset that supplied the footprint, e.g.
      `OpenStreetMap` or `Microsoft ML Buildings`.

    The feature's `attributions` list Overture Maps and each upstream dataset
    its buildings came from. The data is licensed under ODbL; reproduce each
    `citation` wherever you use or share it.

    Args:
        domain_id (str):
        body (CreateOvertureBuildingFeatureRequest): Request body for creating a building feature
            via Overture Maps.

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
    body: CreateOvertureBuildingFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a building feature from Overture Maps

     # Create Overture Building Feature

    Creates building footprint polygons for the domain from the
    [Overture Maps](https://overturemaps.org) buildings dataset, which combines
    OpenStreetMap and Microsoft ML Buildings footprints.

    Data comes from the latest Overture release. The release used is recorded
    in `source.release` once the feature completes.

    ## Request Body

    - **name**: (optional) Name for the building feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent before clipping buildings. Range: 0–100. Default: 0.

    ## Response

    Returns the created Feature with status `\"pending\"`; status changes to
    `\"completed\"` when the buildings are ready.

    Each building has:

    - **height**: building height in meters, or null if unknown.
    - **height_source**: dataset that supplied the height, or null.
    - **source_dataset**: dataset that supplied the footprint, e.g.
      `OpenStreetMap` or `Microsoft ML Buildings`.

    The feature's `attributions` list Overture Maps and each upstream dataset
    its buildings came from. The data is licensed under ODbL; reproduce each
    `citation` wherever you use or share it.

    Args:
        domain_id (str):
        body (CreateOvertureBuildingFeatureRequest): Request body for creating a building feature
            via Overture Maps.

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
    body: CreateOvertureBuildingFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a building feature from Overture Maps

     # Create Overture Building Feature

    Creates building footprint polygons for the domain from the
    [Overture Maps](https://overturemaps.org) buildings dataset, which combines
    OpenStreetMap and Microsoft ML Buildings footprints.

    Data comes from the latest Overture release. The release used is recorded
    in `source.release` once the feature completes.

    ## Request Body

    - **name**: (optional) Name for the building feature.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing features.
    - **extent_buffer_m**: (optional) Distance in meters to expand the domain
      extent before clipping buildings. Range: 0–100. Default: 0.

    ## Response

    Returns the created Feature with status `\"pending\"`; status changes to
    `\"completed\"` when the buildings are ready.

    Each building has:

    - **height**: building height in meters, or null if unknown.
    - **height_source**: dataset that supplied the height, or null.
    - **source_dataset**: dataset that supplied the footprint, e.g.
      `OpenStreetMap` or `Microsoft ML Buildings`.

    The feature's `attributions` list Overture Maps and each upstream dataset
    its buildings came from. The data is licensed under ODbL; reproduce each
    `citation` wherever you use or share it.

    Args:
        domain_id (str):
        body (CreateOvertureBuildingFeatureRequest): Request body for creating a building feature
            via Overture Maps.

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
