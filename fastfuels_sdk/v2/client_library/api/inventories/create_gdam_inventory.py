from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_gdam_inventory_request import CreateGdamInventoryRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateGdamInventoryRequest,
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
    body: CreateGdamInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    and species — from simple stem metrics (position and height). It replaces
    legacy region-specific allometric equations with a single generative model:
    each tree is routed to a region-specific model by geography, and a masked
    tabular autoencoder fills in every missing field in one pass while preserving
    any values you already supply.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the missing morphology columns (diameter, crown ratio, species) of an existing
    tree inventory.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM predicts the missing fields; any values already present are
    preserved and passed to GDAM as conditioning inputs.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``. Narrow it (e.g.
      ``[\"fia_species_code\"]``) to impute fewer columns and write less to disk;
      columns left out are not imputed. Must be non-empty with no duplicates.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``).

    **Imputable by GDAM** (select via ``impute_columns``) — filled only where
    missing; existing values are preserved:

    - **dbh**: diameter at breast height, in centimetres (``cm``).
    - **crown_ratio**: live crown ratio, as a 0–1 fraction.
    - **fia_species_code**: FIA species code.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamInventoryRequest): Request body for creating an inventory via GDAM
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
    body: CreateGdamInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    and species — from simple stem metrics (position and height). It replaces
    legacy region-specific allometric equations with a single generative model:
    each tree is routed to a region-specific model by geography, and a masked
    tabular autoencoder fills in every missing field in one pass while preserving
    any values you already supply.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the missing morphology columns (diameter, crown ratio, species) of an existing
    tree inventory.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM predicts the missing fields; any values already present are
    preserved and passed to GDAM as conditioning inputs.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``. Narrow it (e.g.
      ``[\"fia_species_code\"]``) to impute fewer columns and write less to disk;
      columns left out are not imputed. Must be non-empty with no duplicates.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``).

    **Imputable by GDAM** (select via ``impute_columns``) — filled only where
    missing; existing values are preserved:

    - **dbh**: diameter at breast height, in centimetres (``cm``).
    - **crown_ratio**: live crown ratio, as a 0–1 fraction.
    - **fia_species_code**: FIA species code.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamInventoryRequest): Request body for creating an inventory via GDAM
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
    body: CreateGdamInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    and species — from simple stem metrics (position and height). It replaces
    legacy region-specific allometric equations with a single generative model:
    each tree is routed to a region-specific model by geography, and a masked
    tabular autoencoder fills in every missing field in one pass while preserving
    any values you already supply.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the missing morphology columns (diameter, crown ratio, species) of an existing
    tree inventory.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM predicts the missing fields; any values already present are
    preserved and passed to GDAM as conditioning inputs.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``. Narrow it (e.g.
      ``[\"fia_species_code\"]``) to impute fewer columns and write less to disk;
      columns left out are not imputed. Must be non-empty with no duplicates.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``).

    **Imputable by GDAM** (select via ``impute_columns``) — filled only where
    missing; existing values are preserved:

    - **dbh**: diameter at breast height, in centimetres (``cm``).
    - **crown_ratio**: live crown ratio, as a 0–1 fraction.
    - **fia_species_code**: FIA species code.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamInventoryRequest): Request body for creating an inventory via GDAM
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
    body: CreateGdamInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by filling in another via GDAM

     # Create GDAM Allometry Inventory

    **GDAM (Generalized Dendro Allometric Model)** is a machine-learning model
    that predicts tree morphology — diameter at breast height, live crown ratio,
    and species — from simple stem metrics (position and height). It replaces
    legacy region-specific allometric equations with a single generative model:
    each tree is routed to a region-specific model by geography, and a masked
    tabular autoencoder fills in every missing field in one pass while preserving
    any values you already supply.

    This endpoint creates a new tree inventory by calling the GDAM API to fill in
    the missing morphology columns (diameter, crown ratio, species) of an existing
    tree inventory.

    The typical input is an uploaded **position + height** inventory (`x`, `y`,
    `height`). GDAM predicts the missing fields; any values already present are
    preserved and passed to GDAM as conditioning inputs.

    ## Request Body

    - **source_tree_inventory_id**: (required) ID of a completed tree inventory to
      fill in.
    - **impute_columns**: (optional) Which morphology columns to impute. Defaults
      to all of ``dbh``, ``crown_ratio``, ``fia_species_code``. Narrow it (e.g.
      ``[\"fia_species_code\"]``) to impute fewer columns and write less to disk;
      columns left out are not imputed. Must be non-empty with no duplicates.
    - **name**: (optional) Name for the inventory.
    - **description**: (optional) Description.
    - **tags**: (optional) Tags for organizing inventories.

    ## Columns

    **Required on the source inventory** (the typical uploaded position+height set):

    - **x**, **y**: tree position, in the domain CRS.
    - **height**: tree height, in metres (``m``).

    **Imputable by GDAM** (select via ``impute_columns``) — filled only where
    missing; existing values are preserved:

    - **dbh**: diameter at breast height, in centimetres (``cm``).
    - **crown_ratio**: live crown ratio, as a 0–1 fraction.
    - **fia_species_code**: FIA species code.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) calls GDAM asynchronously and updates status to ``\"completed\"`` when
    ready.

    Args:
        domain_id (str):
        body (CreateGdamInventoryRequest): Request body for creating an inventory via GDAM
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
