from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.landfire_coverage_response import LandfireCoverageResponse
from ...types import Response


def _get_kwargs(
    domain_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/domains/{domain_id}/grids/fccs/landfire/coverage".format(
            domain_id=quote(str(domain_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | LandfireCoverageResponse | None:
    if response.status_code == 200:
        response_200 = LandfireCoverageResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | LandfireCoverageResponse]:
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
) -> Response[HTTPValidationError | LandfireCoverageResponse]:
    """Check LANDFIRE FCCS release coverage for a domain

     # Check LANDFIRE FCCS Coverage

    Immediate pre-flight check reporting every FCCS release the API serves
    and how much of this domain each one covers. Staged annual releases are
    national; the current-year release is served by LANDFIRE Product Service
    region by region, so its coverage depends on where the domain is.

    ## Response

    `latest` is the release representing the most recent point in time that
    fully covers the domain. `releases` lists every release, newest first.
    Each release that covers the domain carries a `links.create` request:
    send its `body` to its `href`, a path relative to this API's base URL,
    to create the grid.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LandfireCoverageResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | LandfireCoverageResponse | None:
    """Check LANDFIRE FCCS release coverage for a domain

     # Check LANDFIRE FCCS Coverage

    Immediate pre-flight check reporting every FCCS release the API serves
    and how much of this domain each one covers. Staged annual releases are
    national; the current-year release is served by LANDFIRE Product Service
    region by region, so its coverage depends on where the domain is.

    ## Response

    `latest` is the release representing the most recent point in time that
    fully covers the domain. `releases` lists every release, newest first.
    Each release that covers the domain carries a `links.create` request:
    send its `body` to its `href`, a path relative to this API's base URL,
    to create the grid.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LandfireCoverageResponse
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | LandfireCoverageResponse]:
    """Check LANDFIRE FCCS release coverage for a domain

     # Check LANDFIRE FCCS Coverage

    Immediate pre-flight check reporting every FCCS release the API serves
    and how much of this domain each one covers. Staged annual releases are
    national; the current-year release is served by LANDFIRE Product Service
    region by region, so its coverage depends on where the domain is.

    ## Response

    `latest` is the release representing the most recent point in time that
    fully covers the domain. `releases` lists every release, newest first.
    Each release that covers the domain carries a `links.create` request:
    send its `body` to its `href`, a path relative to this API's base URL,
    to create the grid.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LandfireCoverageResponse]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | LandfireCoverageResponse | None:
    """Check LANDFIRE FCCS release coverage for a domain

     # Check LANDFIRE FCCS Coverage

    Immediate pre-flight check reporting every FCCS release the API serves
    and how much of this domain each one covers. Staged annual releases are
    national; the current-year release is served by LANDFIRE Product Service
    region by region, so its coverage depends on where the domain is.

    ## Response

    `latest` is the release representing the most recent point in time that
    fully covers the domain. `releases` lists every release, newest first.
    Each release that covers the domain carries a `links.create` request:
    send its `body` to its `href`, a path relative to this API's base URL,
    to create the grid.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LandfireCoverageResponse
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
        )
    ).parsed
