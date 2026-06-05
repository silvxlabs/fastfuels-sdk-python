from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_domain_request_body import CreateDomainRequestBody
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CreateDomainRequestBody,
    target_epsg: int,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["target_epsg"] = target_epsg

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/reproject",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateDomainRequestBody | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CreateDomainRequestBody.from_dict(response.json())

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
) -> Response[CreateDomainRequestBody | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
    target_epsg: int,
) -> Response[CreateDomainRequestBody | HTTPValidationError]:
    """Reproject a FeatureCollection to a target CRS

     # Reproject Domain Endpoint

    Stateless utility that reprojects a GeoJSON `FeatureCollection` from one
    coordinate reference system to another. No resource is created; the
    reprojected `FeatureCollection` is returned immediately.

    ## Query Parameters

    - **target_epsg**: (integer, required) EPSG code of the target CRS
      (e.g., `4326` for WGS84, `32611` for UTM zone 11N).

    ## Request Body

    A GeoJSON `FeatureCollection`. The source CRS is read from the
    `crs.properties.name` field if present; otherwise EPSG:4326 is assumed.

    ## Response

    Returns the reprojected `FeatureCollection` with:

    - **features**: All input features reprojected to the target CRS, with
      original feature properties preserved.
    - **crs**: Set to the target EPSG code.

    ## Error Responses

    - **422**: Invalid source CRS, invalid target EPSG, or geometry that
      cannot be reprojected.

    Args:
        target_epsg (int): EPSG code of the target CRS.
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDomainRequestBody | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        target_epsg=target_epsg,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
    target_epsg: int,
) -> CreateDomainRequestBody | HTTPValidationError | None:
    """Reproject a FeatureCollection to a target CRS

     # Reproject Domain Endpoint

    Stateless utility that reprojects a GeoJSON `FeatureCollection` from one
    coordinate reference system to another. No resource is created; the
    reprojected `FeatureCollection` is returned immediately.

    ## Query Parameters

    - **target_epsg**: (integer, required) EPSG code of the target CRS
      (e.g., `4326` for WGS84, `32611` for UTM zone 11N).

    ## Request Body

    A GeoJSON `FeatureCollection`. The source CRS is read from the
    `crs.properties.name` field if present; otherwise EPSG:4326 is assumed.

    ## Response

    Returns the reprojected `FeatureCollection` with:

    - **features**: All input features reprojected to the target CRS, with
      original feature properties preserved.
    - **crs**: Set to the target EPSG code.

    ## Error Responses

    - **422**: Invalid source CRS, invalid target EPSG, or geometry that
      cannot be reprojected.

    Args:
        target_epsg (int): EPSG code of the target CRS.
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDomainRequestBody | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        target_epsg=target_epsg,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
    target_epsg: int,
) -> Response[CreateDomainRequestBody | HTTPValidationError]:
    """Reproject a FeatureCollection to a target CRS

     # Reproject Domain Endpoint

    Stateless utility that reprojects a GeoJSON `FeatureCollection` from one
    coordinate reference system to another. No resource is created; the
    reprojected `FeatureCollection` is returned immediately.

    ## Query Parameters

    - **target_epsg**: (integer, required) EPSG code of the target CRS
      (e.g., `4326` for WGS84, `32611` for UTM zone 11N).

    ## Request Body

    A GeoJSON `FeatureCollection`. The source CRS is read from the
    `crs.properties.name` field if present; otherwise EPSG:4326 is assumed.

    ## Response

    Returns the reprojected `FeatureCollection` with:

    - **features**: All input features reprojected to the target CRS, with
      original feature properties preserved.
    - **crs**: Set to the target EPSG code.

    ## Error Responses

    - **422**: Invalid source CRS, invalid target EPSG, or geometry that
      cannot be reprojected.

    Args:
        target_epsg (int): EPSG code of the target CRS.
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDomainRequestBody | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        target_epsg=target_epsg,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateDomainRequestBody,
    target_epsg: int,
) -> CreateDomainRequestBody | HTTPValidationError | None:
    """Reproject a FeatureCollection to a target CRS

     # Reproject Domain Endpoint

    Stateless utility that reprojects a GeoJSON `FeatureCollection` from one
    coordinate reference system to another. No resource is created; the
    reprojected `FeatureCollection` is returned immediately.

    ## Query Parameters

    - **target_epsg**: (integer, required) EPSG code of the target CRS
      (e.g., `4326` for WGS84, `32611` for UTM zone 11N).

    ## Request Body

    A GeoJSON `FeatureCollection`. The source CRS is read from the
    `crs.properties.name` field if present; otherwise EPSG:4326 is assumed.

    ## Response

    Returns the reprojected `FeatureCollection` with:

    - **features**: All input features reprojected to the target CRS, with
      original feature properties preserved.
    - **crs**: Set to the target EPSG code.

    ## Error Responses

    - **422**: Invalid source CRS, invalid target EPSG, or geometry that
      cannot be reprojected.

    Args:
        target_epsg (int): EPSG code of the target CRS.
        body (CreateDomainRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDomainRequestBody | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            target_epsg=target_epsg,
        )
    ).parsed
