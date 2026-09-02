from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apply_grid_modifications_request import ApplyGridModificationsRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...models.quota_exceeded_detail import QuotaExceededDetail
from ...types import Response


def _get_kwargs(
    domain_id: str,
    grid_id: str,
    *,
    body: ApplyGridModificationsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/{grid_id}/modifications".format(
            domain_id=quote(str(domain_id), safe=""),
            grid_id=quote(str(grid_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    if response.status_code == 200:
        response_200 = Grid.from_dict(response.json())

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
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyGridModificationsRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Apply modifications to a grid in place

     # Apply Modifications to a Grid (in place)

    Applies modification rules to **this** grid in place — the grid keeps its
    ID and the submitted rules are applied on top of its current data
    asynchronously. To keep the original data instead, duplicate the grid
    first (`POST .../{grid_id}/duplicate`) and modify the copy.

    The grid's stored data is updated directly; the upstream source (LANDFIRE,
    3DEP, ...) is **not** re-fetched, so cells your rules don't touch are
    byte-for-byte unchanged — even if the upstream product has been updated
    since the grid was built.

    Modifications select cells by conditions and apply actions to the matching
    cells.

    ## Combining conditions: AND within a rule, OR across rules

    Each rule's `conditions` are **ANDed** — a cell is selected only when it
    satisfies *every* condition in that rule. Adding a condition to a rule
    therefore **narrows** the selection (the intersection). Example: a feature
    condition plus an attribute condition matches cells inside the feature
    **and** above a value threshold.

    There is **no OR within a rule**. To act on a **union** — \"roads *or*
    water bodies\", \"GR1 *or* GR2 cells\" — use **multiple rules**. Rules are
    applied independently and in order, so a cell matched by *any* rule is
    affected. Adding a rule therefore **widens** the overall selection.

    Putting two mutually exclusive conditions in one rule (e.g. a road feature
    AND a water feature) is the classic mistake: it selects cells that are
    both at once — usually none. Split them into one rule per feature instead.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    grid** — every cell. Use it for a blanket adjustment (e.g. subtract a
    constant from every cell); add conditions to narrow the selection.

    **Attribute conditions** compare a band's cell values against a value:
    - `band`: dot-notation band key (e.g., `fbfm`, `fuel_load.1hr`)
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`eq`/`ne` also accept a list of values)
    - `value`: number or list for `eq`/`ne`. For `fbfm` bands you may use the
      human-readable Scott-Burgan labels (`\"GR1\"`) or the numeric codes (`101`)
      interchangeably — labels are resolved to codes when the rule is stored.

    **Spatial conditions** test each cell's location against a geometry. Two
    variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this grid and be in `completed` status; cross-domain,
      missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing.
    - `target`: `centroid` (default) tests the cell center; `cell` tests the
      cell's full footprint — use it with linestring features (e.g. roads)
      so every crossed cell matches.

    ## Actions

    - `{\"band\": \"...\", \"modifier\": \"replace|multiply|divide|add|subtract\", \"value\": ...}`
    - Non-`replace` results are clamped at zero (grid bands are physical
      quantities).

    ## Response

    Returns this grid (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it (resample, lookup,
    exports) can detect that the source has changed. The submitted rules
    appear in the grid's `modifications` list once processing completes —
    poll the grid until status returns to `\"completed\"`.

    If processing fails, the grid's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not owned by the caller,
      or is not in this domain.
    - **422 Unprocessable Content**: The grid is not in `completed` status
      (and is not a retryable failed modification); the grid is a 3D voxel
      grid (apply modifications to the source tree inventory and re-voxelize
      instead); a referenced `feature_id` is missing, cross-domain, or not
      completed; or a referenced band does not exist on this grid.
    - **429 Too Many Requests**: You have too many active grid jobs in progress
      (your `max_active_grids` quota). Wait for jobs to complete or delete
      unneeded grids, then retry. The response detail names the exact `quota`
      and includes a `Retry-After` header.

    Args:
        domain_id (str):
        grid_id (str):
        body (ApplyGridModificationsRequest): Request body for applying modifications to a grid in
            place.

            Metadata (name, description, tags) is not accepted here — the grid keeps
            its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyGridModificationsRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Apply modifications to a grid in place

     # Apply Modifications to a Grid (in place)

    Applies modification rules to **this** grid in place — the grid keeps its
    ID and the submitted rules are applied on top of its current data
    asynchronously. To keep the original data instead, duplicate the grid
    first (`POST .../{grid_id}/duplicate`) and modify the copy.

    The grid's stored data is updated directly; the upstream source (LANDFIRE,
    3DEP, ...) is **not** re-fetched, so cells your rules don't touch are
    byte-for-byte unchanged — even if the upstream product has been updated
    since the grid was built.

    Modifications select cells by conditions and apply actions to the matching
    cells.

    ## Combining conditions: AND within a rule, OR across rules

    Each rule's `conditions` are **ANDed** — a cell is selected only when it
    satisfies *every* condition in that rule. Adding a condition to a rule
    therefore **narrows** the selection (the intersection). Example: a feature
    condition plus an attribute condition matches cells inside the feature
    **and** above a value threshold.

    There is **no OR within a rule**. To act on a **union** — \"roads *or*
    water bodies\", \"GR1 *or* GR2 cells\" — use **multiple rules**. Rules are
    applied independently and in order, so a cell matched by *any* rule is
    affected. Adding a rule therefore **widens** the overall selection.

    Putting two mutually exclusive conditions in one rule (e.g. a road feature
    AND a water feature) is the classic mistake: it selects cells that are
    both at once — usually none. Split them into one rule per feature instead.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    grid** — every cell. Use it for a blanket adjustment (e.g. subtract a
    constant from every cell); add conditions to narrow the selection.

    **Attribute conditions** compare a band's cell values against a value:
    - `band`: dot-notation band key (e.g., `fbfm`, `fuel_load.1hr`)
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`eq`/`ne` also accept a list of values)
    - `value`: number or list for `eq`/`ne`. For `fbfm` bands you may use the
      human-readable Scott-Burgan labels (`\"GR1\"`) or the numeric codes (`101`)
      interchangeably — labels are resolved to codes when the rule is stored.

    **Spatial conditions** test each cell's location against a geometry. Two
    variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this grid and be in `completed` status; cross-domain,
      missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing.
    - `target`: `centroid` (default) tests the cell center; `cell` tests the
      cell's full footprint — use it with linestring features (e.g. roads)
      so every crossed cell matches.

    ## Actions

    - `{\"band\": \"...\", \"modifier\": \"replace|multiply|divide|add|subtract\", \"value\": ...}`
    - Non-`replace` results are clamped at zero (grid bands are physical
      quantities).

    ## Response

    Returns this grid (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it (resample, lookup,
    exports) can detect that the source has changed. The submitted rules
    appear in the grid's `modifications` list once processing completes —
    poll the grid until status returns to `\"completed\"`.

    If processing fails, the grid's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not owned by the caller,
      or is not in this domain.
    - **422 Unprocessable Content**: The grid is not in `completed` status
      (and is not a retryable failed modification); the grid is a 3D voxel
      grid (apply modifications to the source tree inventory and re-voxelize
      instead); a referenced `feature_id` is missing, cross-domain, or not
      completed; or a referenced band does not exist on this grid.
    - **429 Too Many Requests**: You have too many active grid jobs in progress
      (your `max_active_grids` quota). Wait for jobs to complete or delete
      unneeded grids, then retry. The response detail names the exact `quota`
      and includes a `Retry-After` header.

    Args:
        domain_id (str):
        grid_id (str):
        body (ApplyGridModificationsRequest): Request body for applying modifications to a grid in
            place.

            Metadata (name, description, tags) is not accepted here — the grid keeps
            its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError | QuotaExceededDetail
    """

    return sync_detailed(
        domain_id=domain_id,
        grid_id=grid_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyGridModificationsRequest,
) -> Response[Grid | HTTPValidationError | QuotaExceededDetail]:
    r"""Apply modifications to a grid in place

     # Apply Modifications to a Grid (in place)

    Applies modification rules to **this** grid in place — the grid keeps its
    ID and the submitted rules are applied on top of its current data
    asynchronously. To keep the original data instead, duplicate the grid
    first (`POST .../{grid_id}/duplicate`) and modify the copy.

    The grid's stored data is updated directly; the upstream source (LANDFIRE,
    3DEP, ...) is **not** re-fetched, so cells your rules don't touch are
    byte-for-byte unchanged — even if the upstream product has been updated
    since the grid was built.

    Modifications select cells by conditions and apply actions to the matching
    cells.

    ## Combining conditions: AND within a rule, OR across rules

    Each rule's `conditions` are **ANDed** — a cell is selected only when it
    satisfies *every* condition in that rule. Adding a condition to a rule
    therefore **narrows** the selection (the intersection). Example: a feature
    condition plus an attribute condition matches cells inside the feature
    **and** above a value threshold.

    There is **no OR within a rule**. To act on a **union** — \"roads *or*
    water bodies\", \"GR1 *or* GR2 cells\" — use **multiple rules**. Rules are
    applied independently and in order, so a cell matched by *any* rule is
    affected. Adding a rule therefore **widens** the overall selection.

    Putting two mutually exclusive conditions in one rule (e.g. a road feature
    AND a water feature) is the classic mistake: it selects cells that are
    both at once — usually none. Split them into one rule per feature instead.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    grid** — every cell. Use it for a blanket adjustment (e.g. subtract a
    constant from every cell); add conditions to narrow the selection.

    **Attribute conditions** compare a band's cell values against a value:
    - `band`: dot-notation band key (e.g., `fbfm`, `fuel_load.1hr`)
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`eq`/`ne` also accept a list of values)
    - `value`: number or list for `eq`/`ne`. For `fbfm` bands you may use the
      human-readable Scott-Burgan labels (`\"GR1\"`) or the numeric codes (`101`)
      interchangeably — labels are resolved to codes when the rule is stored.

    **Spatial conditions** test each cell's location against a geometry. Two
    variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this grid and be in `completed` status; cross-domain,
      missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing.
    - `target`: `centroid` (default) tests the cell center; `cell` tests the
      cell's full footprint — use it with linestring features (e.g. roads)
      so every crossed cell matches.

    ## Actions

    - `{\"band\": \"...\", \"modifier\": \"replace|multiply|divide|add|subtract\", \"value\": ...}`
    - Non-`replace` results are clamped at zero (grid bands are physical
      quantities).

    ## Response

    Returns this grid (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it (resample, lookup,
    exports) can detect that the source has changed. The submitted rules
    appear in the grid's `modifications` list once processing completes —
    poll the grid until status returns to `\"completed\"`.

    If processing fails, the grid's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not owned by the caller,
      or is not in this domain.
    - **422 Unprocessable Content**: The grid is not in `completed` status
      (and is not a retryable failed modification); the grid is a 3D voxel
      grid (apply modifications to the source tree inventory and re-voxelize
      instead); a referenced `feature_id` is missing, cross-domain, or not
      completed; or a referenced band does not exist on this grid.
    - **429 Too Many Requests**: You have too many active grid jobs in progress
      (your `max_active_grids` quota). Wait for jobs to complete or delete
      unneeded grids, then retry. The response detail names the exact `quota`
      and includes a `Retry-After` header.

    Args:
        domain_id (str):
        grid_id (str):
        body (ApplyGridModificationsRequest): Request body for applying modifications to a grid in
            place.

            Metadata (name, description, tags) is not accepted here — the grid keeps
            its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError | QuotaExceededDetail]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        grid_id=grid_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    grid_id: str,
    *,
    client: AuthenticatedClient,
    body: ApplyGridModificationsRequest,
) -> Grid | HTTPValidationError | QuotaExceededDetail | None:
    r"""Apply modifications to a grid in place

     # Apply Modifications to a Grid (in place)

    Applies modification rules to **this** grid in place — the grid keeps its
    ID and the submitted rules are applied on top of its current data
    asynchronously. To keep the original data instead, duplicate the grid
    first (`POST .../{grid_id}/duplicate`) and modify the copy.

    The grid's stored data is updated directly; the upstream source (LANDFIRE,
    3DEP, ...) is **not** re-fetched, so cells your rules don't touch are
    byte-for-byte unchanged — even if the upstream product has been updated
    since the grid was built.

    Modifications select cells by conditions and apply actions to the matching
    cells.

    ## Combining conditions: AND within a rule, OR across rules

    Each rule's `conditions` are **ANDed** — a cell is selected only when it
    satisfies *every* condition in that rule. Adding a condition to a rule
    therefore **narrows** the selection (the intersection). Example: a feature
    condition plus an attribute condition matches cells inside the feature
    **and** above a value threshold.

    There is **no OR within a rule**. To act on a **union** — \"roads *or*
    water bodies\", \"GR1 *or* GR2 cells\" — use **multiple rules**. Rules are
    applied independently and in order, so a cell matched by *any* rule is
    affected. Adding a rule therefore **widens** the overall selection.

    Putting two mutually exclusive conditions in one rule (e.g. a road feature
    AND a water feature) is the classic mistake: it selects cells that are
    both at once — usually none. Split them into one rule per feature instead.

    ## Conditions

    A rule with an **empty `conditions` list applies its actions to the whole
    grid** — every cell. Use it for a blanket adjustment (e.g. subtract a
    constant from every cell); add conditions to narrow the selection.

    **Attribute conditions** compare a band's cell values against a value:
    - `band`: dot-notation band key (e.g., `fbfm`, `fuel_load.1hr`)
    - `operator`: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
      (`eq`/`ne` also accept a list of values)
    - `value`: number or list for `eq`/`ne`. For `fbfm` bands you may use the
      human-readable Scott-Burgan labels (`\"GR1\"`) or the numeric codes (`101`)
      interchangeably — labels are resolved to codes when the rule is stored.

    **Spatial conditions** test each cell's location against a geometry. Two
    variants discriminated by the required `source` field:

    - `source: \"geometry\"` — supply GeoJSON directly via `geometry` (plus
      optional `crs`; defaults to the domain CRS).
    - `source: \"feature\"` — reference a persisted Feature resource by
      `feature_id` (road, water, layerset). The Feature must belong to the
      same domain as this grid and be in `completed` status; cross-domain,
      missing, or unfinished references are rejected with 422.

    Both spatial variants accept:
    - `operator`: `within`, `outside`, or `intersects`
    - `buffer_m`: (optional, meters) expands the geometry outward in the
      domain's projected CRS before testing.
    - `target`: `centroid` (default) tests the cell center; `cell` tests the
      cell's full footprint — use it with linestring features (e.g. roads)
      so every crossed cell matches.

    ## Actions

    - `{\"band\": \"...\", \"modifier\": \"replace|multiply|divide|add|subtract\", \"value\": ...}`
    - Non-`replace` results are clamped at zero (grid bands are physical
      quantities).

    ## Response

    Returns this grid (same ID) with status `\"pending\"`. Its `checksum`
    changes immediately, so any resource derived from it (resample, lookup,
    exports) can detect that the source has changed. The submitted rules
    appear in the grid's `modifications` list once processing completes —
    poll the grid until status returns to `\"completed\"`.

    If processing fails, the grid's status becomes `\"failed\"` with error
    details, the stored data is unchanged, and the queued rules are retained —
    submit another POST to retry (the new rules are applied together with the
    retained ones).

    ## Error Responses

    - **404 Not Found**: The grid does not exist, is not owned by the caller,
      or is not in this domain.
    - **422 Unprocessable Content**: The grid is not in `completed` status
      (and is not a retryable failed modification); the grid is a 3D voxel
      grid (apply modifications to the source tree inventory and re-voxelize
      instead); a referenced `feature_id` is missing, cross-domain, or not
      completed; or a referenced band does not exist on this grid.
    - **429 Too Many Requests**: You have too many active grid jobs in progress
      (your `max_active_grids` quota). Wait for jobs to complete or delete
      unneeded grids, then retry. The response detail names the exact `quota`
      and includes a `Retry-After` header.

    Args:
        domain_id (str):
        grid_id (str):
        body (ApplyGridModificationsRequest): Request body for applying modifications to a grid in
            place.

            Metadata (name, description, tags) is not accepted here — the grid keeps
            its identity; use PATCH to edit metadata.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError | QuotaExceededDetail
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            grid_id=grid_id,
            client=client,
            body=body,
        )
    ).parsed
