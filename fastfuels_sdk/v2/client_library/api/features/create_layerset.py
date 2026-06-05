from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_layerset_request_body import CreateLayersetRequestBody
from ...models.feature import Feature
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateLayersetRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/features/layerset/geojson".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Feature | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = Feature.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Feature | HTTPValidationError]:
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
    body: CreateLayersetRequestBody,
) -> Response[Feature | HTTPValidationError]:
    r"""Upload a custom Layerset

     # Create Layerset Endpoint

    Uploads a flat GeoJSON FeatureCollection of fuelbed polygons as a new
    feature resource. Each Feature's ``properties`` block carries one
    fuelbed's input columns for ``fastfuels_core.rasterize_layerset``. The
    payload is validated and saved directly to Cloud Storage.

    ## Path Parameters
    - **domain_id**: (string) The domain this layerset belongs to.

    ## Request Body

    The body **is** the GeoJSON FeatureCollection (mirroring `POST /domains`),
    with optional resource metadata as top-level fields:

    - **type**: (string) Must be `\"FeatureCollection\"`.
    - **features**: (array) At least one Feature, each carrying one fuelbed's
      `properties` and a `Polygon`/`MultiPolygon` `geometry`.
    - **crs**: (object) The GeoJSON `crs` block declaring a **projected** CRS
      (e.g. `EPSG:32612`). Geographic CRSes are rejected — rasterization
      requires cell sizes in meters.
    - **name**: (string, optional) Name of the layerset.
    - **description**: (string, optional) Description of the data.
    - **tags**: (array of strings, optional) Searchable tags.

    ## Response
    Returns the created Feature resource with a status of `completed`.

    Args:
        domain_id (str):
        body (CreateLayersetRequestBody): Request body for uploading a flat GeoJSON layerset.

            The body **is** the GeoJSON FeatureCollection (matching ``POST /domains``,
            whose body is a ``FeatureCollection`` directly), extended with the
            resource-metadata fields. No ``type`` discriminator: the URL
            ``/features/layerset/geojson`` already discriminates layersets from
            road/water uploads.

            ``name`` overrides the optional GeoJSON ``name`` member inherited from
            ``LayersetFeatureCollection`` — the FeatureCollection's name doubles as the
            resource name, exactly as ``CreateDomainRequestBody`` treats it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Feature | HTTPValidationError]
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
    body: CreateLayersetRequestBody,
) -> Feature | HTTPValidationError | None:
    r"""Upload a custom Layerset

     # Create Layerset Endpoint

    Uploads a flat GeoJSON FeatureCollection of fuelbed polygons as a new
    feature resource. Each Feature's ``properties`` block carries one
    fuelbed's input columns for ``fastfuels_core.rasterize_layerset``. The
    payload is validated and saved directly to Cloud Storage.

    ## Path Parameters
    - **domain_id**: (string) The domain this layerset belongs to.

    ## Request Body

    The body **is** the GeoJSON FeatureCollection (mirroring `POST /domains`),
    with optional resource metadata as top-level fields:

    - **type**: (string) Must be `\"FeatureCollection\"`.
    - **features**: (array) At least one Feature, each carrying one fuelbed's
      `properties` and a `Polygon`/`MultiPolygon` `geometry`.
    - **crs**: (object) The GeoJSON `crs` block declaring a **projected** CRS
      (e.g. `EPSG:32612`). Geographic CRSes are rejected — rasterization
      requires cell sizes in meters.
    - **name**: (string, optional) Name of the layerset.
    - **description**: (string, optional) Description of the data.
    - **tags**: (array of strings, optional) Searchable tags.

    ## Response
    Returns the created Feature resource with a status of `completed`.

    Args:
        domain_id (str):
        body (CreateLayersetRequestBody): Request body for uploading a flat GeoJSON layerset.

            The body **is** the GeoJSON FeatureCollection (matching ``POST /domains``,
            whose body is a ``FeatureCollection`` directly), extended with the
            resource-metadata fields. No ``type`` discriminator: the URL
            ``/features/layerset/geojson`` already discriminates layersets from
            road/water uploads.

            ``name`` overrides the optional GeoJSON ``name`` member inherited from
            ``LayersetFeatureCollection`` — the FeatureCollection's name doubles as the
            resource name, exactly as ``CreateDomainRequestBody`` treats it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Feature | HTTPValidationError
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
    body: CreateLayersetRequestBody,
) -> Response[Feature | HTTPValidationError]:
    r"""Upload a custom Layerset

     # Create Layerset Endpoint

    Uploads a flat GeoJSON FeatureCollection of fuelbed polygons as a new
    feature resource. Each Feature's ``properties`` block carries one
    fuelbed's input columns for ``fastfuels_core.rasterize_layerset``. The
    payload is validated and saved directly to Cloud Storage.

    ## Path Parameters
    - **domain_id**: (string) The domain this layerset belongs to.

    ## Request Body

    The body **is** the GeoJSON FeatureCollection (mirroring `POST /domains`),
    with optional resource metadata as top-level fields:

    - **type**: (string) Must be `\"FeatureCollection\"`.
    - **features**: (array) At least one Feature, each carrying one fuelbed's
      `properties` and a `Polygon`/`MultiPolygon` `geometry`.
    - **crs**: (object) The GeoJSON `crs` block declaring a **projected** CRS
      (e.g. `EPSG:32612`). Geographic CRSes are rejected — rasterization
      requires cell sizes in meters.
    - **name**: (string, optional) Name of the layerset.
    - **description**: (string, optional) Description of the data.
    - **tags**: (array of strings, optional) Searchable tags.

    ## Response
    Returns the created Feature resource with a status of `completed`.

    Args:
        domain_id (str):
        body (CreateLayersetRequestBody): Request body for uploading a flat GeoJSON layerset.

            The body **is** the GeoJSON FeatureCollection (matching ``POST /domains``,
            whose body is a ``FeatureCollection`` directly), extended with the
            resource-metadata fields. No ``type`` discriminator: the URL
            ``/features/layerset/geojson`` already discriminates layersets from
            road/water uploads.

            ``name`` overrides the optional GeoJSON ``name`` member inherited from
            ``LayersetFeatureCollection`` — the FeatureCollection's name doubles as the
            resource name, exactly as ``CreateDomainRequestBody`` treats it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Feature | HTTPValidationError]
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
    body: CreateLayersetRequestBody,
) -> Feature | HTTPValidationError | None:
    r"""Upload a custom Layerset

     # Create Layerset Endpoint

    Uploads a flat GeoJSON FeatureCollection of fuelbed polygons as a new
    feature resource. Each Feature's ``properties`` block carries one
    fuelbed's input columns for ``fastfuels_core.rasterize_layerset``. The
    payload is validated and saved directly to Cloud Storage.

    ## Path Parameters
    - **domain_id**: (string) The domain this layerset belongs to.

    ## Request Body

    The body **is** the GeoJSON FeatureCollection (mirroring `POST /domains`),
    with optional resource metadata as top-level fields:

    - **type**: (string) Must be `\"FeatureCollection\"`.
    - **features**: (array) At least one Feature, each carrying one fuelbed's
      `properties` and a `Polygon`/`MultiPolygon` `geometry`.
    - **crs**: (object) The GeoJSON `crs` block declaring a **projected** CRS
      (e.g. `EPSG:32612`). Geographic CRSes are rejected — rasterization
      requires cell sizes in meters.
    - **name**: (string, optional) Name of the layerset.
    - **description**: (string, optional) Description of the data.
    - **tags**: (array of strings, optional) Searchable tags.

    ## Response
    Returns the created Feature resource with a status of `completed`.

    Args:
        domain_id (str):
        body (CreateLayersetRequestBody): Request body for uploading a flat GeoJSON layerset.

            The body **is** the GeoJSON FeatureCollection (matching ``POST /domains``,
            whose body is a ``FeatureCollection`` directly), extended with the
            resource-metadata fields. No ``type`` discriminator: the URL
            ``/features/layerset/geojson`` already discriminates layersets from
            road/water uploads.

            ``name`` overrides the optional GeoJSON ``name`` member inherited from
            ``LayersetFeatureCollection`` — the FeatureCollection's name doubles as the
            resource name, exactly as ``CreateDomainRequestBody`` treats it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Feature | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
