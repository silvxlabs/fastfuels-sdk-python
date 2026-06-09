"""
fastfuels_sdk/v2/features.py
"""

# Core imports
import json
from http import HTTPStatus
from typing import Any, Dict, List, Optional

# Internal imports
from fastfuels_sdk.v2._jobs import wait as _wait
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect
from fastfuels_sdk.v2.client_library.api.features import (
    create_layerset,
    create_osm_road_feature,
    create_osm_water_feature,
    delete_feature,
    get_feature as get_feature_endpoint,
    get_feature_data_metadata,
    get_feature_data_partition,
    list_features as list_features_endpoint,
    list_features_cross_domain,
    update_feature,
)
from fastfuels_sdk.v2.client_library.models import (
    Feature as FeatureModel,
    CreateLayersetRequestBody,
    CreateOsmRoadFeatureRequest,
    CreateOsmWaterFeatureRequest,
    FeatureDataMetadata,
    FeatureSortField,
    FeatureType,
    JobStatus,
    ListFeaturesResponse,
    SortOrder,
    UpdateFeatureRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET

# External imports
import attrs
import geopandas as gpd


def _domain_id(domain) -> str:
    """Resolve a Domain object or a domain-id string to the id string."""
    return getattr(domain, "id", domain)


def _opt(value):
    """Map ``None`` to the generated UNSET sentinel, else pass through."""
    return value if value is not None else UNSET


def _as_feature_collection(geojson: dict) -> dict:
    """Return ``geojson`` as a FeatureCollection dict.

    A single Feature is wrapped in a FeatureCollection (carrying along a
    feature-level ``crs`` member if present) so Feature input keeps
    working.
    """
    geojson_type = geojson.get("type")
    if geojson_type == "Feature":
        feature_collection = {"type": "FeatureCollection", "features": [geojson]}
        if "crs" in geojson:
            feature_collection["crs"] = geojson["crs"]
        return feature_collection
    if geojson_type != "FeatureCollection":
        raise ValueError(
            "GeoJSON type must be 'Feature' or 'FeatureCollection', "
            f"got {geojson_type!r}"
        )
    return geojson


class Feature(FeatureModel):
    """Feature resource for the FastFuels v2 API.

    Represents geographic features within a domain: roads and water
    bodies sourced from OpenStreetMap, or user-uploaded layersets of
    fuelbed polygons. Features are asynchronous job resources — OSM
    features are generated in the background and expose a
    ``status``/``progress`` lifecycle, while layerset uploads complete
    synchronously.

    The Feature resource itself is geometry-free; the generated geodata
    is retrieved through the data methods (:meth:`get_data_metadata`,
    :meth:`get_data_partition`, :meth:`get_data`,
    :meth:`to_geodataframe`) once the feature is completed.

    Attributes
    ----------
    id : str
        Unique identifier for the feature.
    domain_id : str
        Identifier of the domain the feature belongs to.
    type_ : FeatureType
        Type of geographic feature: "road", "water", or "layerset".
    status : JobStatus
        Job status: "pending", "running", "completed", or "failed".
    source : FeatureSource
        Where the feature data comes from (e.g. "osm").
    name : str
        Human-readable name for the feature.
    description : str
        Detailed description of the feature.
    progress : JobProgress, optional
        Progress info while the job is running.
    georeference : FeatureGeoreference, optional
        Spatial reference of the generated data; populated when the job
        completes.
    error : JobError, optional
        Error details if the job failed.
    tags : List[str], optional
        User-defined tags for organization.
    created_on : datetime
        When the feature was created.
    modified_on : datetime
        When the feature was last modified.

    Examples
    --------
    Create a road feature and wait for it to complete:
    >>> import fastfuels_sdk as ff
    >>> feature = ff.features.create_road_feature_from_osm(domain)
    >>> feature.wait()
    >>> roads = feature.to_geodataframe()

    Get a feature by ID:
    >>> feature = ff.get_feature(domain, "def456")

    See Also
    --------
    create_road_feature_from_osm : Create a road feature from OpenStreetMap.
    create_water_feature_from_osm : Create a water feature from OpenStreetMap.
    create_layerset_feature_from_geojson : Upload a custom layerset of fuelbed polygons.
    Feature.to_geodataframe : Retrieve the feature data as a GeoDataFrame.
    Feature.rasterize : Rasterize a layerset feature into a grid.
    list_features : List features in a domain or across all domains.
    """

    @classmethod
    def _from_model(cls, model: FeatureModel) -> "Feature":
        """Build a Feature from a generated FeatureModel instance.

        Round-trips through the generated to_dict/from_dict — from_dict
        constructs ``cls``, i.e. this subclass.
        """
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: FeatureModel) -> "Feature":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(FeatureModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    def _require_completed(self, action: str) -> None:
        """Raise if the feature is not completed, before deriving from it."""
        if self.status != JobStatus.COMPLETED:
            raise ValueError(
                f"Cannot {action} a feature with status '{self.status}'. Call "
                ".wait() until it completes first."
            )

    @classmethod
    def from_id(cls, domain_id: str, feature_id: str) -> "Feature":
        """Retrieve an existing Feature resource by its ID.

        Parameters
        ----------
        domain_id : str
            The unique identifier of the domain the feature belongs to.
        feature_id : str
            The unique identifier of the feature to retrieve.

        Returns
        -------
        Feature
            The requested Feature object.

        Raises
        ------
        NotFoundException
            If no feature exists with the given IDs, or the user does not
            have access to it.

        Examples
        --------
        >>> feature = Feature.from_id("abc123", "def456")
        >>> feature.id
        'def456'
        """
        response = get_feature_endpoint.sync_detailed(
            domain_id, feature_id, client=ensure_client()
        )
        return cls._from_model(expect(response))

    def refresh(self) -> "Feature":
        """Update this Feature in place with the latest data from the API.

        Returns
        -------
        Feature
            ``self``, updated with the latest data (so calls chain).

        Raises
        ------
        NotFoundException
            If the feature no longer exists.

        Examples
        --------
        >>> feature.refresh()
        """
        response = get_feature_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        return self._copy_fields_from(expect(response))

    def wait(self, timeout: Optional[float] = None, verbose: bool = False) -> "Feature":
        """Poll the feature job until it reaches a terminal status.

        Parameters
        ----------
        timeout : float, optional
            Maximum seconds to wait. ``None`` (default) waits indefinitely; the
            job runs server-side regardless, so a bounded wait is resumable.
        verbose : bool, optional
            If True, print the job status at each poll.

        Returns
        -------
        Feature
            ``self``, updated to its terminal state (so calls chain).

        Raises
        ------
        TimeoutError
            If ``timeout`` is set and elapses before a terminal status.
        JobFailedError
            If the job finished with status "failed".

        Examples
        --------
        >>> feature = create_road_feature_from_osm(domain)
        >>> feature.wait(verbose=True)
        Feature def456: JobStatus.COMPLETED (5s)
        """
        return _wait(self, timeout=timeout, verbose=verbose)

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "Feature":
        """Update the feature's mutable metadata (name, description, tags) in place.

        Only provided fields are sent. If no fields are provided, no API call
        is made.

        Parameters
        ----------
        name : str, optional
            New name for the feature.
        description : str, optional
            New description for the feature.
        tags : List[str], optional
            New tags for the feature (replaces existing tags).

        Returns
        -------
        Feature
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the feature no longer exists.

        Examples
        --------
        >>> feature.update(name="new name", tags=["test"])
        """
        if name is None and description is None and tags is None:
            return self

        request_body = UpdateFeatureRequestBody(
            name=_opt(name), description=_opt(description), tags=_opt(tags)
        )
        response = update_feature.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def delete(self) -> None:
        """Delete this feature and its generated data.

        Raises
        ------
        NotFoundException
            If the feature no longer exists.

        Examples
        --------
        >>> feature = Feature.from_id("abc123", "def456")
        >>> feature.delete()
        """
        response = delete_feature.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        expect(response, HTTPStatus.NO_CONTENT)

    def rasterize(
        self,
        output_resolution_m: Optional[float] = None,
        align_to=None,
        align: Optional[str] = None,
        resampling: Optional[str] = None,
        overlap_method: Optional[str] = None,
        extent_buffer_cells: int = 0,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        modifications: Optional[list] = None,
    ):
        """Rasterize this layerset feature into a grid.

        Only valid for layerset features (uploaded fuelbed polygons).

        Parameters
        ----------
        output_resolution_m : float, optional
            Output cell size in meters, anchored to the domain origin.
        align_to : Grid or str, optional
            Match the lattice of an existing grid (or its id).
        align : str, optional
            Pass ``"native"`` to keep the source pixel anchor.
        resampling : str, optional
            Resampling method (e.g. "bilinear", "nearest").
        overlap_method : str, optional
            Per-cell reduction when polygons of the same fuel type overlap:
            "max", "mean", or "min".
        extent_buffer_cells : int, optional
            Result-grid cells to buffer around the domain extent (0-10).
        name, description : str, optional
            Metadata for the new grid.
        tags : List[str], optional
            Tags for the new grid.
        modifications : list, optional
            Modification rules applied after the grid is built.

        Returns
        -------
        Grid
            The new (pending) rasterized Grid.
        """
        # Imported here rather than at module scope so the feature/grid
        # modules stay decoupled (grids never imports features).
        from fastfuels_sdk.v2.grids import Grid, _build_alignment
        from fastfuels_sdk.v2.client_library.api.grids import create_layerset_rasterize
        from fastfuels_sdk.v2.client_library.models import (
            CreateLayersetRasterizeRequest,
            OverlapMethod,
        )

        self._require_completed("rasterize")
        request_body = CreateLayersetRasterizeRequest(
            layerset_id=self.id,
            alignment=_build_alignment(
                output_resolution_m, align_to, align, resampling
            ),
            overlap_method=(
                OverlapMethod(overlap_method) if overlap_method is not None else UNSET
            ),
            extent_buffer_cells=extent_buffer_cells,
            name=name,
            description=description,
            tags=_opt(tags),
            modifications=_opt(modifications),
        )
        response = create_layerset_rasterize.sync_detailed(
            self.domain_id, client=ensure_client(), body=request_body
        )
        return Grid._from_model(expect(response, HTTPStatus.CREATED))

    def get_data_metadata(self) -> FeatureDataMetadata:
        """Get the partition layout of the feature's generated data.

        The generated geodata is served in fixed-size partitions. Use
        this to discover how many partitions exist before retrieving them
        with :meth:`get_data_partition` (or call :meth:`get_data` /
        :meth:`to_geodataframe` to retrieve everything at once).

        Returns
        -------
        FeatureDataMetadata
            With attributes ``total_features`` (count across all
            partitions), ``partition_count`` (number of valid partition
            indices), and ``partitions`` (per-partition feature counts).
            A feature with no data has ``partition_count`` 0.

        Raises
        ------
        NotFoundException
            If the feature no longer exists.
        UnprocessableEntityException
            If the feature is not in "completed" status.

        Examples
        --------
        >>> metadata = feature.get_data_metadata()
        >>> metadata.partition_count
        1
        """
        response = get_feature_data_metadata.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        return expect(response)

    def get_data_partition(self, partition_index: int) -> Dict[str, Any]:
        """Get one partition of the feature's generated data.

        Parameters
        ----------
        partition_index : int
            Zero-indexed partition number. Must be less than the
            ``partition_count`` reported by :meth:`get_data_metadata`.

        Returns
        -------
        dict
            A self-contained GeoJSON FeatureCollection with this
            partition's features.

        Raises
        ------
        NotFoundException
            If the feature no longer exists.
        UnprocessableEntityException
            If ``partition_index`` is past the last partition, or the
            feature is not in "completed" status.
        ApiException
            With ``status_code`` 413 if the serialized partition exceeds
            the 30 MB response cap.

        Examples
        --------
        >>> partition = feature.get_data_partition(0)
        >>> partition["type"]
        'FeatureCollection'
        """
        response = get_feature_data_partition.sync_detailed(
            self.domain_id, self.id, partition_index, client=ensure_client()
        )
        return expect(response)

    def get_data(self) -> Dict[str, Any]:
        """Get the feature's complete generated data as GeoJSON.

        Retrieves every partition and concatenates them into a single
        FeatureCollection, preserving source order.

        Returns
        -------
        dict
            A GeoJSON FeatureCollection with all of the feature's data.
            Empty (no features) if the source data contained nothing
            within the domain extent.

        Raises
        ------
        NotFoundException
            If the feature no longer exists.
        UnprocessableEntityException
            If the feature is not in "completed" status.

        Examples
        --------
        >>> data = feature.get_data()
        >>> len(data["features"])
        42
        """
        metadata = self.get_data_metadata()
        feature_collection: Dict[str, Any] = {
            "type": "FeatureCollection",
            "features": [],
        }
        for partition_index in range(metadata.partition_count):
            partition = self.get_data_partition(partition_index)
            if "crs" in partition and "crs" not in feature_collection:
                feature_collection["crs"] = partition["crs"]
            feature_collection["features"].extend(partition.get("features", []))
        return feature_collection

    def to_geodataframe(self) -> gpd.GeoDataFrame:
        """Retrieve the feature's generated data as a GeoPandas GeoDataFrame.

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame with one row per generated feature. Empty if the
            source data contained nothing within the domain extent.

        Raises
        ------
        NotFoundException
            If the feature no longer exists.
        UnprocessableEntityException
            If the feature is not in "completed" status.

        Examples
        --------
        >>> feature.wait()
        >>> gdf = feature.to_geodataframe()
        """
        data = self.get_data()
        if not data["features"]:
            return gpd.GeoDataFrame()
        return gpd.read_file(json.dumps(data))

    def to_json(self) -> str:
        """Serialize the complete Feature object to a JSON string.

        Returns
        -------
        str
            The Feature as a pretty-printed JSON string.
        """
        return json.dumps(self.to_dict(), default=str, indent=2)


# ---------------------------------------------------------------------------
# Create features (module-level functions)
# ---------------------------------------------------------------------------


def create_road_feature_from_osm(
    domain,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    extent_buffer_m: float = 0.0,
) -> Feature:
    """Create a road feature from OpenStreetMap data.

    Starts a background job that extracts road geometries from
    OpenStreetMap within the domain extent. Use :meth:`Feature.wait` to
    block until the data is ready.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the feature in.
    name : str, optional
        Name for the feature.
    description : str, optional
        Description of the feature.
    tags : List[str], optional
        Tags for organizing the feature.
    extent_buffer_m : float, optional
        Distance in meters (0-100, default 0) to buffer the domain extent
        outward when querying OpenStreetMap.

    Returns
    -------
    Feature
        The created Feature object (job status "pending" or "running").

    Raises
    ------
    NotFoundException
        If the domain does not exist.
    UnprocessableEntityException
        If ``extent_buffer_m`` is outside the 0-100 meter range.

    Examples
    --------
    >>> feature = create_road_feature_from_osm(domain, name="roads")
    >>> feature.type_
    <FeatureType.ROAD: 'road'>
    """
    request_body = CreateOsmRoadFeatureRequest(
        name=name,
        description=description,
        tags=_opt(tags),
        extent_buffer_m=extent_buffer_m,
    )
    response = create_osm_road_feature.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Feature._from_model(expect(response, HTTPStatus.CREATED))


def create_water_feature_from_osm(
    domain,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    extent_buffer_m: float = 0.0,
) -> Feature:
    """Create a water feature from OpenStreetMap data.

    Starts a background job that extracts water-body geometries from
    OpenStreetMap within the domain extent. Use :meth:`Feature.wait` to
    block until the data is ready.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the feature in.
    name : str, optional
        Name for the feature.
    description : str, optional
        Description of the feature.
    tags : List[str], optional
        Tags for organizing the feature.
    extent_buffer_m : float, optional
        Distance in meters (0-100, default 0) to buffer the domain extent
        outward when querying OpenStreetMap.

    Returns
    -------
    Feature
        The created Feature object (job status "pending" or "running").

    Raises
    ------
    NotFoundException
        If the domain does not exist.
    UnprocessableEntityException
        If ``extent_buffer_m`` is outside the 0-100 meter range.

    Examples
    --------
    >>> feature = create_water_feature_from_osm(domain, name="water")
    >>> feature.type_
    <FeatureType.WATER: 'water'>
    """
    request_body = CreateOsmWaterFeatureRequest(
        name=name,
        description=description,
        tags=_opt(tags),
        extent_buffer_m=extent_buffer_m,
    )
    response = create_osm_water_feature.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Feature._from_model(expect(response, HTTPStatus.CREATED))


def create_layerset_feature_from_geojson(
    domain,
    geojson: dict,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Feature:
    """Upload a custom layerset of fuelbed polygons from GeoJSON.

    Uploads a GeoJSON FeatureCollection where each feature is one fuelbed
    polygon. The upload is validated and stored synchronously: the returned
    Feature has status "completed" and its data is immediately available
    through the data methods.

    Each feature's ``properties`` must carry the fuelbed input columns:

    - ``fuel_type`` (str)
    - ``fuel_loading`` (float)
    - ``fuel_height`` (float)
    - ``percent_cover`` (float)
    - ``distribution`` (str): "homogeneous", "random_clusters", or
      "uniform_random"

    Optional columns: ``strata_fb``, ``patch_size``,
    ``live_fuel_moisture``, ``dead_fuel_moisture``, ``heat_of_combustion``,
    ``patch_std_dev``.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the feature in.
    geojson : dict
        A GeoJSON FeatureCollection or Feature (a single Feature is wrapped
        automatically) with Polygon or MultiPolygon geometries. The ``crs``
        member must declare a **projected** CRS (e.g. EPSG:5070); geographic
        coordinates are rejected.
    name : str, optional
        Name for the feature.
    description : str, optional
        Description of the feature.
    tags : List[str], optional
        Tags for organizing the feature.

    Returns
    -------
    Feature
        The created Feature object with status "completed".

    Raises
    ------
    ValueError
        If the GeoJSON is not a Feature or FeatureCollection.
    NotFoundException
        If the domain does not exist.
    UnprocessableEntityException
        If the CRS is missing or geographic, a geometry is not a
        Polygon/MultiPolygon, or a feature is missing required fuelbed
        properties.

    Examples
    --------
    >>> feature = create_layerset_feature_from_geojson(domain, geojson)
    >>> feature.status
    <JobStatus.COMPLETED: 'completed'>
    """
    feature_collection = _as_feature_collection(geojson)
    body = {**feature_collection, "name": name, "description": description}
    if tags is not None:
        body["tags"] = tags
    request_body = CreateLayersetRequestBody.from_dict(body)
    response = create_layerset.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Feature._from_model(expect(response, HTTPStatus.CREATED))


def create_layerset_feature_from_geodataframe(
    domain,
    geodataframe: gpd.GeoDataFrame,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Feature:
    """Upload a custom layerset from a GeoPandas GeoDataFrame.

    The GeoDataFrame's CRS is forwarded to the API as the FeatureCollection's
    ``crs`` member. The CRS must be **projected** (e.g. EPSG:5070); the
    GeoDataFrame is not reprojected — use ``geodataframe.to_crs(...)`` first if
    needed. Each row's columns must carry the fuelbed properties described in
    :func:`create_layerset_feature_from_geojson`.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the feature in.
    geodataframe : gpd.GeoDataFrame
        GeoDataFrame with one fuelbed polygon per row.
    name : str, optional
        Name for the feature.
    description : str, optional
        Description of the feature.
    tags : List[str], optional
        Tags for organizing the feature.

    Returns
    -------
    Feature
        The created Feature object with status "completed".

    Raises
    ------
    ValueError
        If the GeoDataFrame CRS has no authority code (e.g. a custom CRS).
    UnprocessableEntityException
        Same validation errors as :func:`create_layerset_feature_from_geojson`.

    Examples
    --------
    >>> gdf = gpd.read_file("fuelbeds.shp").to_crs(epsg=5070)
    >>> feature = create_layerset_feature_from_geodataframe(domain, gdf)
    """
    geojson = json.loads(geodataframe.to_json())
    if geodataframe.crs is not None:
        authority = geodataframe.crs.to_authority()
        if authority is None:
            raise ValueError(
                "GeoDataFrame CRS has no authority code (e.g. a custom "
                "CRS). Reproject to a known projected CRS with "
                "geodataframe.to_crs(...) before creating a layerset."
            )
        geojson["crs"] = {
            "type": "name",
            "properties": {"name": ":".join(authority)},
        }
    return create_layerset_feature_from_geojson(
        domain,
        geojson,
        name=name,
        description=description,
        tags=tags,
    )


def get_feature(domain, feature_id: str) -> Feature:
    """Retrieve a single feature by its ID.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) the feature belongs to.
    feature_id : str
        The unique identifier of the feature.

    Returns
    -------
    Feature
        The requested Feature object.

    Raises
    ------
    NotFoundException
        If no feature exists with the given IDs, or the user does not have
        access to it.
    """
    return Feature.from_id(_domain_id(domain), feature_id)


def list_features(
    domain=None,
    page: int = 0,
    size: int = 100,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    feature_type: Optional[str] = None,
    product: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[Feature]:
    """List features in a domain, or across all domains (single page).

    Parameters
    ----------
    domain : Domain or str, optional
        The domain (or its id) to list features in. If omitted, features from
        all the user's domains are listed.
    page : int, optional
        The page number to retrieve, zero-indexed (default 0).
    size : int, optional
        The number of features per page (default 100).
    sort_by : str, optional
        Field to sort by: "name", "created_on", or "modified_on".
    sort_order : str, optional
        Sort direction: "ascending" or "descending".
    feature_type : str, optional
        Only return features of this type: "road", "water", or "layerset".
    product : str, optional
        Only return features from this data product (e.g. "osm").
    tag : str, optional
        Only return features carrying this tag.

    Returns
    -------
    List[Feature]
        The requested page of Feature objects.

    Examples
    --------
    >>> features = list_features(domain, feature_type="road")
    >>> all_features = list_features()  # across all domains
    """
    kwargs = dict(
        client=ensure_client(),
        page=page,
        size=size,
        sort_by=FeatureSortField(sort_by) if sort_by else UNSET,
        sort_order=SortOrder(sort_order) if sort_order else UNSET,
        type_=FeatureType(feature_type) if feature_type else UNSET,
        product=_opt(product),
        tag=_opt(tag),
    )
    if domain is None:
        response = list_features_cross_domain.sync_detailed(**kwargs)
    else:
        response = list_features_endpoint.sync_detailed(_domain_id(domain), **kwargs)
    list_response: ListFeaturesResponse = expect(response)
    return [Feature._from_model(f) for f in list_response.features]
