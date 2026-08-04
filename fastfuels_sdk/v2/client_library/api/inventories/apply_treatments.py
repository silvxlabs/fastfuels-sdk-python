from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apply_treatments_request import ApplyTreatmentsRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
    *,
    body: ApplyTreatmentsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/{inventory_id}/treatments".format(
            domain_id=quote(str(domain_id), safe=""),
            inventory_id=quote(str(inventory_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    if response.status_code == 200:
        response_200 = Inventory.from_dict(response.json())

        return response_200

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
    inventory_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyTreatmentsRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Apply treatments to an inventory in place

     # Apply Treatments to an Inventory (in place)

    Applies silvicultural treatments to **this** inventory in place — the
    inventory keeps its ID and the submitted treatments are appended to its
    cumulative `treatments` list, then the tree data is re-derived
    asynchronously. To keep the original data instead, duplicate the inventory
    first (`POST .../{inventory_id}/duplicate`) and treat the copy.

    A treatment thins the stand toward a target metric using a tree-selection
    method. Treatments compose: each is applied to the result of the previous.

    ## Metrics

    Each treatment is discriminated by its `metric`:

    - `diameter` — thin to a diameter-at-breast-height limit (in cm unless
      `unit` is set). `from_below` removes trees smaller than the limit;
      `from_above` removes trees larger than it.
    - `basal_area` — thin to a residual basal area (in `m**2/ha` unless `unit`
      is set). `from_below`/`from_above` remove the smallest/largest trees first
      until the target is reached; `proportional` removes across all diameter
      classes, preserving the diameter distribution.

    `proportional` is only valid for a basal-area target — it is not an option
    for a diameter limit.

    ## Units

    `value` uses the metric's native unit (`cm` for diameter, `m**2/ha` for
    basal area) unless an optional `unit` is supplied. A supplied `unit` must be
    canonical and dimensionally compatible with the native unit; it is converted
    before the treatment is applied.

    ## Spatial scoping

    An optional `conditions` list restricts the treatment to a region
    (`within`/`outside`/`intersects` a geometry or a referenced Feature, with an
    optional `buffer_m`). An empty/omitted list treats the entire inventory. A
    referenced Feature must belong to the same domain as this inventory and be
    in `completed` status; cross-domain, missing, or unfinished references are
    rejected with 422.

    Because a basal-area treatment holds its entire treated population in memory
    at once, an inventory-wide basal-area treatment over a very large domain is
    rejected with 422 — scope it with a spatial condition.

    ## Requirements

    Treatments thin against tree diameter, so the inventory must have a `dbh`
    column. Inventories derived from a canopy height model (CHM) carry only
    height and position, so treatments cannot be applied to them (422).

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted treatments appear in the inventory's
    `treatments` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued treatments are
    retained — submit another POST to retry (the new treatments are applied
    together with the retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed treatment); the inventory has no `dbh`
      column to thin against (e.g. CHM-derived); an inventory-wide basal-area
      treatment over a very large domain; or a referenced `feature_id` is
      missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyTreatmentsRequest): Request body for applying treatments to an inventory in
            place.

            Metadata (name, description, tags) is not accepted here — the inventory
            keeps its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyTreatmentsRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Apply treatments to an inventory in place

     # Apply Treatments to an Inventory (in place)

    Applies silvicultural treatments to **this** inventory in place — the
    inventory keeps its ID and the submitted treatments are appended to its
    cumulative `treatments` list, then the tree data is re-derived
    asynchronously. To keep the original data instead, duplicate the inventory
    first (`POST .../{inventory_id}/duplicate`) and treat the copy.

    A treatment thins the stand toward a target metric using a tree-selection
    method. Treatments compose: each is applied to the result of the previous.

    ## Metrics

    Each treatment is discriminated by its `metric`:

    - `diameter` — thin to a diameter-at-breast-height limit (in cm unless
      `unit` is set). `from_below` removes trees smaller than the limit;
      `from_above` removes trees larger than it.
    - `basal_area` — thin to a residual basal area (in `m**2/ha` unless `unit`
      is set). `from_below`/`from_above` remove the smallest/largest trees first
      until the target is reached; `proportional` removes across all diameter
      classes, preserving the diameter distribution.

    `proportional` is only valid for a basal-area target — it is not an option
    for a diameter limit.

    ## Units

    `value` uses the metric's native unit (`cm` for diameter, `m**2/ha` for
    basal area) unless an optional `unit` is supplied. A supplied `unit` must be
    canonical and dimensionally compatible with the native unit; it is converted
    before the treatment is applied.

    ## Spatial scoping

    An optional `conditions` list restricts the treatment to a region
    (`within`/`outside`/`intersects` a geometry or a referenced Feature, with an
    optional `buffer_m`). An empty/omitted list treats the entire inventory. A
    referenced Feature must belong to the same domain as this inventory and be
    in `completed` status; cross-domain, missing, or unfinished references are
    rejected with 422.

    Because a basal-area treatment holds its entire treated population in memory
    at once, an inventory-wide basal-area treatment over a very large domain is
    rejected with 422 — scope it with a spatial condition.

    ## Requirements

    Treatments thin against tree diameter, so the inventory must have a `dbh`
    column. Inventories derived from a canopy height model (CHM) carry only
    height and position, so treatments cannot be applied to them (422).

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted treatments appear in the inventory's
    `treatments` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued treatments are
    retained — submit another POST to retry (the new treatments are applied
    together with the retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed treatment); the inventory has no `dbh`
      column to thin against (e.g. CHM-derived); an inventory-wide basal-area
      treatment over a very large domain; or a referenced `feature_id` is
      missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyTreatmentsRequest): Request body for applying treatments to an inventory in
            place.

            Metadata (name, description, tags) is not accepted here — the inventory
            keeps its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory | QuotaExceededDetail
    """

    return sync_detailed(
        domain_id=domain_id,
        inventory_id=inventory_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyTreatmentsRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Apply treatments to an inventory in place

     # Apply Treatments to an Inventory (in place)

    Applies silvicultural treatments to **this** inventory in place — the
    inventory keeps its ID and the submitted treatments are appended to its
    cumulative `treatments` list, then the tree data is re-derived
    asynchronously. To keep the original data instead, duplicate the inventory
    first (`POST .../{inventory_id}/duplicate`) and treat the copy.

    A treatment thins the stand toward a target metric using a tree-selection
    method. Treatments compose: each is applied to the result of the previous.

    ## Metrics

    Each treatment is discriminated by its `metric`:

    - `diameter` — thin to a diameter-at-breast-height limit (in cm unless
      `unit` is set). `from_below` removes trees smaller than the limit;
      `from_above` removes trees larger than it.
    - `basal_area` — thin to a residual basal area (in `m**2/ha` unless `unit`
      is set). `from_below`/`from_above` remove the smallest/largest trees first
      until the target is reached; `proportional` removes across all diameter
      classes, preserving the diameter distribution.

    `proportional` is only valid for a basal-area target — it is not an option
    for a diameter limit.

    ## Units

    `value` uses the metric's native unit (`cm` for diameter, `m**2/ha` for
    basal area) unless an optional `unit` is supplied. A supplied `unit` must be
    canonical and dimensionally compatible with the native unit; it is converted
    before the treatment is applied.

    ## Spatial scoping

    An optional `conditions` list restricts the treatment to a region
    (`within`/`outside`/`intersects` a geometry or a referenced Feature, with an
    optional `buffer_m`). An empty/omitted list treats the entire inventory. A
    referenced Feature must belong to the same domain as this inventory and be
    in `completed` status; cross-domain, missing, or unfinished references are
    rejected with 422.

    Because a basal-area treatment holds its entire treated population in memory
    at once, an inventory-wide basal-area treatment over a very large domain is
    rejected with 422 — scope it with a spatial condition.

    ## Requirements

    Treatments thin against tree diameter, so the inventory must have a `dbh`
    column. Inventories derived from a canopy height model (CHM) carry only
    height and position, so treatments cannot be applied to them (422).

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted treatments appear in the inventory's
    `treatments` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued treatments are
    retained — submit another POST to retry (the new treatments are applied
    together with the retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed treatment); the inventory has no `dbh`
      column to thin against (e.g. CHM-derived); an inventory-wide basal-area
      treatment over a very large domain; or a referenced `feature_id` is
      missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyTreatmentsRequest): Request body for applying treatments to an inventory in
            place.

            Metadata (name, description, tags) is not accepted here — the inventory
            keeps its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Inventory | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        inventory_id=inventory_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    inventory_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyTreatmentsRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Apply treatments to an inventory in place

     # Apply Treatments to an Inventory (in place)

    Applies silvicultural treatments to **this** inventory in place — the
    inventory keeps its ID and the submitted treatments are appended to its
    cumulative `treatments` list, then the tree data is re-derived
    asynchronously. To keep the original data instead, duplicate the inventory
    first (`POST .../{inventory_id}/duplicate`) and treat the copy.

    A treatment thins the stand toward a target metric using a tree-selection
    method. Treatments compose: each is applied to the result of the previous.

    ## Metrics

    Each treatment is discriminated by its `metric`:

    - `diameter` — thin to a diameter-at-breast-height limit (in cm unless
      `unit` is set). `from_below` removes trees smaller than the limit;
      `from_above` removes trees larger than it.
    - `basal_area` — thin to a residual basal area (in `m**2/ha` unless `unit`
      is set). `from_below`/`from_above` remove the smallest/largest trees first
      until the target is reached; `proportional` removes across all diameter
      classes, preserving the diameter distribution.

    `proportional` is only valid for a basal-area target — it is not an option
    for a diameter limit.

    ## Units

    `value` uses the metric's native unit (`cm` for diameter, `m**2/ha` for
    basal area) unless an optional `unit` is supplied. A supplied `unit` must be
    canonical and dimensionally compatible with the native unit; it is converted
    before the treatment is applied.

    ## Spatial scoping

    An optional `conditions` list restricts the treatment to a region
    (`within`/`outside`/`intersects` a geometry or a referenced Feature, with an
    optional `buffer_m`). An empty/omitted list treats the entire inventory. A
    referenced Feature must belong to the same domain as this inventory and be
    in `completed` status; cross-domain, missing, or unfinished references are
    rejected with 422.

    Because a basal-area treatment holds its entire treated population in memory
    at once, an inventory-wide basal-area treatment over a very large domain is
    rejected with 422 — scope it with a spatial condition.

    ## Requirements

    Treatments thin against tree diameter, so the inventory must have a `dbh`
    column. Inventories derived from a canopy height model (CHM) carry only
    height and position, so treatments cannot be applied to them (422).

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted treatments appear in the inventory's
    `treatments` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued treatments are
    retained — submit another POST to retry (the new treatments are applied
    together with the retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed treatment); the inventory has no `dbh`
      column to thin against (e.g. CHM-derived); an inventory-wide basal-area
      treatment over a very large domain; or a referenced `feature_id` is
      missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyTreatmentsRequest): Request body for applying treatments to an inventory in
            place.

            Metadata (name, description, tags) is not accepted here — the inventory
            keeps its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Inventory | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            inventory_id=inventory_id,
            client=client,
            body=body,
        )
    ).parsed
