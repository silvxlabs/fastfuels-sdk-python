"""
fastfuels_sdk/v2/domains.py
"""

# Core imports
import json
from http import HTTPStatus
from pathlib import Path
from typing import Any, List, Optional, Union

# Internal imports
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect
from fastfuels_sdk.v2.client_library.api.domains import (
    create_domain,
    delete_domain,
    get_domain,
    get_domain_lattice,
    list_domains as list_domains_endpoint,
    preview_domain,
    reproject_domain,
    update_domain,
)
from fastfuels_sdk.v2.client_library.models import (
    Domain as DomainModel,
    DomainLattice,
    DomainSortField,
    DomainSortOrder,
    GeoJsonFeatureCollection,
    ListDomainsResponse,
    UpdateDomainRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Unset

# External imports
import attrs
import geopandas as gpd


def _build_create_request_body(
    geojson: dict,
    name: str,
    description: str,
    tags: Optional[List[str]],
    pad_to_resolution: Optional[float],
) -> GeoJsonFeatureCollection:
    """Build a domain creation request body from GeoJSON input.

    The v2 API accepts FeatureCollection input only; a single Feature is
    wrapped in a FeatureCollection here (carrying along a feature-level
    ``crs`` member if present) so v1-style Feature input keeps working.
    """
    geojson_type = geojson.get("type")
    if geojson_type == "Feature":
        feature_collection = {"type": "FeatureCollection", "features": [geojson]}
        if "crs" in geojson:
            feature_collection["crs"] = geojson["crs"]
        geojson = feature_collection
    elif geojson_type != "FeatureCollection":
        raise ValueError(
            "GeoJSON type must be 'Feature' or 'FeatureCollection', "
            f"got {geojson_type!r}"
        )

    return GeoJsonFeatureCollection.from_dict(
        {
            **geojson,
            "name": name,
            "description": description,
            "tags": tags,
            "pad_to_resolution": pad_to_resolution,
        }
    )


class Domain(DomainModel):
    """Domain resource for the FastFuels v2 API.

    Represents a spatial container that defines geographic boundaries for
    fire behavior modeling and analysis. A Domain includes metadata like
    name and description along with geometric data defining its spatial
    extent. Domains must specify a valid area between 0 and 16 square
    kilometers, located within CONUS.

    The Domain handles coordinate system transformations automatically:

    1. Geographic coordinates (e.g. EPSG:4326) are projected to the
       appropriate UTM zone
    2. Projected coordinates are preserved in their original CRS
    3. Geometries are optionally padded to align with a grid resolution
       (``pad_to_resolution``)

    Attributes
    ----------
    id : str
        Unique identifier for the domain.
    name : str
        Human-readable name for the domain.
    description : str
        Detailed description of the domain.
    type_ : str
        Always "FeatureCollection".
    features : List[GeoJsonFeature]
        Two named GeoJSON features: "domain" (the working extent /
        bounding box) and "input" (the original geometry).
    bbox : List[float]
        Bounding box of the "domain" feature.
    crs : GeoJsonCRS
        Coordinate reference system specification (always projected).
    tags : List[str], optional
        User-defined tags for organization.
    pad_to_resolution : float, optional
        Resolution in meters the domain bounding box was padded to align
        with.
    created_on : datetime
        When the domain was created.
    modified_on : datetime
        When the domain was last modified.

    Examples
    --------
    Create a domain from a file:
    >>> domain = Domain.from_file("area.geojson", name="my domain")

    Get a domain by ID:
    >>> domain = Domain.from_id("abc123")
    >>> print(domain.name)
    'my domain'

    See Also
    --------
    Domain.from_geojson : Create a domain from GeoJSON data.
    Domain.from_geodataframe : Create a domain from a GeoPandas GeoDataFrame.
    Domain.from_file : Create a domain from a geospatial file.
    Domain.preview : Validate and project a domain without persisting it.
    Domain.get_lattice : Get the pixel lattice for a domain at a resolution.
    Domain.to_geodataframe : Convert a domain to a GeoPandas GeoDataFrame.
    list_domains : List available domains.
    reproject_geojson : Reproject a GeoJSON FeatureCollection (stateless).
    """

    @classmethod
    def _from_model(cls, model: DomainModel) -> "Domain":
        """Build a Domain from a generated DomainModel instance.

        Round-trips through the generated to_dict/from_dict — from_dict
        constructs ``cls``, i.e. this subclass.
        """
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
        """Retrieve an existing Domain resource by its ID.

        Parameters
        ----------
        domain_id : str
            The unique identifier of the domain to retrieve.

        Returns
        -------
        Domain
            The requested Domain object.

        Raises
        ------
        NotFoundException
            If no domain exists with the given ID, or the user does not
            have access to it.

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> domain.id
        'abc123'
        """
        response = get_domain.sync_detailed(client=ensure_client(), domain_id=domain_id)
        return cls._from_model(expect(response))

    @classmethod
    def from_geojson(
        cls,
        geojson: dict,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        pad_to_resolution: Optional[float] = None,
    ) -> "Domain":
        """Create a new Domain from GeoJSON data.

        Parameters
        ----------
        geojson : dict
            A GeoJSON FeatureCollection or Feature. (The v2 API accepts
            FeatureCollection input only; a single Feature is wrapped
            automatically.) The source CRS is read from the ``crs`` member
            if present; otherwise EPSG:4326 is assumed.
        name : str, optional
            Name for the domain.
        description : str, optional
            Description of the domain.
        tags : List[str], optional
            Tags for organizing the domain.
        pad_to_resolution : float, optional
            Pad the domain bounding box outward so its extent is a
            multiple of this resolution (meters).

        Returns
        -------
        Domain
            The created Domain object.

        Raises
        ------
        ValueError
            If the GeoJSON is not a Feature or FeatureCollection.
        UnprocessableEntityException
            If the geometry is invalid: zero area, larger than 16 square
            kilometers, outside CONUS, or an invalid CRS.

        Examples
        --------
        >>> with open("area.geojson") as f:
        ...     geojson = json.load(f)
        >>> domain = Domain.from_geojson(geojson, name="my domain")
        """
        request_body = _build_create_request_body(
            geojson, name, description, tags, pad_to_resolution
        )
        response = create_domain.sync_detailed(
            client=ensure_client(), body=request_body
        )
        return cls._from_model(expect(response, HTTPStatus.CREATED))

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
        FeatureCollection's ``crs`` member, so projected inputs (e.g.
        EPSG:5070) are interpreted correctly.

        Parameters
        ----------
        geodataframe : gpd.GeoDataFrame
            GeoDataFrame containing the domain geometry.
        name : str, optional
            Name for the domain.
        description : str, optional
            Description of the domain.
        tags : List[str], optional
            Tags for organizing the domain.
        pad_to_resolution : float, optional
            Pad the domain bounding box outward so its extent is a
            multiple of this resolution (meters).

        Returns
        -------
        Domain
            The created Domain object.

        Raises
        ------
        ValueError
            If the GeoDataFrame CRS has no authority code (e.g. a custom
            CRS).
        UnprocessableEntityException
            If the geometry is invalid: zero area, larger than 16 square
            kilometers, outside CONUS, or an invalid CRS.

        Examples
        --------
        >>> gdf = gpd.read_file("area.shp")
        >>> domain = Domain.from_geodataframe(gdf, name="my domain")
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

        Parameters
        ----------
        path : str or Path
            Path to the geospatial file.
        name : str, optional
            Name for the domain.
        description : str, optional
            Description of the domain.
        tags : List[str], optional
            Tags for organizing the domain.
        pad_to_resolution : float, optional
            Pad the domain bounding box outward so its extent is a
            multiple of this resolution (meters).

        Returns
        -------
        Domain
            The created Domain object.

        Examples
        --------
        >>> domain = Domain.from_file("area.geojson", name="my domain")
        """
        return cls.from_geodataframe(
            gpd.read_file(path),
            name=name,
            description=description,
            tags=tags,
            pad_to_resolution=pad_to_resolution,
        )

    @classmethod
    def preview(
        cls,
        geojson: dict,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        pad_to_resolution: Optional[float] = None,
    ) -> "Domain":
        """Preview a domain without persisting it.

        Runs the same validation and projection pipeline as domain
        creation but writes nothing: use this to inspect the projected,
        padded bounding box before committing to a create. Takes the same
        arguments as :meth:`from_geojson`.

        Parameters
        ----------
        geojson : dict
            A GeoJSON FeatureCollection or Feature (a single Feature is
            wrapped automatically).
        name : str, optional
            Name for the domain.
        description : str, optional
            Description of the domain.
        tags : List[str], optional
            Tags for organizing the domain.
        pad_to_resolution : float, optional
            Pad the domain bounding box outward so its extent is a
            multiple of this resolution (meters).

        Returns
        -------
        Domain
            The previewed Domain object. Its ``id`` is always
            ``"preview"`` — not a real domain identifier, so API-backed
            instance methods (``refresh``, ``update``, ``delete``,
            ``get_lattice``) will not work on it.

        Raises
        ------
        UnprocessableEntityException
            Same validation errors as :meth:`from_geojson`.

        Examples
        --------
        >>> previewed = Domain.preview(geojson, pad_to_resolution=2.0)
        >>> previewed.id
        'preview'
        """
        request_body = _build_create_request_body(
            geojson, name, description, tags, pad_to_resolution
        )
        response = preview_domain.sync_detailed(
            client=ensure_client(), body=request_body
        )
        return cls._from_model(expect(response))

    def refresh(self) -> "Domain":
        """Update this Domain in place with the latest data from the API.

        Returns
        -------
        Domain
            ``self``, updated with the latest data (so calls chain). To fetch
            a fresh, separate copy instead, use :meth:`Domain.from_id`.

        Raises
        ------
        NotFoundException
            If the domain no longer exists.

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> domain.refresh()  # refresh in place
        """
        domain_id = self._require_id()
        response = get_domain.sync_detailed(client=ensure_client(), domain_id=domain_id)
        return self._copy_fields_from(expect(response))

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "Domain":
        """Update the domain's mutable properties (name, description, tags) in place.

        Only provided fields are sent in the PATCH body (the generated
        UNSET sentinel keeps omitted fields out of the request entirely).
        If no fields are provided, no API call is made.

        Parameters
        ----------
        name : str, optional
            New name for the domain.
        description : str, optional
            New description for the domain.
        tags : List[str], optional
            New tags for the domain (replaces existing tags).

        Returns
        -------
        Domain
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the domain no longer exists.

        Examples
        --------
        >>> domain.update(name="new name", tags=["test"])
        """
        if name is None and description is None and tags is None:
            return self

        request_body = UpdateDomainRequestBody(
            name=name if name is not None else UNSET,
            description=description if description is not None else UNSET,
            tags=tags if tags is not None else UNSET,
        )
        domain_id = self._require_id()
        response = update_domain.sync_detailed(
            client=ensure_client(), domain_id=domain_id, body=request_body
        )
        return self._copy_fields_from(expect(response))

    def delete(self, force: bool = False) -> None:
        """Delete this domain.

        Parameters
        ----------
        force : bool, optional
            If True, cascade-delete every child resource (features, grids,
            inventories, exports) in the domain. If False (default), the API
            rejects the request with 412 when the domain still has child
            resources.

        Raises
        ------
        NotFoundException
            If the domain no longer exists.
        ApiException
            With ``status_code`` 412 if the domain has child resources and
            ``force`` is False.

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> domain.delete(force=True)  # also deletes its grids and features
        """
        domain_id = self._require_id()
        response = delete_domain.sync_detailed(
            client=ensure_client(), domain_id=domain_id, force=force
        )
        expect(response, HTTPStatus.NO_CONTENT)

    def get_lattice(
        self, resolution: float, num_buffer_cells: int = 0
    ) -> DomainLattice:
        """Get the pixel lattice for this domain at a given resolution.

        Returns the pixel lattice (affine transform + raster shape) for
        the domain at the requested resolution. Use this to align a
        GeoTIFF before uploading it as a custom grid.

        Parameters
        ----------
        resolution : float
            Pixel size in meters (domain CRS units, always projected).
        num_buffer_cells : int, optional
            Expand the lattice by N cells on each side (default 0).
            Mirrors the buffer semantics of the grid creation endpoints.

        Returns
        -------
        DomainLattice
            With attributes ``crs`` (authority string), ``resolution``,
            ``num_buffer_cells``, ``transform`` (affine coefficients
            ``[a, b, c, d, e, f]``, rasterio convention), and ``shape``
            (``[height, width]`` in pixels).

        Raises
        ------
        NotFoundException
            If the domain no longer exists.
        UnprocessableEntityException
            If ``resolution`` is non-positive or ``num_buffer_cells`` is
            negative.

        Examples
        --------
        >>> lattice = domain.get_lattice(resolution=2.0)
        >>> lattice.shape
        [400, 400]
        """
        domain_id = self._require_id()
        response = get_domain_lattice.sync_detailed(
            domain_id=domain_id,
            client=ensure_client(),
            resolution=resolution,
            num_buffer_cells=num_buffer_cells,
        )
        return expect(response)

    def to_json(self) -> str:
        """Serialize the complete Domain object to a JSON string.

        Returns
        -------
        str
            The Domain as a pretty-printed JSON string.
        """
        return json.dumps(self.to_dict(), default=str, indent=2)

    def to_geodataframe(self) -> gpd.GeoDataFrame:
        """Convert the Domain to a GeoPandas GeoDataFrame.

        The v2 API returns two named features: "domain" (the working
        extent / bounding box) and "input" (the original geometry), so the
        GeoDataFrame has one row per feature.

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame in the domain CRS with the domain features as
            rows and domain metadata as columns.

        Examples
        --------
        >>> gdf = domain.to_geodataframe()
        >>> gdf[gdf["name"] == "input"].geometry  # the original geometry
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
    """List domains belonging to the authenticated user (single page).

    Parameters
    ----------
    page : int, optional
        The page number to retrieve, zero-indexed (default 0).
    size : int, optional
        The number of domains per page (default 100).
    sort_by : str, optional
        Field to sort by: "name", "created_on", or "modified_on".
    sort_order : str, optional
        Sort direction: "ascending" or "descending".

    Returns
    -------
    List[Domain]
        The requested page of Domain objects.

    Examples
    --------
    >>> domains = list_domains(sort_by="created_on", sort_order="descending")
    """
    response = list_domains_endpoint.sync_detailed(
        client=ensure_client(),
        page=page,
        size=size,
        sort_by=DomainSortField(sort_by) if sort_by else UNSET,
        sort_order=DomainSortOrder(sort_order) if sort_order else UNSET,
    )
    list_response: ListDomainsResponse = expect(response)
    return [Domain._from_model(d) for d in list_response.domains]


