from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_crown_base_height_inventory_request import (
    CreateCrownBaseHeightInventoryRequest,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateCrownBaseHeightInventoryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/tree/allometry/crown_base_height".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    if response.status_code == 201:
        response_201 = Inventory.from_dict(response.json())

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
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
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
    body: CreateCrownBaseHeightInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by computing crown base heights

     # Create Crown Base Height Inventory

    Creates a new tree inventory with each tree's crown base height computed
    from its species, dbh, crown ratio and height by a crown base height
    equation, or predicted by GDAM with the ``gdam`` model. Use it for a tree
    inventory without a crown base height, such as an uploaded inventory,
    before voxelizing it or building canopy grids from it.

    With an equation, an inventory without dbh, crown ratio or species needs
    the GDAM route (``POST /domains/{domain_id}/inventories/tree/allometry/gdam``)
    instead, which fills those and the crown base height in one request. The
    ``gdam`` model needs only position and height, conditions on whichever of
    species, dbh, crown ratio and crown base height are present, and writes
    only the crown base height. GDAM covers the conterminous US; an inventory
    with a tree outside it fails.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory
      with the required columns below.
    - **model**: (optional) The crown base height model, selected by ``name``.
      Defaults to ``{\"name\": \"fia_national_logit_2026\"}``. Species an equation
      does not cover get no crown base height. ``{\"name\": \"gdam\"}`` predicts it
      with GDAM.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      crown base heights and fills only empty cells; a source where every tree
      already has one is rejected. ``true`` recomputes every tree's crown base
      height, and ``gdam`` is not given the old values.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory**, with a value for every tree:

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``); above zero for ``gdam``.
    - **dbh**: diameter at breast height, in centimetres (``cm``). Not
      required for ``gdam``.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction). Not
      required for ``gdam``.
    - **fia_species_code**: FIA species code. Not required for ``gdam``.

    **Written**:

    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height``
      for a tree with no live crown.

    Every other source column is copied unchanged.

    ## Source

    The created inventory's ``source`` records ``model`` and ``overwrite``.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) computes the crown base heights asynchronously and
    updates status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateCrownBaseHeightInventoryRequest): Request body for creating an inventory with
            model-computed crown base
            heights.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory | QuotaExceededDetail]
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
    body: CreateCrownBaseHeightInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by computing crown base heights

     # Create Crown Base Height Inventory

    Creates a new tree inventory with each tree's crown base height computed
    from its species, dbh, crown ratio and height by a crown base height
    equation, or predicted by GDAM with the ``gdam`` model. Use it for a tree
    inventory without a crown base height, such as an uploaded inventory,
    before voxelizing it or building canopy grids from it.

    With an equation, an inventory without dbh, crown ratio or species needs
    the GDAM route (``POST /domains/{domain_id}/inventories/tree/allometry/gdam``)
    instead, which fills those and the crown base height in one request. The
    ``gdam`` model needs only position and height, conditions on whichever of
    species, dbh, crown ratio and crown base height are present, and writes
    only the crown base height. GDAM covers the conterminous US; an inventory
    with a tree outside it fails.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory
      with the required columns below.
    - **model**: (optional) The crown base height model, selected by ``name``.
      Defaults to ``{\"name\": \"fia_national_logit_2026\"}``. Species an equation
      does not cover get no crown base height. ``{\"name\": \"gdam\"}`` predicts it
      with GDAM.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      crown base heights and fills only empty cells; a source where every tree
      already has one is rejected. ``true`` recomputes every tree's crown base
      height, and ``gdam`` is not given the old values.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory**, with a value for every tree:

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``); above zero for ``gdam``.
    - **dbh**: diameter at breast height, in centimetres (``cm``). Not
      required for ``gdam``.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction). Not
      required for ``gdam``.
    - **fia_species_code**: FIA species code. Not required for ``gdam``.

    **Written**:

    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height``
      for a tree with no live crown.

    Every other source column is copied unchanged.

    ## Source

    The created inventory's ``source`` records ``model`` and ``overwrite``.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) computes the crown base heights asynchronously and
    updates status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateCrownBaseHeightInventoryRequest): Request body for creating an inventory with
            model-computed crown base
            heights.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory | QuotaExceededDetail
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
    body: CreateCrownBaseHeightInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by computing crown base heights

     # Create Crown Base Height Inventory

    Creates a new tree inventory with each tree's crown base height computed
    from its species, dbh, crown ratio and height by a crown base height
    equation, or predicted by GDAM with the ``gdam`` model. Use it for a tree
    inventory without a crown base height, such as an uploaded inventory,
    before voxelizing it or building canopy grids from it.

    With an equation, an inventory without dbh, crown ratio or species needs
    the GDAM route (``POST /domains/{domain_id}/inventories/tree/allometry/gdam``)
    instead, which fills those and the crown base height in one request. The
    ``gdam`` model needs only position and height, conditions on whichever of
    species, dbh, crown ratio and crown base height are present, and writes
    only the crown base height. GDAM covers the conterminous US; an inventory
    with a tree outside it fails.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory
      with the required columns below.
    - **model**: (optional) The crown base height model, selected by ``name``.
      Defaults to ``{\"name\": \"fia_national_logit_2026\"}``. Species an equation
      does not cover get no crown base height. ``{\"name\": \"gdam\"}`` predicts it
      with GDAM.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      crown base heights and fills only empty cells; a source where every tree
      already has one is rejected. ``true`` recomputes every tree's crown base
      height, and ``gdam`` is not given the old values.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory**, with a value for every tree:

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``); above zero for ``gdam``.
    - **dbh**: diameter at breast height, in centimetres (``cm``). Not
      required for ``gdam``.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction). Not
      required for ``gdam``.
    - **fia_species_code**: FIA species code. Not required for ``gdam``.

    **Written**:

    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height``
      for a tree with no live crown.

    Every other source column is copied unchanged.

    ## Source

    The created inventory's ``source`` records ``model`` and ``overwrite``.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) computes the crown base heights asynchronously and
    updates status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateCrownBaseHeightInventoryRequest): Request body for creating an inventory with
            model-computed crown base
            heights.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory | QuotaExceededDetail]
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
    body: CreateCrownBaseHeightInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by computing crown base heights

     # Create Crown Base Height Inventory

    Creates a new tree inventory with each tree's crown base height computed
    from its species, dbh, crown ratio and height by a crown base height
    equation, or predicted by GDAM with the ``gdam`` model. Use it for a tree
    inventory without a crown base height, such as an uploaded inventory,
    before voxelizing it or building canopy grids from it.

    With an equation, an inventory without dbh, crown ratio or species needs
    the GDAM route (``POST /domains/{domain_id}/inventories/tree/allometry/gdam``)
    instead, which fills those and the crown base height in one request. The
    ``gdam`` model needs only position and height, conditions on whichever of
    species, dbh, crown ratio and crown base height are present, and writes
    only the crown base height. GDAM covers the conterminous US; an inventory
    with a tree outside it fails.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory
      with the required columns below.
    - **model**: (optional) The crown base height model, selected by ``name``.
      Defaults to ``{\"name\": \"fia_national_logit_2026\"}``. Species an equation
      does not cover get no crown base height. ``{\"name\": \"gdam\"}`` predicts it
      with GDAM.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      crown base heights and fills only empty cells; a source where every tree
      already has one is rejected. ``true`` recomputes every tree's crown base
      height, and ``gdam`` is not given the old values.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory**, with a value for every tree:

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``); above zero for ``gdam``.
    - **dbh**: diameter at breast height, in centimetres (``cm``). Not
      required for ``gdam``.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction). Not
      required for ``gdam``.
    - **fia_species_code**: FIA species code. Not required for ``gdam``.

    **Written**:

    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height``
      for a tree with no live crown.

    Every other source column is copied unchanged.

    ## Source

    The created inventory's ``source`` records ``model`` and ``overwrite``.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The
    backend (Standgen) computes the crown base heights asynchronously and
    updates status to ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreateCrownBaseHeightInventoryRequest): Request body for creating an inventory with
            model-computed crown base
            heights.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
