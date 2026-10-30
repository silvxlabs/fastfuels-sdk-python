from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_gdam_allometry_request import CreateGdamAllometryRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateGdamAllometryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/tree/allometry/gdam".format(
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
    body: CreateGdamAllometryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    species and uncompacted crown ratio — from simple stem metrics (position and
    height). It replaces legacy region-specific allometric equations with a
    single national generative model: each predicted value is one draw from the
    predicted distribution given the values you already supply. Every tree is treated as visible from
    above, as trees
    detected on a canopy height model are.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the morphology columns (diameter, crown ratio, species, crown base height)
    of an existing tree inventory. With the default ``gdam``
    ``crown_base_height_model`` GDAM predicts the crown base too; any other
    model computes it from the final species, diameter, crown ratio and height.
    GDAM covers the conterminous US; an inventory with a tree outside it fails.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM conditions on every dbh, crown ratio and species column the
    source has, and on its crown base height with the ``gdam`` model, except
    those being overwritten.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``,
      ``crown_base_height``. Narrow it (e.g. ``[\"fia_species_code\"]``) to impute
      fewer columns and write less to disk; columns left out are not imputed.
      With a ``crown_base_height_model`` other than ``gdam``, requesting
      ``crown_base_height`` requires each of ``dbh``, ``crown_ratio`` and
      ``fia_species_code`` to be imputed too or to be a column of the source
      inventory. Must be non-empty with no duplicates.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      values and fills only empty cells. ``true`` replaces every tree's value in
      ``impute_columns``, and GDAM does not see the old values. With a model
      other than ``gdam``, overwriting ``crown_ratio`` without
      ``crown_base_height`` leaves crown bases that no longer match the new
      crown ratios.
    - **crown_base_height_model**: (optional) The model that gives
      ``crown_base_height``, selected by ``name``. Defaults to
      ``{\"name\": \"gdam\"}``: GDAM predicts it with the other columns. The other
      models compute it from species, dbh, crown ratio and height.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height above zero, in metres (``m``).

    **Imputable** (select via ``impute_columns``):

    - **dbh**: diameter at breast height, in centimetres (``cm``). Predicted by
      GDAM.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction), as
      recorded by FIA field crews. Predicted by GDAM.
    - **fia_species_code**: FIA species code. Predicted by GDAM.
    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height`` for
      a tree with no live crown. Predicted by GDAM with the ``gdam`` model.
      Any other ``crown_base_height_model`` computes it from each tree's final
      species, crown ratio, diameter and height; species the model does not
      cover get no value, and with only ``crown_base_height`` requested no GDAM
      call is made.

    ## Source

    The created inventory's ``source`` records ``impute_columns``,
    ``overwrite``, ``crown_base_height_model`` and ``conditioned_columns`` (the
    source columns GDAM conditioned on, including ``crown_base_height`` when
    the ``gdam`` model was sent it).

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamAllometryRequest): Request body for creating an inventory via GDAM
            allometry imputation.

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
    body: CreateGdamAllometryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    species and uncompacted crown ratio — from simple stem metrics (position and
    height). It replaces legacy region-specific allometric equations with a
    single national generative model: each predicted value is one draw from the
    predicted distribution given the values you already supply. Every tree is treated as visible from
    above, as trees
    detected on a canopy height model are.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the morphology columns (diameter, crown ratio, species, crown base height)
    of an existing tree inventory. With the default ``gdam``
    ``crown_base_height_model`` GDAM predicts the crown base too; any other
    model computes it from the final species, diameter, crown ratio and height.
    GDAM covers the conterminous US; an inventory with a tree outside it fails.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM conditions on every dbh, crown ratio and species column the
    source has, and on its crown base height with the ``gdam`` model, except
    those being overwritten.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``,
      ``crown_base_height``. Narrow it (e.g. ``[\"fia_species_code\"]``) to impute
      fewer columns and write less to disk; columns left out are not imputed.
      With a ``crown_base_height_model`` other than ``gdam``, requesting
      ``crown_base_height`` requires each of ``dbh``, ``crown_ratio`` and
      ``fia_species_code`` to be imputed too or to be a column of the source
      inventory. Must be non-empty with no duplicates.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      values and fills only empty cells. ``true`` replaces every tree's value in
      ``impute_columns``, and GDAM does not see the old values. With a model
      other than ``gdam``, overwriting ``crown_ratio`` without
      ``crown_base_height`` leaves crown bases that no longer match the new
      crown ratios.
    - **crown_base_height_model**: (optional) The model that gives
      ``crown_base_height``, selected by ``name``. Defaults to
      ``{\"name\": \"gdam\"}``: GDAM predicts it with the other columns. The other
      models compute it from species, dbh, crown ratio and height.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height above zero, in metres (``m``).

    **Imputable** (select via ``impute_columns``):

    - **dbh**: diameter at breast height, in centimetres (``cm``). Predicted by
      GDAM.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction), as
      recorded by FIA field crews. Predicted by GDAM.
    - **fia_species_code**: FIA species code. Predicted by GDAM.
    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height`` for
      a tree with no live crown. Predicted by GDAM with the ``gdam`` model.
      Any other ``crown_base_height_model`` computes it from each tree's final
      species, crown ratio, diameter and height; species the model does not
      cover get no value, and with only ``crown_base_height`` requested no GDAM
      call is made.

    ## Source

    The created inventory's ``source`` records ``impute_columns``,
    ``overwrite``, ``crown_base_height_model`` and ``conditioned_columns`` (the
    source columns GDAM conditioned on, including ``crown_base_height`` when
    the ``gdam`` model was sent it).

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamAllometryRequest): Request body for creating an inventory via GDAM
            allometry imputation.

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
    body: CreateGdamAllometryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    species and uncompacted crown ratio — from simple stem metrics (position and
    height). It replaces legacy region-specific allometric equations with a
    single national generative model: each predicted value is one draw from the
    predicted distribution given the values you already supply. Every tree is treated as visible from
    above, as trees
    detected on a canopy height model are.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the morphology columns (diameter, crown ratio, species, crown base height)
    of an existing tree inventory. With the default ``gdam``
    ``crown_base_height_model`` GDAM predicts the crown base too; any other
    model computes it from the final species, diameter, crown ratio and height.
    GDAM covers the conterminous US; an inventory with a tree outside it fails.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM conditions on every dbh, crown ratio and species column the
    source has, and on its crown base height with the ``gdam`` model, except
    those being overwritten.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``,
      ``crown_base_height``. Narrow it (e.g. ``[\"fia_species_code\"]``) to impute
      fewer columns and write less to disk; columns left out are not imputed.
      With a ``crown_base_height_model`` other than ``gdam``, requesting
      ``crown_base_height`` requires each of ``dbh``, ``crown_ratio`` and
      ``fia_species_code`` to be imputed too or to be a column of the source
      inventory. Must be non-empty with no duplicates.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      values and fills only empty cells. ``true`` replaces every tree's value in
      ``impute_columns``, and GDAM does not see the old values. With a model
      other than ``gdam``, overwriting ``crown_ratio`` without
      ``crown_base_height`` leaves crown bases that no longer match the new
      crown ratios.
    - **crown_base_height_model**: (optional) The model that gives
      ``crown_base_height``, selected by ``name``. Defaults to
      ``{\"name\": \"gdam\"}``: GDAM predicts it with the other columns. The other
      models compute it from species, dbh, crown ratio and height.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height above zero, in metres (``m``).

    **Imputable** (select via ``impute_columns``):

    - **dbh**: diameter at breast height, in centimetres (``cm``). Predicted by
      GDAM.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction), as
      recorded by FIA field crews. Predicted by GDAM.
    - **fia_species_code**: FIA species code. Predicted by GDAM.
    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height`` for
      a tree with no live crown. Predicted by GDAM with the ``gdam`` model.
      Any other ``crown_base_height_model`` computes it from each tree's final
      species, crown ratio, diameter and height; species the model does not
      cover get no value, and with only ``crown_base_height`` requested no GDAM
      call is made.

    ## Source

    The created inventory's ``source`` records ``impute_columns``,
    ``overwrite``, ``crown_base_height_model`` and ``conditioned_columns`` (the
    source columns GDAM conditioned on, including ``crown_base_height`` when
    the ``gdam`` model was sent it).

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamAllometryRequest): Request body for creating an inventory via GDAM
            allometry imputation.

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
    body: CreateGdamAllometryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    species and uncompacted crown ratio — from simple stem metrics (position and
    height). It replaces legacy region-specific allometric equations with a
    single national generative model: each predicted value is one draw from the
    predicted distribution given the values you already supply. Every tree is treated as visible from
    above, as trees
    detected on a canopy height model are.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the morphology columns (diameter, crown ratio, species, crown base height)
    of an existing tree inventory. With the default ``gdam``
    ``crown_base_height_model`` GDAM predicts the crown base too; any other
    model computes it from the final species, diameter, crown ratio and height.
    GDAM covers the conterminous US; an inventory with a tree outside it fails.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM conditions on every dbh, crown ratio and species column the
    source has, and on its crown base height with the ``gdam`` model, except
    those being overwritten.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``,
      ``crown_base_height``. Narrow it (e.g. ``[\"fia_species_code\"]``) to impute
      fewer columns and write less to disk; columns left out are not imputed.
      With a ``crown_base_height_model`` other than ``gdam``, requesting
      ``crown_base_height`` requires each of ``dbh``, ``crown_ratio`` and
      ``fia_species_code`` to be imputed too or to be a column of the source
      inventory. Must be non-empty with no duplicates.
    - **overwrite**: (optional, default ``false``) ``false`` keeps existing
      values and fills only empty cells. ``true`` replaces every tree's value in
      ``impute_columns``, and GDAM does not see the old values. With a model
      other than ``gdam``, overwriting ``crown_ratio`` without
      ``crown_base_height`` leaves crown bases that no longer match the new
      crown ratios.
    - **crown_base_height_model**: (optional) The model that gives
      ``crown_base_height``, selected by ``name``. Defaults to
      ``{\"name\": \"gdam\"}``: GDAM predicts it with the other columns. The other
      models compute it from species, dbh, crown ratio and height.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height above zero, in metres (``m``).

    **Imputable** (select via ``impute_columns``):

    - **dbh**: diameter at breast height, in centimetres (``cm``). Predicted by
      GDAM.
    - **crown_ratio**: FIA compacted live crown ratio (0–1 fraction), as
      recorded by FIA field crews. Predicted by GDAM.
    - **fia_species_code**: FIA species code. Predicted by GDAM.
    - **crown_base_height**: height of the lowest live foliage, in metres
      (``m``): the base of a continuous, gap-free crown, equal to ``height`` for
      a tree with no live crown. Predicted by GDAM with the ``gdam`` model.
      Any other ``crown_base_height_model`` computes it from each tree's final
      species, crown ratio, diameter and height; species the model does not
      cover get no value, and with only ``crown_base_height`` requested no GDAM
      call is made.

    ## Source

    The created inventory's ``source`` records ``impute_columns``,
    ``overwrite``, ``crown_base_height_model`` and ``conditioned_columns`` (the
    source columns GDAM conditioned on, including ``crown_base_height`` when
    the ``gdam`` model was sent it).

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamAllometryRequest): Request body for creating an inventory via GDAM
            allometry imputation.

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
