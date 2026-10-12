from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_chm_crown_feature_request import CreateChmCrownFeatureRequest
from ...models.feature import Feature
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateChmCrownFeatureRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/features/crown/chm".format(
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
    body: CreateChmCrownFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a crown feature from a CHM

     # Create CHM Crown Feature

    Outlines each tree's crown by growing it on a Canopy Height Model (CHM)
    from the tree's position in an existing tree inventory.

    Each inventory tree seeds one crown in the CHM cell that contains its
    `x`, `y`. Crowns grow outward one ring of 4-connected cells at a time
    (Dalponte & Coomes, 2016) and never overlap. A tree gets no crown if it
    lies outside the CHM, sits on a no-data cell, or shares its cell with a
    taller tree (ties go to the lower `tree_id`).
    A tree whose CHM cell is below `min_height`, such as one on bare ground,
    gets a one-cell crown.

    The inventory must hold trees detected from this CHM, created with
    `POST /inventories/tree/chm` from `source_chm_grid_id`, so that each crown
    belongs to the tree that made it.

    The completed feature holds one row per crown with columns `tree_id` (the
    seed tree's `tree_id`) and `geometry` (a `Polygon` in the domain CRS,
    traced along CHM cell edges). Read it from the feature's `/data`
    endpoints.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory
      created with `POST /inventories/tree/chm` from `source_chm_grid_id`.
    - **source_chm_grid_id**: (required) ID of a completed grid with a `chm`
      band in metres, at 2 m resolution or finer.
    - **crown_segmentation**: (optional) Segmentation settings. Defaults are
      used for any field left out.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Feature resource with status `\"pending\"`. The backend
    worker segments the crowns asynchronously and updates status to
    `\"completed\"` when ready.

    Args:
        domain_id (str):
        body (CreateChmCrownFeatureRequest): Request body for creating a crown feature from a CHM.

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
    body: CreateChmCrownFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a crown feature from a CHM

     # Create CHM Crown Feature

    Outlines each tree's crown by growing it on a Canopy Height Model (CHM)
    from the tree's position in an existing tree inventory.

    Each inventory tree seeds one crown in the CHM cell that contains its
    `x`, `y`. Crowns grow outward one ring of 4-connected cells at a time
    (Dalponte & Coomes, 2016) and never overlap. A tree gets no crown if it
    lies outside the CHM, sits on a no-data cell, or shares its cell with a
    taller tree (ties go to the lower `tree_id`).
    A tree whose CHM cell is below `min_height`, such as one on bare ground,
    gets a one-cell crown.

    The inventory must hold trees detected from this CHM, created with
    `POST /inventories/tree/chm` from `source_chm_grid_id`, so that each crown
    belongs to the tree that made it.

    The completed feature holds one row per crown with columns `tree_id` (the
    seed tree's `tree_id`) and `geometry` (a `Polygon` in the domain CRS,
    traced along CHM cell edges). Read it from the feature's `/data`
    endpoints.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory
      created with `POST /inventories/tree/chm` from `source_chm_grid_id`.
    - **source_chm_grid_id**: (required) ID of a completed grid with a `chm`
      band in metres, at 2 m resolution or finer.
    - **crown_segmentation**: (optional) Segmentation settings. Defaults are
      used for any field left out.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Feature resource with status `\"pending\"`. The backend
    worker segments the crowns asynchronously and updates status to
    `\"completed\"` when ready.

    Args:
        domain_id (str):
        body (CreateChmCrownFeatureRequest): Request body for creating a crown feature from a CHM.

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
    body: CreateChmCrownFeatureRequest,
) -> Response[Feature | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a crown feature from a CHM

     # Create CHM Crown Feature

    Outlines each tree's crown by growing it on a Canopy Height Model (CHM)
    from the tree's position in an existing tree inventory.

    Each inventory tree seeds one crown in the CHM cell that contains its
    `x`, `y`. Crowns grow outward one ring of 4-connected cells at a time
    (Dalponte & Coomes, 2016) and never overlap. A tree gets no crown if it
    lies outside the CHM, sits on a no-data cell, or shares its cell with a
    taller tree (ties go to the lower `tree_id`).
    A tree whose CHM cell is below `min_height`, such as one on bare ground,
    gets a one-cell crown.

    The inventory must hold trees detected from this CHM, created with
    `POST /inventories/tree/chm` from `source_chm_grid_id`, so that each crown
    belongs to the tree that made it.

    The completed feature holds one row per crown with columns `tree_id` (the
    seed tree's `tree_id`) and `geometry` (a `Polygon` in the domain CRS,
    traced along CHM cell edges). Read it from the feature's `/data`
    endpoints.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory
      created with `POST /inventories/tree/chm` from `source_chm_grid_id`.
    - **source_chm_grid_id**: (required) ID of a completed grid with a `chm`
      band in metres, at 2 m resolution or finer.
    - **crown_segmentation**: (optional) Segmentation settings. Defaults are
      used for any field left out.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Feature resource with status `\"pending\"`. The backend
    worker segments the crowns asynchronously and updates status to
    `\"completed\"` when ready.

    Args:
        domain_id (str):
        body (CreateChmCrownFeatureRequest): Request body for creating a crown feature from a CHM.

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
    body: CreateChmCrownFeatureRequest,
) -> Feature | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a crown feature from a CHM

     # Create CHM Crown Feature

    Outlines each tree's crown by growing it on a Canopy Height Model (CHM)
    from the tree's position in an existing tree inventory.

    Each inventory tree seeds one crown in the CHM cell that contains its
    `x`, `y`. Crowns grow outward one ring of 4-connected cells at a time
    (Dalponte & Coomes, 2016) and never overlap. A tree gets no crown if it
    lies outside the CHM, sits on a no-data cell, or shares its cell with a
    taller tree (ties go to the lower `tree_id`).
    A tree whose CHM cell is below `min_height`, such as one on bare ground,
    gets a one-cell crown.

    The inventory must hold trees detected from this CHM, created with
    `POST /inventories/tree/chm` from `source_chm_grid_id`, so that each crown
    belongs to the tree that made it.

    The completed feature holds one row per crown with columns `tree_id` (the
    seed tree's `tree_id`) and `geometry` (a `Polygon` in the domain CRS,
    traced along CHM cell edges). Read it from the feature's `/data`
    endpoints.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory
      created with `POST /inventories/tree/chm` from `source_chm_grid_id`.
    - **source_chm_grid_id**: (required) ID of a completed grid with a `chm`
      band in metres, at 2 m resolution or finer.
    - **crown_segmentation**: (optional) Segmentation settings. Defaults are
      used for any field left out.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Feature resource with status `\"pending\"`. The backend
    worker segments the crowns asynchronously and updates status to
    `\"completed\"` when ready.

    Args:
        domain_id (str):
        body (CreateChmCrownFeatureRequest): Request body for creating a crown feature from a CHM.

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
