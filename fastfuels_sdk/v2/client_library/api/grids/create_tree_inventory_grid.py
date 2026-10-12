from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_tree_inventory_request import CreateTreeInventoryRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
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
    body: CreateTreeInventoryRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
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
      Its `x`, `y`, `height`, `dbh`, `crown_ratio` and `fia_species_code`
      (and any biomass column read) must have no null values; a null
      `fia_status_code` counts as live.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown shape. Every crown runs from
      the crown base, height × (1 − crown_ratio), to the tree height.
      - `purves` (default): Purves et al. (2007), species-specific; widest at
        the crown base.
      - `beta`: species-group beta distribution; widest within the crown, per
        species group.
      - `cone`: right circular cone; widest at the crown base.
      - `cylinder`: right circular cylinder; uniform radius.
      - `single_ellipsoid`: one half-ellipsoid of revolution; widest at the
        crown base.
      - `dual_ellipsoid`: two half-ellipsoids joined at the crown midpoint;
        widest there.
      - `single_paraboloid`: one paraboloid of revolution; widest at the crown
        base.
      - `dual_paraboloid`: two paraboloids joined at the crown midpoint;
        widest there (the LANL Trees crown envelope).
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. The default, `{\"type\": \"allometry\"}`, uses the Purves et
      al. (2007) maximum crown radius for `purves` and every geometric shape
      (`cone`, `cylinder`, ellipsoids, paraboloids), so a tree's crown is
      equally wide under each of them and only the shape changes; `beta` uses
      its own allometric radius. Pass
      `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled. A tree with a null in that column uses its
      allometric radius.
    - **crown_geometry_source**: (optional) Where crown shapes come from.
      `{\"type\": \"parametric\"}` (default) draws every crown from
      `crown_profile_model`. `{\"type\": \"crown_feature\", \"feature_id\": <id>}`
      gives each tree with a crown in that crown Feature a measured crown,
      matched by `tree_id`:
      - Outline: the crown's CHM cells.
      - Top: each cell's CHM height.
      - Bottom: `crown_profile_model`, going up from the crown base. Profiles
        widest at the crown base give a flat bottom there; `beta` and the
        dual profiles give a bottom that rises toward the crown's edge. Each
        cell's bottom is at least one voxel below its top, but never below
        the crown base.

      `max_crown_radius_source` does not apply to measured crowns, and every
      tree keeps the mass `biomass_source` gives it. Trees with no crown in
      the Feature, trees whose crown does not contain their stem, and trees
      with no CHM height above their crown base, are drawn parametrically.
      Crowns of trees not in the inventory are ignored. The inventory must
      have a `tree_id` column, the Feature must be a completed crown Feature
      in this domain, and the CHM grid it was built from must still exist.
    - **max_bulk_density**: (optional) Upper limit on bulk density, in
      kg/m**3. In any voxel where a biomass component's bulk density, live
      and dead combined, exceeds the limit, that component's live and dead
      bulk density are scaled down to it, keeping their live/dead split, and
      `leaf_area_density` is scaled with foliage. Fuel above the limit is
      removed from the grid. Omit for no limit.
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

    With a `crown_feature` source, `source.source_chm_grid_id` and
    `source.source_chm_grid_checksum` record the crown Feature's CHM grid and
    its `checksum` at creation, and the completed grid's
    `source.crown_geometry_counts` gives the number of trees drawn with a
    measured crown (`measured`) and drawn parametrically because they had no
    crown in the Feature (`parametric_no_crown`), their crown did not contain
    their stem (`parametric_stem_outside_crown`), or they had no CHM height
    above their crown base (`parametric_no_volume`). Trees that cannot be
    drawn at all are not counted.

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
    body: CreateTreeInventoryRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
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
      Its `x`, `y`, `height`, `dbh`, `crown_ratio` and `fia_species_code`
      (and any biomass column read) must have no null values; a null
      `fia_status_code` counts as live.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown shape. Every crown runs from
      the crown base, height × (1 − crown_ratio), to the tree height.
      - `purves` (default): Purves et al. (2007), species-specific; widest at
        the crown base.
      - `beta`: species-group beta distribution; widest within the crown, per
        species group.
      - `cone`: right circular cone; widest at the crown base.
      - `cylinder`: right circular cylinder; uniform radius.
      - `single_ellipsoid`: one half-ellipsoid of revolution; widest at the
        crown base.
      - `dual_ellipsoid`: two half-ellipsoids joined at the crown midpoint;
        widest there.
      - `single_paraboloid`: one paraboloid of revolution; widest at the crown
        base.
      - `dual_paraboloid`: two paraboloids joined at the crown midpoint;
        widest there (the LANL Trees crown envelope).
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. The default, `{\"type\": \"allometry\"}`, uses the Purves et
      al. (2007) maximum crown radius for `purves` and every geometric shape
      (`cone`, `cylinder`, ellipsoids, paraboloids), so a tree's crown is
      equally wide under each of them and only the shape changes; `beta` uses
      its own allometric radius. Pass
      `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled. A tree with a null in that column uses its
      allometric radius.
    - **crown_geometry_source**: (optional) Where crown shapes come from.
      `{\"type\": \"parametric\"}` (default) draws every crown from
      `crown_profile_model`. `{\"type\": \"crown_feature\", \"feature_id\": <id>}`
      gives each tree with a crown in that crown Feature a measured crown,
      matched by `tree_id`:
      - Outline: the crown's CHM cells.
      - Top: each cell's CHM height.
      - Bottom: `crown_profile_model`, going up from the crown base. Profiles
        widest at the crown base give a flat bottom there; `beta` and the
        dual profiles give a bottom that rises toward the crown's edge. Each
        cell's bottom is at least one voxel below its top, but never below
        the crown base.

      `max_crown_radius_source` does not apply to measured crowns, and every
      tree keeps the mass `biomass_source` gives it. Trees with no crown in
      the Feature, trees whose crown does not contain their stem, and trees
      with no CHM height above their crown base, are drawn parametrically.
      Crowns of trees not in the inventory are ignored. The inventory must
      have a `tree_id` column, the Feature must be a completed crown Feature
      in this domain, and the CHM grid it was built from must still exist.
    - **max_bulk_density**: (optional) Upper limit on bulk density, in
      kg/m**3. In any voxel where a biomass component's bulk density, live
      and dead combined, exceeds the limit, that component's live and dead
      bulk density are scaled down to it, keeping their live/dead split, and
      `leaf_area_density` is scaled with foliage. Fuel above the limit is
      removed from the grid. Omit for no limit.
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

    With a `crown_feature` source, `source.source_chm_grid_id` and
    `source.source_chm_grid_checksum` record the crown Feature's CHM grid and
    its `checksum` at creation, and the completed grid's
    `source.crown_geometry_counts` gives the number of trees drawn with a
    measured crown (`measured`) and drawn parametrically because they had no
    crown in the Feature (`parametric_no_crown`), their crown did not contain
    their stem (`parametric_stem_outside_crown`), or they had no CHM height
    above their crown base (`parametric_no_volume`). Trees that cannot be
    drawn at all are not counted.

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
    body: CreateTreeInventoryRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
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
      Its `x`, `y`, `height`, `dbh`, `crown_ratio` and `fia_species_code`
      (and any biomass column read) must have no null values; a null
      `fia_status_code` counts as live.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown shape. Every crown runs from
      the crown base, height × (1 − crown_ratio), to the tree height.
      - `purves` (default): Purves et al. (2007), species-specific; widest at
        the crown base.
      - `beta`: species-group beta distribution; widest within the crown, per
        species group.
      - `cone`: right circular cone; widest at the crown base.
      - `cylinder`: right circular cylinder; uniform radius.
      - `single_ellipsoid`: one half-ellipsoid of revolution; widest at the
        crown base.
      - `dual_ellipsoid`: two half-ellipsoids joined at the crown midpoint;
        widest there.
      - `single_paraboloid`: one paraboloid of revolution; widest at the crown
        base.
      - `dual_paraboloid`: two paraboloids joined at the crown midpoint;
        widest there (the LANL Trees crown envelope).
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. The default, `{\"type\": \"allometry\"}`, uses the Purves et
      al. (2007) maximum crown radius for `purves` and every geometric shape
      (`cone`, `cylinder`, ellipsoids, paraboloids), so a tree's crown is
      equally wide under each of them and only the shape changes; `beta` uses
      its own allometric radius. Pass
      `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled. A tree with a null in that column uses its
      allometric radius.
    - **crown_geometry_source**: (optional) Where crown shapes come from.
      `{\"type\": \"parametric\"}` (default) draws every crown from
      `crown_profile_model`. `{\"type\": \"crown_feature\", \"feature_id\": <id>}`
      gives each tree with a crown in that crown Feature a measured crown,
      matched by `tree_id`:
      - Outline: the crown's CHM cells.
      - Top: each cell's CHM height.
      - Bottom: `crown_profile_model`, going up from the crown base. Profiles
        widest at the crown base give a flat bottom there; `beta` and the
        dual profiles give a bottom that rises toward the crown's edge. Each
        cell's bottom is at least one voxel below its top, but never below
        the crown base.

      `max_crown_radius_source` does not apply to measured crowns, and every
      tree keeps the mass `biomass_source` gives it. Trees with no crown in
      the Feature, trees whose crown does not contain their stem, and trees
      with no CHM height above their crown base, are drawn parametrically.
      Crowns of trees not in the inventory are ignored. The inventory must
      have a `tree_id` column, the Feature must be a completed crown Feature
      in this domain, and the CHM grid it was built from must still exist.
    - **max_bulk_density**: (optional) Upper limit on bulk density, in
      kg/m**3. In any voxel where a biomass component's bulk density, live
      and dead combined, exceeds the limit, that component's live and dead
      bulk density are scaled down to it, keeping their live/dead split, and
      `leaf_area_density` is scaled with foliage. Fuel above the limit is
      removed from the grid. Omit for no limit.
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

    With a `crown_feature` source, `source.source_chm_grid_id` and
    `source.source_chm_grid_checksum` record the crown Feature's CHM grid and
    its `checksum` at creation, and the completed grid's
    `source.crown_geometry_counts` gives the number of trees drawn with a
    measured crown (`measured`) and drawn parametrically because they had no
    crown in the Feature (`parametric_no_crown`), their crown did not contain
    their stem (`parametric_stem_outside_crown`), or they had no CHM height
    above their crown base (`parametric_no_volume`). Trees that cannot be
    drawn at all are not counted.

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
    body: CreateTreeInventoryRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
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
      Its `x`, `y`, `height`, `dbh`, `crown_ratio` and `fia_species_code`
      (and any biomass column read) must have no null values; a null
      `fia_status_code` counts as live.
    - **resolution**: (optional) Voxel resolution in meters. Defaults to
      `{\"horizontal\": 2.0, \"vertical\": 1.0}`. All components must be positive.
    - **bands**: (optional) Which output bands to produce. Defaults to
      `[\"bulk_density.foliage.live\"]`. Must be non-empty and contain no
      duplicates. Branchwood and fine bands are accepted by the API, but
      Treevox currently fails those jobs with a not-implemented processing
      error.
    - **crown_profile_model**: (optional) Crown shape. Every crown runs from
      the crown base, height × (1 − crown_ratio), to the tree height.
      - `purves` (default): Purves et al. (2007), species-specific; widest at
        the crown base.
      - `beta`: species-group beta distribution; widest within the crown, per
        species group.
      - `cone`: right circular cone; widest at the crown base.
      - `cylinder`: right circular cylinder; uniform radius.
      - `single_ellipsoid`: one half-ellipsoid of revolution; widest at the
        crown base.
      - `dual_ellipsoid`: two half-ellipsoids joined at the crown midpoint;
        widest there.
      - `single_paraboloid`: one paraboloid of revolution; widest at the crown
        base.
      - `dual_paraboloid`: two paraboloids joined at the crown midpoint;
        widest there (the LANL Trees crown envelope).
    - **biomass_source**: (optional) Biomass source and requested components. The
      default uses NSVB allometry for foliage. Inventory-column sources must
      provide per-tree kg values for each requested direct component.
    - **max_crown_radius_source**: (optional) Source of each tree's maximum
      crown radius. The default, `{\"type\": \"allometry\"}`, uses the Purves et
      al. (2007) maximum crown radius for `purves` and every geometric shape
      (`cone`, `cylinder`, ellipsoids, paraboloids), so a tree's crown is
      equally wide under each of them and only the shape changes; `beta` uses
      its own allometric radius. Pass
      `{\"type\": \"inventory_column\", \"column\": <name>}` to read a per-tree
      maximum radius (m) from an inventory column (e.g. derived from LiDAR).
      The crown profile model still controls the crown shape — only the peak
      radius is rescaled. A tree with a null in that column uses its
      allometric radius.
    - **crown_geometry_source**: (optional) Where crown shapes come from.
      `{\"type\": \"parametric\"}` (default) draws every crown from
      `crown_profile_model`. `{\"type\": \"crown_feature\", \"feature_id\": <id>}`
      gives each tree with a crown in that crown Feature a measured crown,
      matched by `tree_id`:
      - Outline: the crown's CHM cells.
      - Top: each cell's CHM height.
      - Bottom: `crown_profile_model`, going up from the crown base. Profiles
        widest at the crown base give a flat bottom there; `beta` and the
        dual profiles give a bottom that rises toward the crown's edge. Each
        cell's bottom is at least one voxel below its top, but never below
        the crown base.

      `max_crown_radius_source` does not apply to measured crowns, and every
      tree keeps the mass `biomass_source` gives it. Trees with no crown in
      the Feature, trees whose crown does not contain their stem, and trees
      with no CHM height above their crown base, are drawn parametrically.
      Crowns of trees not in the inventory are ignored. The inventory must
      have a `tree_id` column, the Feature must be a completed crown Feature
      in this domain, and the CHM grid it was built from must still exist.
    - **max_bulk_density**: (optional) Upper limit on bulk density, in
      kg/m**3. In any voxel where a biomass component's bulk density, live
      and dead combined, exceeds the limit, that component's live and dead
      bulk density are scaled down to it, keeping their live/dead split, and
      `leaf_area_density` is scaled with foliage. Fuel above the limit is
      removed from the grid. Omit for no limit.
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

    With a `crown_feature` source, `source.source_chm_grid_id` and
    `source.source_chm_grid_checksum` record the crown Feature's CHM grid and
    its `checksum` at creation, and the completed grid's
    `source.crown_geometry_counts` gives the number of trees drawn with a
    measured crown (`measured`) and drawn parametrically because they had no
    crown in the Feature (`parametric_no_crown`), their crown did not contain
    their stem (`parametric_stem_outside_crown`), or they had no CHM height
    above their crown base (`parametric_no_volume`). Trees that cannot be
    drawn at all are not counted.

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
        Grid | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
