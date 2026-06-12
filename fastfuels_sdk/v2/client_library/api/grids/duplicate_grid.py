from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.duplicate_grid_request import DuplicateGridRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    grid_id: str,
    *,
    body: DuplicateGridRequest | None | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/{grid_id}/duplicate".format(
            domain_id=quote(str(domain_id), safe=""),
            grid_id=quote(str(grid_id), safe=""),
        ),
    }

    if isinstance(body, DuplicateGridRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body

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
    grid_id: str,
    *,
    client: AuthenticatedClient,
    body: DuplicateGridRequest | None | Unset = UNSET,
) -> Response[Grid | HTTPValidationError]:
    r"""Duplicate a grid

     # Duplicate a Grid

    Creates an independent **copy** of a completed grid under a new ID. Use
    this to branch a scenario: duplicate, then edit the copy while the
    original stays untouched.

    This is a true clone, not a re-derivation. The finished data is
    byte-copied; no regeneration is performed and the upstream source is never
    re-fetched, so the copy is exact even if the upstream product has been
    updated since the original was built. The copy carries over the source's
    `source`, `modifications`, `bands`, `georeference`, `chunks`, and
    `checksum` verbatim — only its `id` and timestamps differ.

    ## Request Body (optional)

    All fields are optional. Any field omitted is carried over from the source.

    - **name**: Name for the copy.
    - **description**: Description for the copy.
    - **tags**: Tags for the copy.

    Send no body at all to copy the metadata unchanged.

    ## Response

    Returns the new Grid with status `\"pending\"`. The data is copied in the
    background; the status transitions to `\"completed\"` once the copy finishes
    (or `\"failed\"` if it does not). Data endpoints (`/chunks`, `/data`) become
    available only after the copy completes. The source grid is unchanged.

    ## Error Responses

    - **404 Not Found**: The source grid does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The source grid exists but is not yet
      `completed`, so there is no finished artifact to copy.

    Args:
        domain_id (str):
        grid_id (str):
        body (DuplicateGridRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: DuplicateGridRequest | None | Unset = UNSET,
) -> Grid | HTTPValidationError | None:
    r"""Duplicate a grid

     # Duplicate a Grid

    Creates an independent **copy** of a completed grid under a new ID. Use
    this to branch a scenario: duplicate, then edit the copy while the
    original stays untouched.

    This is a true clone, not a re-derivation. The finished data is
    byte-copied; no regeneration is performed and the upstream source is never
    re-fetched, so the copy is exact even if the upstream product has been
    updated since the original was built. The copy carries over the source's
    `source`, `modifications`, `bands`, `georeference`, `chunks`, and
    `checksum` verbatim — only its `id` and timestamps differ.

    ## Request Body (optional)

    All fields are optional. Any field omitted is carried over from the source.

    - **name**: Name for the copy.
    - **description**: Description for the copy.
    - **tags**: Tags for the copy.

    Send no body at all to copy the metadata unchanged.

    ## Response

    Returns the new Grid with status `\"pending\"`. The data is copied in the
    background; the status transitions to `\"completed\"` once the copy finishes
    (or `\"failed\"` if it does not). Data endpoints (`/chunks`, `/data`) become
    available only after the copy completes. The source grid is unchanged.

    ## Error Responses

    - **404 Not Found**: The source grid does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The source grid exists but is not yet
      `completed`, so there is no finished artifact to copy.

    Args:
        domain_id (str):
        grid_id (str):
        body (DuplicateGridRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
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
    body: DuplicateGridRequest | None | Unset = UNSET,
) -> Response[Grid | HTTPValidationError]:
    r"""Duplicate a grid

     # Duplicate a Grid

    Creates an independent **copy** of a completed grid under a new ID. Use
    this to branch a scenario: duplicate, then edit the copy while the
    original stays untouched.

    This is a true clone, not a re-derivation. The finished data is
    byte-copied; no regeneration is performed and the upstream source is never
    re-fetched, so the copy is exact even if the upstream product has been
    updated since the original was built. The copy carries over the source's
    `source`, `modifications`, `bands`, `georeference`, `chunks`, and
    `checksum` verbatim — only its `id` and timestamps differ.

    ## Request Body (optional)

    All fields are optional. Any field omitted is carried over from the source.

    - **name**: Name for the copy.
    - **description**: Description for the copy.
    - **tags**: Tags for the copy.

    Send no body at all to copy the metadata unchanged.

    ## Response

    Returns the new Grid with status `\"pending\"`. The data is copied in the
    background; the status transitions to `\"completed\"` once the copy finishes
    (or `\"failed\"` if it does not). Data endpoints (`/chunks`, `/data`) become
    available only after the copy completes. The source grid is unchanged.

    ## Error Responses

    - **404 Not Found**: The source grid does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The source grid exists but is not yet
      `completed`, so there is no finished artifact to copy.

    Args:
        domain_id (str):
        grid_id (str):
        body (DuplicateGridRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: DuplicateGridRequest | None | Unset = UNSET,
) -> Grid | HTTPValidationError | None:
    r"""Duplicate a grid

     # Duplicate a Grid

    Creates an independent **copy** of a completed grid under a new ID. Use
    this to branch a scenario: duplicate, then edit the copy while the
    original stays untouched.

    This is a true clone, not a re-derivation. The finished data is
    byte-copied; no regeneration is performed and the upstream source is never
    re-fetched, so the copy is exact even if the upstream product has been
    updated since the original was built. The copy carries over the source's
    `source`, `modifications`, `bands`, `georeference`, `chunks`, and
    `checksum` verbatim — only its `id` and timestamps differ.

    ## Request Body (optional)

    All fields are optional. Any field omitted is carried over from the source.

    - **name**: Name for the copy.
    - **description**: Description for the copy.
    - **tags**: Tags for the copy.

    Send no body at all to copy the metadata unchanged.

    ## Response

    Returns the new Grid with status `\"pending\"`. The data is copied in the
    background; the status transitions to `\"completed\"` once the copy finishes
    (or `\"failed\"` if it does not). Data endpoints (`/chunks`, `/data`) become
    available only after the copy completes. The source grid is unchanged.

    ## Error Responses

    - **404 Not Found**: The source grid does not exist, is not owned by the
      caller, or is not in this domain.
    - **422 Unprocessable Content**: The source grid exists but is not yet
      `completed`, so there is no finished artifact to copy.

    Args:
        domain_id (str):
        grid_id (str):
        body (DuplicateGridRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            grid_id=grid_id,
            client=client,
            body=body,
        )
    ).parsed
