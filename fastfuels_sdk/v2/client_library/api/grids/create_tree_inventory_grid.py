from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_tree_inventory_request import CreateTreeInventoryRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateTreeInventoryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/voxelize/inventory/tree".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Grid | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = Grid.from_dict(response.json())

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
) -> Response[Grid | HTTPValidationError]:
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
    body: CreateTreeInventoryRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a 3D tree fuel grid from a tree inventory

     # Create Tree Inventory Grid

    Voxelizes a tree inventory into a 3D canopy fuel grid. Each tree's crown
    is discretized onto the voxel grid using a species-specific crown profile
    model, and per-voxel fuel properties (bulk density, moisture, SAV) are
    computed from biomass and moisture models.

    This is a 3D grid product — resampling and modifications are not
    supported. Apply modifications to the source inventory before voxelizing.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown geometry model. One of
      `purves` (default) or `beta`.
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. Defaults to the crown profile model's allometric value;
      pass `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled.
    - **moisture_model**: (optional) Live/dead fuel moisture configuration.
      Required shape: `{\"live\": {\"method\": \"uniform\", \"value\": <percent>}}`
      and/or `{\"dead\": {\"method\": \"uniform\", \"value\": <percent>}}`.
      Applied only when matching `fuel_moisture.*` bands are requested. Live
      defaults to 100%; dead defaults to 10%.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Grid resource with status `\"pending\"` and
    `georeference: null`. The Treevox backend performs voxelization
    asynchronously and updates the grid to `\"completed\"` with a
    `Georeference3D` when done.

    Args:
        domain_id (str):
        body (CreateTreeInventoryRequest): Request body for creating a tree fuel grid from a tree
            inventory.

            Does not extend CreateGridRequestBase because 3D grids do not support
            modifications — modifications must be applied to the inventory before
            voxelization, not to the resulting voxel grid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: CreateTreeInventoryRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a 3D tree fuel grid from a tree inventory

     # Create Tree Inventory Grid

    Voxelizes a tree inventory into a 3D canopy fuel grid. Each tree's crown
    is discretized onto the voxel grid using a species-specific crown profile
    model, and per-voxel fuel properties (bulk density, moisture, SAV) are
    computed from biomass and moisture models.

    This is a 3D grid product — resampling and modifications are not
    supported. Apply modifications to the source inventory before voxelizing.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown geometry model. One of
      `purves` (default) or `beta`.
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. Defaults to the crown profile model's allometric value;
      pass `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled.
    - **moisture_model**: (optional) Live/dead fuel moisture configuration.
      Required shape: `{\"live\": {\"method\": \"uniform\", \"value\": <percent>}}`
      and/or `{\"dead\": {\"method\": \"uniform\", \"value\": <percent>}}`.
      Applied only when matching `fuel_moisture.*` bands are requested. Live
      defaults to 100%; dead defaults to 10%.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Grid resource with status `\"pending\"` and
    `georeference: null`. The Treevox backend performs voxelization
    asynchronously and updates the grid to `\"completed\"` with a
    `Georeference3D` when done.

    Args:
        domain_id (str):
        body (CreateTreeInventoryRequest): Request body for creating a tree fuel grid from a tree
            inventory.

            Does not extend CreateGridRequestBase because 3D grids do not support
            modifications — modifications must be applied to the inventory before
            voxelization, not to the resulting voxel grid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
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
    body: CreateTreeInventoryRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a 3D tree fuel grid from a tree inventory

     # Create Tree Inventory Grid

    Voxelizes a tree inventory into a 3D canopy fuel grid. Each tree's crown
    is discretized onto the voxel grid using a species-specific crown profile
    model, and per-voxel fuel properties (bulk density, moisture, SAV) are
    computed from biomass and moisture models.

    This is a 3D grid product — resampling and modifications are not
    supported. Apply modifications to the source inventory before voxelizing.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown geometry model. One of
      `purves` (default) or `beta`.
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. Defaults to the crown profile model's allometric value;
      pass `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled.
    - **moisture_model**: (optional) Live/dead fuel moisture configuration.
      Required shape: `{\"live\": {\"method\": \"uniform\", \"value\": <percent>}}`
      and/or `{\"dead\": {\"method\": \"uniform\", \"value\": <percent>}}`.
      Applied only when matching `fuel_moisture.*` bands are requested. Live
      defaults to 100%; dead defaults to 10%.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Grid resource with status `\"pending\"` and
    `georeference: null`. The Treevox backend performs voxelization
    asynchronously and updates the grid to `\"completed\"` with a
    `Georeference3D` when done.

    Args:
        domain_id (str):
        body (CreateTreeInventoryRequest): Request body for creating a tree fuel grid from a tree
            inventory.

            Does not extend CreateGridRequestBase because 3D grids do not support
            modifications — modifications must be applied to the inventory before
            voxelization, not to the resulting voxel grid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: CreateTreeInventoryRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a 3D tree fuel grid from a tree inventory

     # Create Tree Inventory Grid

    Voxelizes a tree inventory into a 3D canopy fuel grid. Each tree's crown
    is discretized onto the voxel grid using a species-specific crown profile
    model, and per-voxel fuel properties (bulk density, moisture, SAV) are
    computed from biomass and moisture models.

    This is a 3D grid product — resampling and modifications are not
    supported. Apply modifications to the source inventory before voxelizing.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown geometry model. One of
      `purves` (default) or `beta`.
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. Defaults to the crown profile model's allometric value;
      pass `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled.
    - **moisture_model**: (optional) Live/dead fuel moisture configuration.
      Required shape: `{\"live\": {\"method\": \"uniform\", \"value\": <percent>}}`
      and/or `{\"dead\": {\"method\": \"uniform\", \"value\": <percent>}}`.
      Applied only when matching `fuel_moisture.*` bands are requested. Live
      defaults to 100%; dead defaults to 10%.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    ## Response

    Returns the created Grid resource with status `\"pending\"` and
    `georeference: null`. The Treevox backend performs voxelization
    asynchronously and updates the grid to `\"completed\"` with a
    `Georeference3D` when done.

    Args:
        domain_id (str):
        body (CreateTreeInventoryRequest): Request body for creating a tree fuel grid from a tree
            inventory.

            Does not extend CreateGridRequestBase because 3D grids do not support
            modifications — modifications must be applied to the inventory before
            voxelization, not to the resulting voxel grid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