def reproject_geojson(geojson: dict, target_epsg: int) -> dict:
    """Reproject a GeoJSON FeatureCollection to a target CRS.

    Stateless utility — no resource is created; the reprojected
    FeatureCollection is returned immediately.

    Parameters
    ----------
    geojson : dict
        A GeoJSON FeatureCollection or Feature (a single Feature is
        wrapped automatically). The source CRS is read from the ``crs``
        member if present; otherwise EPSG:4326 is assumed.
    target_epsg : int
        EPSG code of the target CRS (e.g. 4326 for WGS84, 32611 for UTM
        zone 11N).

    Returns
    -------
    dict
        The reprojected FeatureCollection, with original feature
        properties preserved and ``crs`` set to the target EPSG code.

    Raises
    ------
    UnprocessableEntityException
        If the source CRS is invalid, the target EPSG is invalid, or a
        geometry cannot be reprojected.

    Examples
    --------
    >>> projected = reproject_geojson(geojson, target_epsg=5070)
    >>> projected["crs"]["properties"]["name"]
    'EPSG:5070'
    """
    request_body = _build_create_request_body(
        geojson, name="", description="", tags=None, pad_to_resolution=None
    )
    response = reproject_domain.sync_detailed(
        client=ensure_client(), body=request_body, target_epsg=target_epsg
    )
    return expect(response).to_dict()
