from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_pim_chm_fusion_inventory_request import (
    CreatePimChmFusionInventoryRequest,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreatePimChmFusionInventoryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/tree/pim/fusion/chm".format(
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
    body: CreatePimChmFusionInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by fusing a PIM with a CHM

     # Create PIM-CHM Fusion Inventory

    Expands a Plot Imputation Map (PIM) into individual tree records, conditioned
    on a Canopy Height Model (CHM). The path names the fused sources; the
    ``method`` object names the algorithm.

    ## Method: `reimputation` (default)

    The v1 fusion algorithm:

    1. Resample the PIM to ``method.resolution``.
    2. Compute the CHM's canopy cover per resampled cell — the fraction of CHM
       cells taller than ``method.min_height``.
    3. Keep a cell's plot only where cover exceeds ``method.cover_threshold``;
       cells at or below become gaps with no trees.
    4. Expand the surviving plots into trees exactly as ``tree/pim`` does.

    The result preserves each plot's species composition and size distributions
    while restricting trees to where the CHM actually shows canopy.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **source_chm_grid_id**: (required) ID of a completed CHM grid (band `chm`,
      unit meters).
    - **method**: (optional) Fusion algorithm and its parameters. Defaults to
      `reimputation`.
    - **seed**: (optional) Random seed for reproducibility. Random if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **modifications** / **treatments**: (optional) Applied after expansion,
      as on ``tree/pim``.
    - **type**, **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) processes the fusion asynchronously and sets status to
    ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimChmFusionInventoryRequest): Request body for creating an inventory by
            fusing a PIM with a CHM.

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
    body: CreatePimChmFusionInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by fusing a PIM with a CHM

     # Create PIM-CHM Fusion Inventory

    Expands a Plot Imputation Map (PIM) into individual tree records, conditioned
    on a Canopy Height Model (CHM). The path names the fused sources; the
    ``method`` object names the algorithm.

    ## Method: `reimputation` (default)

    The v1 fusion algorithm:

    1. Resample the PIM to ``method.resolution``.
    2. Compute the CHM's canopy cover per resampled cell — the fraction of CHM
       cells taller than ``method.min_height``.
    3. Keep a cell's plot only where cover exceeds ``method.cover_threshold``;
       cells at or below become gaps with no trees.
    4. Expand the surviving plots into trees exactly as ``tree/pim`` does.

    The result preserves each plot's species composition and size distributions
    while restricting trees to where the CHM actually shows canopy.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **source_chm_grid_id**: (required) ID of a completed CHM grid (band `chm`,
      unit meters).
    - **method**: (optional) Fusion algorithm and its parameters. Defaults to
      `reimputation`.
    - **seed**: (optional) Random seed for reproducibility. Random if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **modifications** / **treatments**: (optional) Applied after expansion,
      as on ``tree/pim``.
    - **type**, **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) processes the fusion asynchronously and sets status to
    ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimChmFusionInventoryRequest): Request body for creating an inventory by
            fusing a PIM with a CHM.

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
    body: CreatePimChmFusionInventoryRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Create an inventory by fusing a PIM with a CHM

     # Create PIM-CHM Fusion Inventory

    Expands a Plot Imputation Map (PIM) into individual tree records, conditioned
    on a Canopy Height Model (CHM). The path names the fused sources; the
    ``method`` object names the algorithm.

    ## Method: `reimputation` (default)

    The v1 fusion algorithm:

    1. Resample the PIM to ``method.resolution``.
    2. Compute the CHM's canopy cover per resampled cell — the fraction of CHM
       cells taller than ``method.min_height``.
    3. Keep a cell's plot only where cover exceeds ``method.cover_threshold``;
       cells at or below become gaps with no trees.
    4. Expand the surviving plots into trees exactly as ``tree/pim`` does.

    The result preserves each plot's species composition and size distributions
    while restricting trees to where the CHM actually shows canopy.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **source_chm_grid_id**: (required) ID of a completed CHM grid (band `chm`,
      unit meters).
    - **method**: (optional) Fusion algorithm and its parameters. Defaults to
      `reimputation`.
    - **seed**: (optional) Random seed for reproducibility. Random if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **modifications** / **treatments**: (optional) Applied after expansion,
      as on ``tree/pim``.
    - **type**, **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) processes the fusion asynchronously and sets status to
    ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimChmFusionInventoryRequest): Request body for creating an inventory by
            fusing a PIM with a CHM.

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
    body: CreatePimChmFusionInventoryRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Create an inventory by fusing a PIM with a CHM

     # Create PIM-CHM Fusion Inventory

    Expands a Plot Imputation Map (PIM) into individual tree records, conditioned
    on a Canopy Height Model (CHM). The path names the fused sources; the
    ``method`` object names the algorithm.

    ## Method: `reimputation` (default)

    The v1 fusion algorithm:

    1. Resample the PIM to ``method.resolution``.
    2. Compute the CHM's canopy cover per resampled cell — the fraction of CHM
       cells taller than ``method.min_height``.
    3. Keep a cell's plot only where cover exceeds ``method.cover_threshold``;
       cells at or below become gaps with no trees.
    4. Expand the surviving plots into trees exactly as ``tree/pim`` does.

    The result preserves each plot's species composition and size distributions
    while restricting trees to where the CHM actually shows canopy.

    ## Request Body

    - **source_pim_grid_id**: (required) ID of a completed PIM grid.
    - **source_chm_grid_id**: (required) ID of a completed CHM grid (band `chm`,
      unit meters).
    - **method**: (optional) Fusion algorithm and its parameters. Defaults to
      `reimputation`.
    - **seed**: (optional) Random seed for reproducibility. Random if omitted.
    - **point_process**: (optional) Spatial point process for coordinate
      assignment. Default: ``\"inhomogeneous_poisson\"``.
    - **modifications** / **treatments**: (optional) Applied after expansion,
      as on ``tree/pim``.
    - **type**, **name**, **description**, **tags**: (optional) Metadata.

    ## Response

    Returns the created Inventory resource with status ``\"pending\"``. The backend
    (Standgen) processes the fusion asynchronously and sets status to
    ``\"completed\"`` when ready.

    Args:
        domain_id (str):
        body (CreatePimChmFusionInventoryRequest): Request body for creating an inventory by
            fusing a PIM with a CHM.

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
