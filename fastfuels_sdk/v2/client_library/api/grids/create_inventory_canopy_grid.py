from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_inventory_canopy_request import CreateInventoryCanopyRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateInventoryCanopyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/canopy/inventory".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = Grid.from_dict(response.json())

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
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
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
    body: CreateInventoryCanopyRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a canopy fuel grid from a tree inventory

     # Create Inventory Canopy Grid

    Derives the canopy fuel metrics operational fire models consume — canopy
    bulk density (`cbd`), canopy base height (`cbh`), canopy height (`chm`),
    canopy cover (`cc`), and optionally canopy fuel load (`cfl`) — directly
    from a tree inventory, with no voxelization.

    For each tree, available canopy fuel is estimated from crown biomass,
    distributed vertically over the crown, and attributed to output cells;
    each cell's vertical profile is then reduced to the requested bands. This
    is the FuelCalc-style profile method computed per cell from real stem
    positions instead of per plot from expanded tree records. Bands share
    keys and units with the LANDFIRE canopy source, so the result drops into
    anything that accepts one — including the landscape export.

    Only live trees contribute canopy fuel, matching FuelCalc's exclusion of
    dead trees.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory in
      this domain. Required columns depend on the selected methods; the
      defaults need `x`, `y`, `height`, `crown_ratio`, `dbh`, and
      `fia_species_code`.
    - **alignment**: (optional) Output lattice. Against the domain (the
      default) `resolution` defaults to 30 m — an inventory has no native
      cell size to inherit. Against another grid, omitting `resolution`
      matches that grid's lattice exactly. `target: \"native\"` is not
      supported.
    - **bands**: (optional) Defaults to `[\"cbd\", \"cbh\", \"chm\", \"cc\"]` — the
      four landscape-file canopy roles. Add `cfl` for canopy fuel load.
    - **biomass_source**: (optional) `allometry` with `nsvb` (default),
      `jenkins`, or `brown_1978` equations, or `inventory_column` carrying
      precomputed per-tree available canopy fuel.
    - **available_fuel**: (optional) Foliage fraction plus the fine-branchwood
      size partition and fraction. Resolved to `null` with an
      `inventory_column` biomass source.
    - **species_inclusion**, **crown_class_adjustment**, **min_tree_height**:
      (optional) Which trees contribute, and how crown weight is adjusted for
      canopy position.
    - **vertical_distribution**, **layer_depth**: (optional) How each tree's
      fuel stacks over its crown, and the profile layer depth (default
      0.3048 m, FuelCalc's 1 ft).
    - **horizontal_distribution**: (optional) `crown_projected` (default)
      splits each tree's fuel over the cells its crown covers;
      `stem` assigns it to the stem cell.
    - **max_crown_radius_source**: (optional) Allometric crown radii
      (default) or a per-tree inventory column (e.g. from LiDAR).
    - **cbd**, **cbh**, **chm**, **cc**: (optional) Per-band reduction
      methods. Each may only be supplied when its band is requested;
      requested bands default to the FuelCalc-style methods.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    The stored grid `source` records every resolved choice, including
    defaults, so the grid is exactly reproducible from the resource alone.

    ## Response

    Returns the created Grid with status `\"pending\"` and
    `georeference: null`. Griddle computes the canopy metrics asynchronously
    and updates the grid to `\"completed\"` with a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateInventoryCanopyRequest): Request body for creating a canopy fuel grid from a
            tree inventory.

            Only live trees contribute canopy fuel: the worker reads live
            inventory records only, matching FuelCalc, which excludes dead trees
            from all calculations.

            Does not extend CreateGridRequestBase: like DUET and the 3D voxel
            grids, inventory-derived grids do not support modifications — apply
            treatments and modifications to the inventory before deriving canopy
            metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateInventoryCanopyRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a canopy fuel grid from a tree inventory

     # Create Inventory Canopy Grid

    Derives the canopy fuel metrics operational fire models consume — canopy
    bulk density (`cbd`), canopy base height (`cbh`), canopy height (`chm`),
    canopy cover (`cc`), and optionally canopy fuel load (`cfl`) — directly
    from a tree inventory, with no voxelization.

    For each tree, available canopy fuel is estimated from crown biomass,
    distributed vertically over the crown, and attributed to output cells;
    each cell's vertical profile is then reduced to the requested bands. This
    is the FuelCalc-style profile method computed per cell from real stem
    positions instead of per plot from expanded tree records. Bands share
    keys and units with the LANDFIRE canopy source, so the result drops into
    anything that accepts one — including the landscape export.

    Only live trees contribute canopy fuel, matching FuelCalc's exclusion of
    dead trees.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory in
      this domain. Required columns depend on the selected methods; the
      defaults need `x`, `y`, `height`, `crown_ratio`, `dbh`, and
      `fia_species_code`.
    - **alignment**: (optional) Output lattice. Against the domain (the
      default) `resolution` defaults to 30 m — an inventory has no native
      cell size to inherit. Against another grid, omitting `resolution`
      matches that grid's lattice exactly. `target: \"native\"` is not
      supported.
    - **bands**: (optional) Defaults to `[\"cbd\", \"cbh\", \"chm\", \"cc\"]` — the
      four landscape-file canopy roles. Add `cfl` for canopy fuel load.
    - **biomass_source**: (optional) `allometry` with `nsvb` (default),
      `jenkins`, or `brown_1978` equations, or `inventory_column` carrying
      precomputed per-tree available canopy fuel.
    - **available_fuel**: (optional) Foliage fraction plus the fine-branchwood
      size partition and fraction. Resolved to `null` with an
      `inventory_column` biomass source.
    - **species_inclusion**, **crown_class_adjustment**, **min_tree_height**:
      (optional) Which trees contribute, and how crown weight is adjusted for
      canopy position.
    - **vertical_distribution**, **layer_depth**: (optional) How each tree's
      fuel stacks over its crown, and the profile layer depth (default
      0.3048 m, FuelCalc's 1 ft).
    - **horizontal_distribution**: (optional) `crown_projected` (default)
      splits each tree's fuel over the cells its crown covers;
      `stem` assigns it to the stem cell.
    - **max_crown_radius_source**: (optional) Allometric crown radii
      (default) or a per-tree inventory column (e.g. from LiDAR).
    - **cbd**, **cbh**, **chm**, **cc**: (optional) Per-band reduction
      methods. Each may only be supplied when its band is requested;
      requested bands default to the FuelCalc-style methods.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    The stored grid `source` records every resolved choice, including
    defaults, so the grid is exactly reproducible from the resource alone.

    ## Response

    Returns the created Grid with status `\"pending\"` and
    `georeference: null`. Griddle computes the canopy metrics asynchronously
    and updates the grid to `\"completed\"` with a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateInventoryCanopyRequest): Request body for creating a canopy fuel grid from a
            tree inventory.

            Only live trees contribute canopy fuel: the worker reads live
            inventory records only, matching FuelCalc, which excludes dead trees
            from all calculations.

            Does not extend CreateGridRequestBase: like DUET and the 3D voxel
            grids, inventory-derived grids do not support modifications — apply
            treatments and modifications to the inventory before deriving canopy
            metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError | QuotaExceededDetail
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
    body: CreateInventoryCanopyRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Create a canopy fuel grid from a tree inventory

     # Create Inventory Canopy Grid

    Derives the canopy fuel metrics operational fire models consume — canopy
    bulk density (`cbd`), canopy base height (`cbh`), canopy height (`chm`),
    canopy cover (`cc`), and optionally canopy fuel load (`cfl`) — directly
    from a tree inventory, with no voxelization.

    For each tree, available canopy fuel is estimated from crown biomass,
    distributed vertically over the crown, and attributed to output cells;
    each cell's vertical profile is then reduced to the requested bands. This
    is the FuelCalc-style profile method computed per cell from real stem
    positions instead of per plot from expanded tree records. Bands share
    keys and units with the LANDFIRE canopy source, so the result drops into
    anything that accepts one — including the landscape export.

    Only live trees contribute canopy fuel, matching FuelCalc's exclusion of
    dead trees.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory in
      this domain. Required columns depend on the selected methods; the
      defaults need `x`, `y`, `height`, `crown_ratio`, `dbh`, and
      `fia_species_code`.
    - **alignment**: (optional) Output lattice. Against the domain (the
      default) `resolution` defaults to 30 m — an inventory has no native
      cell size to inherit. Against another grid, omitting `resolution`
      matches that grid's lattice exactly. `target: \"native\"` is not
      supported.
    - **bands**: (optional) Defaults to `[\"cbd\", \"cbh\", \"chm\", \"cc\"]` — the
      four landscape-file canopy roles. Add `cfl` for canopy fuel load.
    - **biomass_source**: (optional) `allometry` with `nsvb` (default),
      `jenkins`, or `brown_1978` equations, or `inventory_column` carrying
      precomputed per-tree available canopy fuel.
    - **available_fuel**: (optional) Foliage fraction plus the fine-branchwood
      size partition and fraction. Resolved to `null` with an
      `inventory_column` biomass source.
    - **species_inclusion**, **crown_class_adjustment**, **min_tree_height**:
      (optional) Which trees contribute, and how crown weight is adjusted for
      canopy position.
    - **vertical_distribution**, **layer_depth**: (optional) How each tree's
      fuel stacks over its crown, and the profile layer depth (default
      0.3048 m, FuelCalc's 1 ft).
    - **horizontal_distribution**: (optional) `crown_projected` (default)
      splits each tree's fuel over the cells its crown covers;
      `stem` assigns it to the stem cell.
    - **max_crown_radius_source**: (optional) Allometric crown radii
      (default) or a per-tree inventory column (e.g. from LiDAR).
    - **cbd**, **cbh**, **chm**, **cc**: (optional) Per-band reduction
      methods. Each may only be supplied when its band is requested;
      requested bands default to the FuelCalc-style methods.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    The stored grid `source` records every resolved choice, including
    defaults, so the grid is exactly reproducible from the resource alone.

    ## Response

    Returns the created Grid with status `\"pending\"` and
    `georeference: null`. Griddle computes the canopy metrics asynchronously
    and updates the grid to `\"completed\"` with a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateInventoryCanopyRequest): Request body for creating a canopy fuel grid from a
            tree inventory.

            Only live trees contribute canopy fuel: the worker reads live
            inventory records only, matching FuelCalc, which excludes dead trees
            from all calculations.

            Does not extend CreateGridRequestBase: like DUET and the 3D voxel
            grids, inventory-derived grids do not support modifications — apply
            treatments and modifications to the inventory before deriving canopy
            metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError | QuotaExceededDetail]
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
    body: CreateInventoryCanopyRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Create a canopy fuel grid from a tree inventory

     # Create Inventory Canopy Grid

    Derives the canopy fuel metrics operational fire models consume — canopy
    bulk density (`cbd`), canopy base height (`cbh`), canopy height (`chm`),
    canopy cover (`cc`), and optionally canopy fuel load (`cfl`) — directly
    from a tree inventory, with no voxelization.

    For each tree, available canopy fuel is estimated from crown biomass,
    distributed vertically over the crown, and attributed to output cells;
    each cell's vertical profile is then reduced to the requested bands. This
    is the FuelCalc-style profile method computed per cell from real stem
    positions instead of per plot from expanded tree records. Bands share
    keys and units with the LANDFIRE canopy source, so the result drops into
    anything that accepts one — including the landscape export.

    Only live trees contribute canopy fuel, matching FuelCalc's exclusion of
    dead trees.

    ## Request Body

    - **source_inventory_id**: (required) ID of a completed tree inventory in
      this domain. Required columns depend on the selected methods; the
      defaults need `x`, `y`, `height`, `crown_ratio`, `dbh`, and
      `fia_species_code`.
    - **alignment**: (optional) Output lattice. Against the domain (the
      default) `resolution` defaults to 30 m — an inventory has no native
      cell size to inherit. Against another grid, omitting `resolution`
      matches that grid's lattice exactly. `target: \"native\"` is not
      supported.
    - **bands**: (optional) Defaults to `[\"cbd\", \"cbh\", \"chm\", \"cc\"]` — the
      four landscape-file canopy roles. Add `cfl` for canopy fuel load.
    - **biomass_source**: (optional) `allometry` with `nsvb` (default),
      `jenkins`, or `brown_1978` equations, or `inventory_column` carrying
      precomputed per-tree available canopy fuel.
    - **available_fuel**: (optional) Foliage fraction plus the fine-branchwood
      size partition and fraction. Resolved to `null` with an
      `inventory_column` biomass source.
    - **species_inclusion**, **crown_class_adjustment**, **min_tree_height**:
      (optional) Which trees contribute, and how crown weight is adjusted for
      canopy position.
    - **vertical_distribution**, **layer_depth**: (optional) How each tree's
      fuel stacks over its crown, and the profile layer depth (default
      0.3048 m, FuelCalc's 1 ft).
    - **horizontal_distribution**: (optional) `crown_projected` (default)
      splits each tree's fuel over the cells its crown covers;
      `stem` assigns it to the stem cell.
    - **max_crown_radius_source**: (optional) Allometric crown radii
      (default) or a per-tree inventory column (e.g. from LiDAR).
    - **cbd**, **cbh**, **chm**, **cc**: (optional) Per-band reduction
      methods. Each may only be supplied when its band is requested;
      requested bands default to the FuelCalc-style methods.
    - **name**, **description**, **tags**: (optional) Standard metadata.

    The stored grid `source` records every resolved choice, including
    defaults, so the grid is exactly reproducible from the resource alone.

    ## Response

    Returns the created Grid with status `\"pending\"` and
    `georeference: null`. Griddle computes the canopy metrics asynchronously
    and updates the grid to `\"completed\"` with a 2D `Georeference` when done.

    Args:
        domain_id (str):
        body (CreateInventoryCanopyRequest): Request body for creating a canopy fuel grid from a
            tree inventory.

            Only live trees contribute canopy fuel: the worker reads live
            inventory records only, matching FuelCalc, which excludes dead trees
            from all calculations.

            Does not extend CreateGridRequestBase: like DUET and the 3D voxel
            grids, inventory-derived grids do not support modifications — apply
            treatments and modifications to the inventory before deriving canopy
            metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
