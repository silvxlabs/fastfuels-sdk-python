from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export import Export
from ...models.http_validation_error import HTTPValidationError
from ...models.quicfire_export_request import QuicfireExportRequest
from ...types import Response


def _get_kwargs(
    domain_id: str,
    *,
    body: QuicfireExportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/domains/{domain_id}/grids/exports/quicfire".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Export | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = Export.from_dict(response.json())

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
) -> Response[Export | HTTPValidationError]:
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
    body: QuicfireExportRequest,
) -> Response[Export | HTTPValidationError]:
    """Export combined fuel + topography grids to QUIC-Fire format

     Bundle surface fuel + canopy fuel + (optional) topography grids into a
    QUIC-Fire-loadable zip archive.

    The output zip contains `treesrhof.dat`, `treesmoist.dat`,
    `treesfueldepth.dat`, `metadata.json`, and `domain.geojson` always; plus
    `topo.dat` when a topography role is provided, plus `treesss.dat` when
    both canopy and surface SAVR roles are provided.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (QuicfireExportRequest): Request body for creating a QUIC-Fire combined export.

            Five required roles produce `treesrhof.dat`, `treesmoist.dat`, and
            `treesfueldepth.dat`. `topography` (optional) produces `topo.dat`. The
            SAVR pair (optional, both-or-neither) produces `treesss.dat`.

            The fire grid is defined by the `alignment` field — either the Domain
            bounding box padded to `(dx, dy)` (with `dz` vertical), or the lattice
            of an existing grid. Every role grid must be lattice-aligned to this
            fire grid and cover its full extent; otherwise the request is rejected.
            The exporter only crops oversized roles by integer slicing — it never
            resamples or reprojects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
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
    body: QuicfireExportRequest,
) -> Export | HTTPValidationError | None:
    """Export combined fuel + topography grids to QUIC-Fire format

     Bundle surface fuel + canopy fuel + (optional) topography grids into a
    QUIC-Fire-loadable zip archive.

    The output zip contains `treesrhof.dat`, `treesmoist.dat`,
    `treesfueldepth.dat`, `metadata.json`, and `domain.geojson` always; plus
    `topo.dat` when a topography role is provided, plus `treesss.dat` when
    both canopy and surface SAVR roles are provided.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (QuicfireExportRequest): Request body for creating a QUIC-Fire combined export.

            Five required roles produce `treesrhof.dat`, `treesmoist.dat`, and
            `treesfueldepth.dat`. `topography` (optional) produces `topo.dat`. The
            SAVR pair (optional, both-or-neither) produces `treesss.dat`.

            The fire grid is defined by the `alignment` field — either the Domain
            bounding box padded to `(dx, dy)` (with `dz` vertical), or the lattice
            of an existing grid. Every role grid must be lattice-aligned to this
            fire grid and cover its full extent; otherwise the request is rejected.
            The exporter only crops oversized roles by integer slicing — it never
            resamples or reprojects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError
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
    body: QuicfireExportRequest,
) -> Response[Export | HTTPValidationError]:
    """Export combined fuel + topography grids to QUIC-Fire format

     Bundle surface fuel + canopy fuel + (optional) topography grids into a
    QUIC-Fire-loadable zip archive.

    The output zip contains `treesrhof.dat`, `treesmoist.dat`,
    `treesfueldepth.dat`, `metadata.json`, and `domain.geojson` always; plus
    `topo.dat` when a topography role is provided, plus `treesss.dat` when
    both canopy and surface SAVR roles are provided.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (QuicfireExportRequest): Request body for creating a QUIC-Fire combined export.

            Five required roles produce `treesrhof.dat`, `treesmoist.dat`, and
            `treesfueldepth.dat`. `topography` (optional) produces `topo.dat`. The
            SAVR pair (optional, both-or-neither) produces `treesss.dat`.

            The fire grid is defined by the `alignment` field — either the Domain
            bounding box padded to `(dx, dy)` (with `dz` vertical), or the lattice
            of an existing grid. Every role grid must be lattice-aligned to this
            fire grid and cover its full extent; otherwise the request is rejected.
            The exporter only crops oversized roles by integer slicing — it never
            resamples or reprojects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Export | HTTPValidationError]
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
    body: QuicfireExportRequest,
) -> Export | HTTPValidationError | None:
    """Export combined fuel + topography grids to QUIC-Fire format

     Bundle surface fuel + canopy fuel + (optional) topography grids into a
    QUIC-Fire-loadable zip archive.

    The output zip contains `treesrhof.dat`, `treesmoist.dat`,
    `treesfueldepth.dat`, `metadata.json`, and `domain.geojson` always; plus
    `topo.dat` when a topography role is provided, plus `treesss.dat` when
    both canopy and surface SAVR roles are provided.

    Returns an Export resource with status `pending`. Poll
    `GET /exports/{export_id}` until status is `completed` to retrieve the
    signed download URL.

    Args:
        domain_id (str):
        body (QuicfireExportRequest): Request body for creating a QUIC-Fire combined export.

            Five required roles produce `treesrhof.dat`, `treesmoist.dat`, and
            `treesfueldepth.dat`. `topography` (optional) produces `topo.dat`. The
            SAVR pair (optional, both-or-neither) produces `treesss.dat`.

            The fire grid is defined by the `alignment` field — either the Domain
            bounding box padded to `(dx, dy)` (with `dz` vertical), or the lattice
            of an existing grid. Every role grid must be lattice-aligned to this
            fire grid and cover its full extent; otherwise the request is rejected.
            The exporter only crops oversized roles by integer slicing — it never
            resamples or reprojects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Export | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            body=body,
        )
    ).parsed
