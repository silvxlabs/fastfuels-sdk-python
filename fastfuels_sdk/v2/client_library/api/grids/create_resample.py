from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_resample_request import CreateResampleRequest
from ...models.grid import Grid
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: CreateResampleRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/resample".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

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
    *,
    client: AuthenticatedClient,
    body: CreateResampleRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a grid by resampling an existing grid

     # Create Resampled Grid

    Resamples an existing grid to a new spatial resolution and/or anchor.
    This is the key operation for unifying grids on a common lattice
    (e.g., LANDFIRE 30m to 2m for QUIC-Fire input).

    The resampled grid propagates ``domain_id`` and bands from the source grid.

    ## Request Body

    - **source_grid_id**: (required) Grid to resample. Must have status
      \"completed\" and a georeference.
    - **alignment**: Output alignment target. Default ``target=\"domain\"``.
      ``alignment.resolution`` is required for ``target=\"domain\"`` and
      ``target=\"native\"``; optional for ``target=\"grid\"`` (defaults to the
      target grid's exact transform/shape).
    - **method_overrides**: (optional) Per-band resampling method overrides.
    - **name**, **description**, **tags**: (optional)

    ## Response

    Returns the created Grid with status \"pending\". The backend performs the
    resampling and updates status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateResampleRequest): Request to create a grid by resampling an existing grid.

            Unlike entry-point grid creation requests, ``domain_id`` is not required
            because derived grids carry the same domain reference as their source.

            The ``alignment`` field controls the output lattice. ``alignment.resolution``
            is required for ``target="domain"`` and ``target="native"``; for
            ``target="grid"`` it is optional (defaults to the target grid's exact
            transform/shape; if supplied, keeps the target's CRS and origin and
            recomputes shape at the new cell size).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: CreateResampleRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a grid by resampling an existing grid

     # Create Resampled Grid

    Resamples an existing grid to a new spatial resolution and/or anchor.
    This is the key operation for unifying grids on a common lattice
    (e.g., LANDFIRE 30m to 2m for QUIC-Fire input).

    The resampled grid propagates ``domain_id`` and bands from the source grid.

    ## Request Body

    - **source_grid_id**: (required) Grid to resample. Must have status
      \"completed\" and a georeference.
    - **alignment**: Output alignment target. Default ``target=\"domain\"``.
      ``alignment.resolution`` is required for ``target=\"domain\"`` and
      ``target=\"native\"``; optional for ``target=\"grid\"`` (defaults to the
      target grid's exact transform/shape).
    - **method_overrides**: (optional) Per-band resampling method overrides.
    - **name**, **description**, **tags**: (optional)

    ## Response

    Returns the created Grid with status \"pending\". The backend performs the
    resampling and updates status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateResampleRequest): Request to create a grid by resampling an existing grid.

            Unlike entry-point grid creation requests, ``domain_id`` is not required
            because derived grids carry the same domain reference as their source.

            The ``alignment`` field controls the output lattice. ``alignment.resolution``
            is required for ``target="domain"`` and ``target="native"``; for
            ``target="grid"`` it is optional (defaults to the target grid's exact
            transform/shape; if supplied, keeps the target's CRS and origin and
            recomputes shape at the new cell size).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
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
    body: CreateResampleRequest,
) -> Response[Grid | HTTPValidationError]:
    r"""Create a grid by resampling an existing grid

     # Create Resampled Grid

    Resamples an existing grid to a new spatial resolution and/or anchor.
    This is the key operation for unifying grids on a common lattice
    (e.g., LANDFIRE 30m to 2m for QUIC-Fire input).

    The resampled grid propagates ``domain_id`` and bands from the source grid.

    ## Request Body

    - **source_grid_id**: (required) Grid to resample. Must have status
      \"completed\" and a georeference.
    - **alignment**: Output alignment target. Default ``target=\"domain\"``.
      ``alignment.resolution`` is required for ``target=\"domain\"`` and
      ``target=\"native\"``; optional for ``target=\"grid\"`` (defaults to the
      target grid's exact transform/shape).
    - **method_overrides**: (optional) Per-band resampling method overrides.
    - **name**, **description**, **tags**: (optional)

    ## Response

    Returns the created Grid with status \"pending\". The backend performs the
    resampling and updates status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateResampleRequest): Request to create a grid by resampling an existing grid.

            Unlike entry-point grid creation requests, ``domain_id`` is not required
            because derived grids carry the same domain reference as their source.

            The ``alignment`` field controls the output lattice. ``alignment.resolution``
            is required for ``target="domain"`` and ``target="native"``; for
            ``target="grid"`` it is optional (defaults to the target grid's exact
            transform/shape; if supplied, keeps the target's CRS and origin and
            recomputes shape at the new cell size).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Grid | HTTPValidationError]
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
    body: CreateResampleRequest,
) -> Grid | HTTPValidationError | None:
    r"""Create a grid by resampling an existing grid

     # Create Resampled Grid

    Resamples an existing grid to a new spatial resolution and/or anchor.
    This is the key operation for unifying grids on a common lattice
    (e.g., LANDFIRE 30m to 2m for QUIC-Fire input).

    The resampled grid propagates ``domain_id`` and bands from the source grid.

    ## Request Body

    - **source_grid_id**: (required) Grid to resample. Must have status
      \"completed\" and a georeference.
    - **alignment**: Output alignment target. Default ``target=\"domain\"``.
      ``alignment.resolution`` is required for ``target=\"domain\"`` and
      ``target=\"native\"``; optional for ``target=\"grid\"`` (defaults to the
      target grid's exact transform/shape).
    - **method_overrides**: (optional) Per-band resampling method overrides.
    - **name**, **description**, **tags**: (optional)

    ## Response

    Returns the created Grid with status \"pending\". The backend performs the
    resampling and updates status to \"completed\" when ready.

    Args:
        domain_id (str):
        body (CreateResampleRequest): Request to create a grid by resampling an existing grid.

            Unlike entry-point grid creation requests, ``domain_id`` is not required
            because derived grids carry the same domain reference as their source.

            The ``alignment`` field controls the output lattice. ``alignment.resolution``
            is required for ``target="domain"`` and ``target="native"``; for
            ``target="grid"`` it is optional (defaults to the target grid's exact
            transform/shape; if supplied, keeps the target's CRS and origin and
            recomputes shape at the new cell size).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Grid | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
