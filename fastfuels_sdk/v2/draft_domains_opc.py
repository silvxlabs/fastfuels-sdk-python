"""
fastfuels_sdk/v2/draft_domains_opc.py

DRAFT — Domain wrapper built on the **openapi-python-client** client
(`client_library`: attrs models + httpx).

Part of the v2 client-library generator comparison; see COMPARISON.md.
Mirrors the v1 wrapper ergonomics: a Domain class extending the generated
model with classmethod constructors and instance methods.

v1 parity notes:
- `from_geojson`/`from_geodataframe` lose `horizontal_resolution`/
  `vertical_resolution` (resolution moved to grids in v2) and gain
  `tags`/`pad_to_resolution`.
- `from_file` is new convenience (v1 users went through geopandas manually).
- v1's `export()` has no v2 endpoint equivalent (no
  `/domains/{id}/export` in the v2 spec) and is omitted.
- v2-only endpoints (preview_domain, reproject_domain, get_domain_lattice)
  are not wrapped yet — out of scope for the generator comparison.
"""

import json
import os
from pathlib import Path
from typing import Any, List, Optional, Type, TypeVar, Union

import attrs
import geopandas as gpd

from fastfuels_sdk.v2.client_library.client import (
    AuthenticatedClient,
)
from fastfuels_sdk.v2.client_library.api.domains import (
    create_domain,
    delete_domain,
    get_domain,
    list_domains as list_domains_endpoint,
    update_domain,
)
from fastfuels_sdk.v2.client_library.models import (
    Domain as DomainModel,
    CreateDomainRequestBody,
    HTTPValidationError,
    ListDomainsResponse,
    UpdateDomainRequestBody,
    DomainSortField,
    DomainSortOrder,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Unset

V2_BASE_URL = "https://api-v2-prod-782971006568.us-west1.run.app"

T = TypeVar("T")

_client: Optional[AuthenticatedClient] = None


def get_client() -> AuthenticatedClient:
    """Get the cached AuthenticatedClient, creating it if necessary."""
    global _client
    client = _client
    if client is None:
        api_key = os.getenv("FASTFUELS_API_KEY")
        if not api_key:
            raise RuntimeError(
                "FastFuels API key not configured. "
                "Set the FASTFUELS_API_KEY environment variable."
            )
        client = AuthenticatedClient(
            base_url=V2_BASE_URL,
            token=api_key,
            prefix="",  # raw key, not "Bearer <key>"
            auth_header_name="api-key",
            raise_on_unexpected_status=True,
        )
        _client = client
    return client


def _checked(response: Any, expected: Type[T]) -> T:
    """Unwrap a generated sync() response, raising on error results.

    The generated client returns documented error models instead of raising:
    a 422 comes back as an HTTPValidationError instance (only *undocumented*
    statuses raise errors.UnexpectedStatus, even with
    raise_on_unexpected_status=True). A real v2 SDK should translate these
    into typed SDK exceptions in a shared exceptions layer; the draft raises
    RuntimeError.
    """
    if isinstance(response, expected):
        return response
    if isinstance(response, HTTPValidationError):
        raise RuntimeError(f"API validation error (422): {response.detail}")
    raise RuntimeError(f"Unexpected API response: {response!r}")


class Domain(DomainModel):
    """Domain resource for the FastFuels v2 API (openapi-python-client draft).

    Inherits all attributes from the generated attrs model: id, name,
    description, type_, features, bbox, crs, tags, pad_to_resolution, style,
    created_on, modified_on.
    """

    @classmethod
    def _from_model(cls, model: DomainModel) -> "Domain":
        # The idiomatic opc conversion: round-trip through the generated
        # to_dict/from_dict (from_dict constructs `cls`, i.e. this subclass).
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: DomainModel) -> "Domain":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(DomainModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    def _require_id(self) -> str:
        """Return the domain id, raising if this instance has none."""
        if isinstance(self.id, Unset):
            raise ValueError(
                "This Domain has no id (it was not created through the API)."
            )
        return self.id

    @classmethod
    def from_id(cls, domain_id: str) -> "Domain":
        """Retrieve an existing Domain by its ID.

        Raises errors.UnexpectedStatus for any non-2xx response (the
        generated client has no per-status exception types).
        """
        response = get_domain.sync(client=get_client(), domain_id=domain_id)
        return cls._from_model(_checked(response, DomainModel))

    @classmethod
    def from_geojson(
        cls,
        geojson: dict,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        pad_to_resolution: Optional[float] = None,
    ) -> "Domain":
        """Create a new Domain from a GeoJSON FeatureCollection.

        Note: unlike v1, the v2 API takes no horizontal/vertical resolution
        on the domain (resolution moved to grids); `pad_to_resolution`
        optionally snaps the bounding box outward for grid alignment.
        Also unlike v1, the v2 API accepts FeatureCollection input only —
        wrap a single Feature in a FeatureCollection.
        """
        request_body = CreateDomainRequestBody.from_dict(
            {
                **geojson,
                "name": name,
                "description": description,
                "tags": tags,
                "pad_to_resolution": pad_to_resolution,
            }
        )
        response = create_domain.sync(client=get_client(), body=request_body)
        return cls._from_model(_checked(response, DomainModel))

    @classmethod
    def from_geodataframe(
        cls,
        geodataframe: gpd.GeoDataFrame,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        pad_to_resolution: Optional[float] = None,
    ) -> "Domain":
        """Create a new Domain from a GeoPandas GeoDataFrame.

        The GeoDataFrame's CRS (when set) is forwarded to the API as the
        FeatureCollection's `crs` member, so projected inputs (e.g.
        EPSG:5070) are interpreted correctly. (The v1 SDK dropped the
        GeoDataFrame CRS and relied on the API's EPSG:4326 default.)
        """
        geojson = json.loads(geodataframe.to_json())
        if geodataframe.crs is not None:
            authority = geodataframe.crs.to_authority()
            if authority is None:
                raise ValueError(
                    "GeoDataFrame CRS has no authority code (e.g. a custom "
                    "CRS). Reproject to a known CRS such as EPSG:4326 with "
                    "geodataframe.to_crs(...) before creating a domain."
                )
            geojson["crs"] = {
                "type": "name",
                "properties": {"name": ":".join(authority)},
            }
        return cls.from_geojson(
            geojson=geojson,
            name=name,
            description=description,
            tags=tags,
            pad_to_resolution=pad_to_resolution,
        )

    @classmethod
    def from_file(
        cls,
        path: Union[str, Path],
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        pad_to_resolution: Optional[float] = None,
    ) -> "Domain":
        """Create a new Domain from a geospatial file.

        Reads any format geopandas supports (GeoJSON, Shapefile, KML,
        GeoPackage, ...) and creates a domain from its geometry.
        """
        return cls.from_geodataframe(
            gpd.read_file(path),
            name=name,
            description=description,
            tags=tags,
            pad_to_resolution=pad_to_resolution,
        )

    def get(self, in_place: bool = False) -> "Domain":
        """Retrieve the latest domain data from the API.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates the current Domain instance with the new data
            and returns self. If False, returns a new Domain instance with
            the latest data, leaving the current instance unchanged.
        """
        domain_id = self._require_id()
        response = _checked(
            get_domain.sync(client=get_client(), domain_id=domain_id),
            DomainModel,
        )
        if in_place:
            return self._copy_fields_from(response)
        return Domain._from_model(response)

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        in_place: bool = False,
    ) -> "Domain":
        """Update the domain's mutable properties (name, description, tags).

        Only provided fields are sent in the PATCH body (the generated
        UNSET sentinel keeps omitted fields out of the request entirely).
        If no fields are provided, no API call is made.
        """
        if name is None and description is None and tags is None:
            return self if in_place else Domain.from_dict(self.to_dict())

        request_body = UpdateDomainRequestBody(
            name=name if name is not None else UNSET,
            description=description if description is not None else UNSET,
            tags=tags if tags is not None else UNSET,
        )
        domain_id = self._require_id()
        response = _checked(
            update_domain.sync(
                client=get_client(), domain_id=domain_id, body=request_body
            ),
            DomainModel,
        )
        if in_place:
            return self._copy_fields_from(response)
        return Domain._from_model(response)

    def delete(self) -> None:
        """Delete this domain and all resources associated with it."""
        domain_id = self._require_id()
        delete_domain.sync_detailed(client=get_client(), domain_id=domain_id)

    def to_json(self) -> str:
        """Serialize the complete Domain object to a JSON string."""
        return json.dumps(self.to_dict(), default=str, indent=2)

    def to_geodataframe(self) -> gpd.GeoDataFrame:
        """Convert the Domain to a GeoPandas GeoDataFrame.

        The v2 API returns two named features: "domain" (the working
        extent / bounding box) and "input" (the original geometry), so the
        GeoDataFrame has one row per feature.
        """
        feature_collection: dict[str, Any] = {
            "type": "FeatureCollection",
            "features": (
                [feature.to_dict() for feature in self.features]
                if self.features
                else []
            ),
        }
        if self.crs and not isinstance(self.crs, Unset):
            feature_collection["crs"] = self.crs.to_dict()

        gdf = gpd.read_file(json.dumps(feature_collection))

        # Add domain metadata as columns (UNSET fields become None)
        gdf["domain_id"] = None if isinstance(self.id, Unset) else self.id
        gdf["domain_name"] = None if isinstance(self.name, Unset) else self.name
        gdf["domain_description"] = (
            None if isinstance(self.description, Unset) else self.description
        )
        if self.pad_to_resolution and not isinstance(self.pad_to_resolution, Unset):
            gdf["pad_to_resolution"] = self.pad_to_resolution
        if self.tags and not isinstance(self.tags, Unset):
            gdf["tags"] = ", ".join(self.tags)

        return gdf


def list_domains(
    page: int = 0,
    size: int = 100,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> List[Domain]:
    """List domains belonging to the authenticated user (single page)."""
    response = _checked(
        list_domains_endpoint.sync(
            client=get_client(),
            page=page,
            size=size,
            sort_by=DomainSortField(sort_by) if sort_by else UNSET,
            sort_order=DomainSortOrder(sort_order) if sort_order else UNSET,
        ),
        ListDomainsResponse,
    )
    return [Domain._from_model(d) for d in response.domains]
