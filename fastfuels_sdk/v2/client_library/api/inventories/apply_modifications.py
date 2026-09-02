from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apply_modifications_request import ApplyModificationsRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.inventory import Inventory
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    inventory_id: str,
    *,
    body: ApplyModificationsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/inventories/{inventory_id}/modifications".format(
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
    body: ApplyModificationsRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Apply modifications to an inventory in place

     # Apply Modifications to an Inventory (in place)

    Applies modifications to **this** inventory in place — the inventory keeps
    its ID and the submitted rules are appended to its cumulative
    `modifications` list, then the tree data is re-derived asynchronously. To
    keep the original data instead, duplicate the inventory first
    (`POST .../{inventory_id}/duplicate`) and modify the copy.

    Modifications filter trees by conditions and apply actions (remove,
    multiply, divide, add, subtract, replace) to matching rows. Conditions
    within a single rule are ANDed together; multiple rules are evaluated
    independently in order.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    inventory** — every tree. Combined with `{\"modifier\": \"remove\"}` this
    clears the inventory of all trees; use it deliberately.

    **Attribute conditions** compare a single tree attribute against a value:
    - `attribute`: one of `dbh`, `height`, `crown_ratio`, `fia_species_code`
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`fia_species_code` only supports `eq`/`ne`)
    - `value`: number, string, or list for `eq`/`ne`
    - `unit`: (optional) pint-compatible unit string (e.g., `\"in\"`, `\"ft\"`)

    **Expression conditions** use a boolean expression:
    - `expression`: e.g., `\"dbh < 5 and height < 2\"`
    - Only `dbh`, `height`, `crown_ratio` are allowed in expressions
    - Expressions always use native units (cm, m, 0-1 fraction)

    **Spatial conditions** test each tree's location (a point) against a
    geometry. Two variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this inventory and be in `completed` status;
      cross-domain, missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing. Effectively required for
      linestring features (e.g. roads) because a tree point almost never
      intersects a bare linestring.

    Spatial conditions have **no `target` field** — trees are points, so
    the test is always point-in-(optionally-buffered)-geometry.

    Spatial and attribute conditions can be combined in a single rule
    (AND semantics). For example: `{conditions: [feature within road
    buffer, dbh > 30], actions: [remove]}` removes only large trees that
    fall inside the buffered road.

    ## Actions

    - `{\"modifier\": \"remove\"}` — remove matching trees (must be sole action)
    - `{\"attribute\": \"...\", \"modifier\": \"multiply|divide|add|subtract|replace\", \"value\": ...}`
    - `unit` on actions converts the value before applying

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted rules appear in the inventory's
    `modifications` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed modification); or a referenced `feature_id`
      is missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyModificationsRequest): Request body for applying modifications to an inventory
            in place.

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
    body: ApplyModificationsRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Apply modifications to an inventory in place

     # Apply Modifications to an Inventory (in place)

    Applies modifications to **this** inventory in place — the inventory keeps
    its ID and the submitted rules are appended to its cumulative
    `modifications` list, then the tree data is re-derived asynchronously. To
    keep the original data instead, duplicate the inventory first
    (`POST .../{inventory_id}/duplicate`) and modify the copy.

    Modifications filter trees by conditions and apply actions (remove,
    multiply, divide, add, subtract, replace) to matching rows. Conditions
    within a single rule are ANDed together; multiple rules are evaluated
    independently in order.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    inventory** — every tree. Combined with `{\"modifier\": \"remove\"}` this
    clears the inventory of all trees; use it deliberately.

    **Attribute conditions** compare a single tree attribute against a value:
    - `attribute`: one of `dbh`, `height`, `crown_ratio`, `fia_species_code`
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`fia_species_code` only supports `eq`/`ne`)
    - `value`: number, string, or list for `eq`/`ne`
    - `unit`: (optional) pint-compatible unit string (e.g., `\"in\"`, `\"ft\"`)

    **Expression conditions** use a boolean expression:
    - `expression`: e.g., `\"dbh < 5 and height < 2\"`
    - Only `dbh`, `height`, `crown_ratio` are allowed in expressions
    - Expressions always use native units (cm, m, 0-1 fraction)

    **Spatial conditions** test each tree's location (a point) against a
    geometry. Two variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this inventory and be in `completed` status;
      cross-domain, missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing. Effectively required for
      linestring features (e.g. roads) because a tree point almost never
      intersects a bare linestring.

    Spatial conditions have **no `target` field** — trees are points, so
    the test is always point-in-(optionally-buffered)-geometry.

    Spatial and attribute conditions can be combined in a single rule
    (AND semantics). For example: `{conditions: [feature within road
    buffer, dbh > 30], actions: [remove]}` removes only large trees that
    fall inside the buffered road.

    ## Actions

    - `{\"modifier\": \"remove\"}` — remove matching trees (must be sole action)
    - `{\"attribute\": \"...\", \"modifier\": \"multiply|divide|add|subtract|replace\", \"value\": ...}`
    - `unit` on actions converts the value before applying

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted rules appear in the inventory's
    `modifications` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed modification); or a referenced `feature_id`
      is missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyModificationsRequest): Request body for applying modifications to an inventory
            in place.

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
    body: ApplyModificationsRequest,
) -> Response[HTTPValidationError | Inventory | QuotaExceededDetail]:
    r"""Apply modifications to an inventory in place

     # Apply Modifications to an Inventory (in place)

    Applies modifications to **this** inventory in place — the inventory keeps
    its ID and the submitted rules are appended to its cumulative
    `modifications` list, then the tree data is re-derived asynchronously. To
    keep the original data instead, duplicate the inventory first
    (`POST .../{inventory_id}/duplicate`) and modify the copy.

    Modifications filter trees by conditions and apply actions (remove,
    multiply, divide, add, subtract, replace) to matching rows. Conditions
    within a single rule are ANDed together; multiple rules are evaluated
    independently in order.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    inventory** — every tree. Combined with `{\"modifier\": \"remove\"}` this
    clears the inventory of all trees; use it deliberately.

    **Attribute conditions** compare a single tree attribute against a value:
    - `attribute`: one of `dbh`, `height`, `crown_ratio`, `fia_species_code`
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`fia_species_code` only supports `eq`/`ne`)
    - `value`: number, string, or list for `eq`/`ne`
    - `unit`: (optional) pint-compatible unit string (e.g., `\"in\"`, `\"ft\"`)

    **Expression conditions** use a boolean expression:
    - `expression`: e.g., `\"dbh < 5 and height < 2\"`
    - Only `dbh`, `height`, `crown_ratio` are allowed in expressions
    - Expressions always use native units (cm, m, 0-1 fraction)

    **Spatial conditions** test each tree's location (a point) against a
    geometry. Two variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this inventory and be in `completed` status;
      cross-domain, missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing. Effectively required for
      linestring features (e.g. roads) because a tree point almost never
      intersects a bare linestring.

    Spatial conditions have **no `target` field** — trees are points, so
    the test is always point-in-(optionally-buffered)-geometry.

    Spatial and attribute conditions can be combined in a single rule
    (AND semantics). For example: `{conditions: [feature within road
    buffer, dbh > 30], actions: [remove]}` removes only large trees that
    fall inside the buffered road.

    ## Actions

    - `{\"modifier\": \"remove\"}` — remove matching trees (must be sole action)
    - `{\"attribute\": \"...\", \"modifier\": \"multiply|divide|add|subtract|replace\", \"value\": ...}`
    - `unit` on actions converts the value before applying

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted rules appear in the inventory's
    `modifications` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed modification); or a referenced `feature_id`
      is missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyModificationsRequest): Request body for applying modifications to an inventory
            in place.

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
    body: ApplyModificationsRequest,
) -> HTTPValidationError | Inventory | QuotaExceededDetail | None:
    r"""Apply modifications to an inventory in place

     # Apply Modifications to an Inventory (in place)

    Applies modifications to **this** inventory in place — the inventory keeps
    its ID and the submitted rules are appended to its cumulative
    `modifications` list, then the tree data is re-derived asynchronously. To
    keep the original data instead, duplicate the inventory first
    (`POST .../{inventory_id}/duplicate`) and modify the copy.

    Modifications filter trees by conditions and apply actions (remove,
    multiply, divide, add, subtract, replace) to matching rows. Conditions
    within a single rule are ANDed together; multiple rules are evaluated
    independently in order.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    inventory** — every tree. Combined with `{\"modifier\": \"remove\"}` this
    clears the inventory of all trees; use it deliberately.

    **Attribute conditions** compare a single tree attribute against a value:
    - `attribute`: one of `dbh`, `height`, `crown_ratio`, `fia_species_code`
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`fia_species_code` only supports `eq`/`ne`)
    - `value`: number, string, or list for `eq`/`ne`
    - `unit`: (optional) pint-compatible unit string (e.g., `\"in\"`, `\"ft\"`)

    **Expression conditions** use a boolean expression:
    - `expression`: e.g., `\"dbh < 5 and height < 2\"`
    - Only `dbh`, `height`, `crown_ratio` are allowed in expressions
    - Expressions always use native units (cm, m, 0-1 fraction)

    **Spatial conditions** test each tree's location (a point) against a
    geometry. Two variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this inventory and be in `completed` status;
      cross-domain, missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing. Effectively required for
      linestring features (e.g. roads) because a tree point almost never
      intersects a bare linestring.

    Spatial conditions have **no `target` field** — trees are points, so
    the test is always point-in-(optionally-buffered)-geometry.

    Spatial and attribute conditions can be combined in a single rule
    (AND semantics). For example: `{conditions: [feature within road
    buffer, dbh > 30], actions: [remove]}` removes only large trees that
    fall inside the buffered road.

    ## Actions

    - `{\"modifier\": \"remove\"}` — remove matching trees (must be sole action)
    - `{\"attribute\": \"...\", \"modifier\": \"multiply|divide|add|subtract|replace\", \"value\": ...}`
    - `unit` on actions converts the value before applying

    ## Response

    Returns this inventory (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it can detect that the
    source has changed. The submitted rules appear in the inventory's
    `modifications` list once processing completes — poll the inventory until
    status returns to `\"completed\"`.

    If processing fails, the inventory's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The inventory does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The inventory is not in `completed` status
      (and is not a retryable failed modification); or a referenced `feature_id`
      is missing, cross-domain, or not completed.
    - **429 Too Many Requests**: You have too many active inventory jobs in
      progress (your `max_active_inventories` quota). Wait for jobs to complete
      or delete unneeded inventories, then retry. The response detail names the
      exact `quota` and includes a `Retry-After` header.

    Args:
        domain_id (str):
        inventory_id (str):
        body (ApplyModificationsRequest): Request body for applying modifications to an inventory
            in place.

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
