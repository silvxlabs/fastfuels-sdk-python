"""
fastfuels_sdk/v2/grids.py
"""

# Core imports
import datetime
import json
import re
from collections.abc import Mapping
from http import HTTPStatus
from typing import TYPE_CHECKING, Dict, List, Optional, Union

# Internal imports
from fastfuels_sdk.v2._jobs import wait as _wait
from fastfuels_sdk.v2._uploads import put_upload
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect, raise_for_response
from fastfuels_sdk.v2.client_library.api.grids import (
    apply_grid_modifications as apply_grid_modifications_endpoint,
    check_3dep_coverage as check_3dep_coverage_endpoint,
    check_landfire_fbfm13_coverage as check_landfire_fbfm13_coverage_endpoint,
    check_landfire_fbfm40_coverage as check_landfire_fbfm40_coverage_endpoint,
    check_landfire_fccs_coverage as check_landfire_fccs_coverage_endpoint,
    create_3dep_topography,
    create_compose_grid,
    create_duet_grid,
    create_fccs_lookup,
    create_fosberg_fuel_moisture_grid,
    create_fbfm13_lookup,
    create_fbfm40_lookup,
    create_geotiff_upload,
    create_grid_export,
    create_inventory_canopy_grid,
    create_landfire_canopy,
    create_landfire_fbfm13,
    create_landfire_fbfm40,
    create_landfire_fccs,
    create_landfire_topography,
    create_leaflux_irradiance_grid,
    create_meta_chm,
    create_naip_chm,
    create_netcdf_upload,
    create_point_cloud_chm,
    create_resample,
    create_treemap,
    create_uniform_grid as create_uniform_grid_endpoint,
    delete_grid,
    duplicate_grid as duplicate_grid_endpoint,
    get_grid as get_grid_endpoint,
    get_grid_data_binary,
    list_grids as list_grids_endpoint,
    list_grids_cross_domain,
    update_grid,
)
from fastfuels_sdk.v2.client_library.models import (
    Grid as GridModel,
    AllometryCanopyBiomassSource,
    ApplyGridModificationsRequest,
    BoundaryScatter,
    CanopyAllometryMaxCrownRadiusSource,
    CanopyAvailableFuel,
    CanopyBiomassEquations,
    CanopyBranchwood,
    CanopyBranchwoodSizePartition,
    CanopyCbdLoadOverDepth,
    CanopyCbdRunningMean,
    CanopyCbhMean,
    CanopyCbhMinimum,
    CanopyCbhPercentile,
    CanopyCcCoverFraction,
    CanopyCcCrownOverlap,
    CanopyCcCrownUnion,
    CanopyChmHeightPercentile,
    CanopyCrownWidthEquations,
    CanopyFuelcalcCrownClassAdjustment,
    CanopyHorizontalDistribution,
    CanopyNoCrownClassAdjustment,
    CanopyProfileThreshold,
    CanopySpeciesInclusion,
    CanopyVerticalDistribution,
    ComposeAttributeCondition,
    ComposeCompute,
    ComposeInput,
    ComposeLiteral,
    ComposeSelect,
    CreateDuetRequest,
    ChmMaxAggregation,
    ChmMeanAggregation,
    ChmMedianAggregation,
    ChmPercentileAggregation,
    ChmSpikeFilter,
    CreateComposeRequest,
    CreateFccsLookupRequest,
    CreateFbfm13LookupRequest,
    CreateFbfm40LookupRequest,
    CreateFosbergFuelMoistureRequest,
    CreateGeoTIFFUploadRequest,
    CreateInventoryCanopyRequest,
    CreateLandfireCanopyRequest,
    CreateLandfireFbfm13Request,
    CreateLandfireFbfm40Request,
    CreateLandfireFccsRequest,
    CreateLandfireTopographyRequest,
    CreateLeafluxIrradianceRequest,
    CreateMetaChmRequest,
    CreateNaipChmRequest,
    CreateNetcdfUploadRequest,
    CreatePointCloudChmRequest,
    CreateResampleRequest,
    CreateThreeDepTopographyRequest,
    CreateTreeMapRequest,
    CreateUniformRequest,
    DuplicateGridRequest,
    DuetBand,
    DuetCalibration,
    ExportGridRequest,
    FccsLookupBand,
    Fbfm13LookupBand,
    Fbfm40LookupBand,
    FuelMoistureMonth,
    GridAlignmentDomainTarget,
    GridAlignmentGridTarget,
    GridAlignmentNativeTarget,
    GridDataArrayFormat,
    GridDataOrder,
    GridExportFormat,
    GridSortField,
    InlineCompute,
    InventoryCanopyBand,
    InventoryColumnCanopyBiomassSource,
    InventoryColumnMaxCrownRadiusSource,
    JobStatus,
    LandfireCanopyFuelBand,
    LandfireCanopyVersion,
    LandfireCoverageResponse,
    LandfireFbfm13Version,
    LandfireFbfm40Version,
    LandfireFccsVersion,
    LandfireSeason,
    LandfireTopographyVersion,
    LeafluxBand,
    ListGridsResponse,
    MetaCHMVersion,
    NonBurnableFuelModel,
    RelativeElevation,
    ResamplingMethod,
    SortOrder,
    ThreeDepResolution,
    TopographyBand,
    TopographyThreeDepCoverageResponse,
    TreeMapBand,
    TreeMapVersion,
    UniformBand,
    UniformBandInput,
    UpdateGridRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Response

# External imports
import attrs
import numpy as np

if TYPE_CHECKING:
    from fastfuels_sdk.v2.point_clouds import PointCloud

__all__ = [
    "Grid",
    "create_topography_grid_from_3dep",
    "create_topography_grid_from_landfire",
    "create_canopy_fuel_grid_from_landfire",
    "create_canopy_fuel_grid_from_inventory",
    "create_canopy_height_grid_from_meta",
    "create_canopy_height_grid_from_naip_chm",
    "create_canopy_height_grid_from_point_cloud",
    "create_fuel_model_grid_from_landfire_fbfm13",
    "create_fuel_model_grid_from_landfire_fbfm40",
    "create_fuel_model_grid_from_landfire_fccs",
    "create_pim_grid_from_treemap",
    "create_grid_from_geotiff",
    "create_grid_from_netcdf",
    "create_grid_from_compose",
    "create_uniform_grid",
    "create_surface_fuel_grid_from_duet",
    "create_dead_fuel_moisture_grid_from_fosberg",
    "create_fuel_grid_from_fccs_lookup",
    "create_fuel_grid_from_fbfm13_lookup",
    "create_fuel_grid_from_fbfm40_lookup",
    "create_irradiance_grid_from_leaflux",
    "list_grids",
    "get_grid",
    "check_3dep_coverage",
    "check_landfire_fbfm40_coverage",
    "check_landfire_fbfm13_coverage",
    "check_landfire_fccs_coverage",
]


def _domain_id(domain) -> str:
    """Resolve a Domain object or a domain-id string to the id string."""
    return getattr(domain, "id", domain)


def _grid_id(grid) -> str:
    """Resolve a Grid object or a grid-id string to the id string."""
    return getattr(grid, "id", grid)


def _enum_list(values, enum_cls):
    """Coerce a list of strings/enum members to enum members, or UNSET."""
    if values is None:
        return UNSET
    return [v if isinstance(v, enum_cls) else enum_cls(v) for v in values]


def _opt(value):
    """Map ``None`` to the generated UNSET sentinel, else pass through."""
    return value if value is not None else UNSET


def _build_alignment(
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
):
    """Translate friendly alignment keywords into a grid alignment target.

    Returns a ``GridAlignment{Domain,Grid,Native}Target`` or ``UNSET`` (let the
    API choose its default, which anchors to the domain origin at the source's
    native cell size).

    - ``output_resolution_m=N`` anchors output cells to the domain origin at N
      meters (the default target).
    - ``align_to=<grid or id>`` matches an existing grid's lattice exactly.
    - ``align="native"`` keeps the source raster's pixel anchor.
    - ``resampling=<method>`` selects the resampling method for any of the above.

    ``output_resolution_m``, ``align_to``, and ``align`` are mutually exclusive.
    """
    if align is not None and align != "native":
        raise ValueError(
            f'align must be "native" if given, got {align!r}. Use '
            "output_resolution_m to set a resolution or align_to to match a grid."
        )
    if sum(x is not None for x in (output_resolution_m, align_to, align)) > 1:
        raise ValueError(
            "Specify at most one of output_resolution_m, align_to, or align."
        )

    method = ResamplingMethod(resampling) if resampling is not None else UNSET

    if align_to is not None:
        return GridAlignmentGridTarget(
            target="grid", grid_id=_domain_id(align_to), method=method
        )
    if align is not None:  # align == "native"
        return GridAlignmentNativeTarget(target="native", method=method)
    if output_resolution_m is not None or resampling is not None:
        return GridAlignmentDomainTarget(
            resolution=_opt(output_resolution_m), method=method
        )
    return UNSET


def _build_chm_aggregation(aggregation, percentile):
    """Translate an aggregation keyword into a CHM aggregation target.

    Returns a ``Chm{Max,Mean,Median,Percentile}Aggregation`` or ``UNSET`` (let
    the API choose its default).

    - ``aggregation="max"`` / ``"mean"`` / ``"median"`` selects that statistic.
    - ``aggregation="percentile"`` requires ``percentile`` (0-100).
    - ``percentile`` is only valid with ``aggregation="percentile"``.
    """
    if aggregation is None and percentile is None:
        return UNSET
    if aggregation == "percentile":
        if percentile is None:
            raise ValueError('aggregation="percentile" requires a percentile value.')
        return ChmPercentileAggregation(percentile=percentile)
    if percentile is not None:
        raise ValueError('percentile is only used with aggregation="percentile".')
    methods = {
        "max": ChmMaxAggregation,
        "mean": ChmMeanAggregation,
        "median": ChmMedianAggregation,
    }
    if aggregation not in methods:
        raise ValueError(
            'aggregation must be one of "max", "mean", "median", or '
            f'"percentile", got {aggregation!r}.'
        )
    return methods[aggregation]()


def _build_chm_spike_filter(spike_filter):
    """Translate a spike-filter keyword into a CHM spike-filter target.

    - ``None`` -> ``UNSET`` (the API applies its default filter).
    - ``False`` -> ``None`` (disable filtering, keeping every return).
    - ``True`` -> a default ``ChmSpikeFilter``.
    - a mapping -> a ``ChmSpikeFilter`` built from its fields.
    - a ``ChmSpikeFilter`` -> passed through unchanged.
    """
    if spike_filter is None:
        return UNSET
    if spike_filter is False:
        return None
    if spike_filter is True:
        return ChmSpikeFilter()
    if isinstance(spike_filter, ChmSpikeFilter):
        return spike_filter
    if isinstance(spike_filter, Mapping):
        return ChmSpikeFilter(**spike_filter)
    raise ValueError(
        "spike_filter must be a bool, a mapping of filter fields, or a "
        f"ChmSpikeFilter, got {spike_filter!r}."
    )


def _build_boundary_scatter(scatter):
    """Translate a boundary_scatter kwarg into a BoundaryScatter or UNSET.

    - ``None`` -> ``UNSET`` (the API omits scatter — existing behavior).
    - ``True`` / ``{}`` -> a default ``BoundaryScatter`` (depth=10, seed=42).
    - a mapping -> a ``BoundaryScatter`` built from its fields.
    - a ``BoundaryScatter`` -> passed through unchanged.
    """
    if scatter is None:
        return UNSET
    if scatter is True:
        return BoundaryScatter()
    if isinstance(scatter, BoundaryScatter):
        return scatter
    if isinstance(scatter, Mapping):
        return BoundaryScatter(**scatter)
    raise ValueError(
        "boundary_scatter must be True, a mapping of scatter fields, or a "
        f"BoundaryScatter, got {scatter!r}."
    )


def _fill_for(dtype, nodata=None):
    """Pick the fill value for cells a chunk does not cover.

    Uses the band's ``nodata`` when defined, else NaN for floating dtypes and
    0 for integers (NaN is not representable in an integer array).
    """
    if nodata is not None and nodata is not UNSET:
        return nodata
    return np.nan if np.issubdtype(dtype, np.floating) else 0


def _decode_grid_chunk(content: bytes, headers):
    """Decode one binary grid chunk into ``(offset, block)``.

    The chunk endpoint returns ``application/octet-stream`` and describes the
    payload entirely in headers (see ``get_grid_data_binary``): ``X-Data-Shape``,
    ``X-Data-Offset``, ``X-Data-Order``, ``X-Data-Format`` and the dtype headers.
    ``offset`` is where the block lands in the full grid; ``block`` is an
    ``np.ndarray`` of the chunk's own shape.
    """
    shape = [int(s) for s in headers["X-Data-Shape"].split(",")]
    offset = tuple(int(o) for o in headers["X-Data-Offset"].split(","))
    order = headers.get("X-Data-Order", "C")

    if headers["X-Data-Format"] == "dense":
        dtype = np.dtype(headers["X-Data-Dtype"])
        block = np.frombuffer(content, dtype=dtype).reshape(shape, order=order)
        return offset, block

    # Sparse: the body is the index array bytes immediately followed by the
    # value array bytes; split at NNZ * sizeof(index_dtype).
    nnz = int(headers["X-Data-NNZ"])
    index_dtype = np.dtype(headers["X-Data-Index-Dtype"])
    value_dtype = np.dtype(headers["X-Data-Value-Dtype"])
    split = nnz * index_dtype.itemsize
    indices = np.frombuffer(content[:split], dtype=index_dtype)
    values = np.frombuffer(content[split:], dtype=value_dtype)

    raw_fill = headers.get("X-Data-Fill-Value")
    fill = _fill_for(value_dtype, float(raw_fill) if raw_fill else None)
    flat = np.full(int(np.prod(shape)), fill, dtype=value_dtype)
    flat[indices] = values
    return offset, flat.reshape(shape, order=order)


class Grid(GridModel):
    """Grid resource for the FastFuels v2 API.

    A grid is a raster (2D) or voxel (3D) dataset within a domain: topography,
    canopy, surface fuel models, uploaded rasters, or grids derived from other
    grids. Grids are asynchronous job resources — creation starts a background
    job and returns a *pending* record; call :meth:`wait` to block until it is
    ready.

    Attributes
    ----------
    id : str
        Unique identifier for the grid.
    domain_id : str
        Identifier of the domain the grid belongs to.
    status : JobStatus
        Job status: "pending", "running", "completed", or "failed".
    source : GridSource
        Where the grid data comes from (e.g. "landfire", "3dep").
    bands : List[Band]
        The grid's data bands (keys, types, units).
    name : str
        Human-readable name for the grid.
    description : str
        Detailed description of the grid.
    progress : JobProgress, optional
        Progress info while the job is running.
    georeference : Georeference or Georeference3D, optional
        Spatial reference of the data; populated when the job completes.
    error : JobError, optional
        Error details if the job failed.
    chunks : Chunks, optional
        Chunk layout; populated when processing completes.
    tags : List[str], optional
        User-defined tags for organization.
    created_on : datetime
        When the grid was created.
    modified_on : datetime
        When the grid was last modified.

    Examples
    --------
    Create a topography grid and wait for it to complete:
    >>> import fastfuels_sdk as ff
    >>> grid = ff.grids.create_topography_grid_from_3dep(domain, output_resolution_m=10)
    >>> grid.wait()

    Get a grid by ID:
    >>> grid = ff.get_grid(domain, "def456")

    See Also
    --------
    create_topography_grid_from_3dep : Create a topography grid from USGS 3DEP.
    create_fuel_model_grid_from_landfire_fbfm40 : Create an FBFM40 fuel model grid.
    create_uniform_grid : Create a constant-value grid.
    list_grids : List grids in a domain or across all domains.
    """

    @classmethod
    def _from_model(cls, model: GridModel) -> "Grid":
        """Build a Grid from a generated Grid model instance.

        Round-trips through the generated to_dict/from_dict — from_dict
        constructs ``cls``, i.e. this subclass.
        """
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: GridModel) -> "Grid":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(GridModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    def _require_completed(self, action: str) -> None:
        """Raise if the grid is not completed, before deriving from it."""
        if self.status != JobStatus.COMPLETED:
            raise ValueError(
                f"Cannot {action} a grid with status '{self.status}'. Call "
                ".wait() until it completes first."
            )

    def _band(self, band: str):
        """Return the :class:`Band` with key ``band``, or raise if absent."""
        for grid_band in self.bands:
            if grid_band.key == band:
                return grid_band
        keys = [b.key for b in self.bands]
        raise ValueError(f"Grid has no band {band!r}. Available bands: {keys}.")

    @property
    def represented_year(self) -> Optional[int]:
        """Calendar year the fuel data represents, as reported by the API.

        Populated on LANDFIRE fuel model grids. For an annual product this is
        the landscape vintage (the ``version``); for a seasonal product it is
        the projected season year read from the LANDFIRE Product Service
        catalog. ``None`` when the source does not report a year.
        """
        # `source` is a free-form GridSource, so read the server-set `year`
        # off its additional properties rather than a typed attribute.
        if self.source is None:
            return None
        return self.source.additional_properties.get("year")

    @classmethod
    def from_id(cls, domain_id: str, grid_id: str) -> "Grid":
        """Retrieve an existing Grid resource by its ID.

        Parameters
        ----------
        domain_id : str
            The unique identifier of the domain the grid belongs to.
        grid_id : str
            The unique identifier of the grid to retrieve.

        Returns
        -------
        Grid
            The requested Grid object.

        Raises
        ------
        NotFoundException
            If no grid exists with the given IDs, or the user does not have
            access to it.
        """
        response = get_grid_endpoint.sync_detailed(
            domain_id, grid_id, client=ensure_client()
        )
        return cls._from_model(expect(response))

    def refresh(self) -> "Grid":
        """Update this Grid in place with the latest data from the API.

        Returns
        -------
        Grid
            ``self``, updated with the latest data (so calls chain).

        Raises
        ------
        NotFoundException
            If the grid no longer exists.
        """
        response = get_grid_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        return self._copy_fields_from(expect(response))

    def wait(self, timeout: Optional[float] = None, verbose: bool = False) -> "Grid":
        """Poll the grid job until it reaches a terminal status.

        Parameters
        ----------
        timeout : float, optional
            Maximum seconds to wait. ``None`` (default) waits indefinitely; the
            job runs server-side regardless, so a bounded wait is resumable.
        verbose : bool, optional
            If True, print the job status at each poll.

        Returns
        -------
        Grid
            ``self``, updated to its terminal state (so calls chain).

        Raises
        ------
        TimeoutError
            If ``timeout`` is set and elapses before a terminal status.
        JobFailedError
            If the job finished with status "failed".
        """
        return _wait(self, timeout=timeout, verbose=verbose)

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "Grid":
        """Update the grid's mutable metadata (name, description, tags) in place.

        Only provided fields are sent. If no fields are provided, no API call
        is made.

        Parameters
        ----------
        name : str, optional
            New name for the grid.
        description : str, optional
            New description for the grid.
        tags : List[str], optional
            New tags for the grid (replaces existing tags).

        Returns
        -------
        Grid
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the grid no longer exists.
        """
        if name is None and description is None and tags is None:
            return self
        request_body = UpdateGridRequestBody(
            name=_opt(name), description=_opt(description), tags=_opt(tags)
        )
        response = update_grid.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def delete(self) -> None:
        """Delete this grid and its data.

        Raises
        ------
        NotFoundException
            If the grid no longer exists.
        """
        response = delete_grid.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        expect(response, HTTPStatus.NO_CONTENT)

    def duplicate(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "Grid":
        """Create an independent copy of this grid under a new ID.

        The copy is a true clone — the finished data is byte-copied, not
        re-derived — carrying over the source's ``source``, ``modifications``,
        ``georeference``, and ``checksum`` verbatim; only its ``id`` and
        timestamps differ. Use this to branch from a grid before modifying the
        copy while the original stays untouched.

        Parameters
        ----------
        name : str, optional
            Name for the copy. Defaults to the source's name.
        description : str, optional
            Description for the copy. Defaults to the source's description.
        tags : List[str], optional
            Tags for the copy. Defaults to the source's tags.

        Returns
        -------
        Grid
            The new Grid object (job status "pending" while the data is
            copied; call :meth:`wait` before using it).

        Raises
        ------
        NotFoundException
            If the grid no longer exists.
        """
        request_body = DuplicateGridRequest(
            name=_opt(name), description=_opt(description), tags=_opt(tags)
        )
        response = duplicate_grid_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return Grid._from_model(expect(response, HTTPStatus.CREATED))

    def resample(
        self,
        output_resolution_m: Optional[float] = None,
        align_to=None,
        align: Optional[str] = None,
        resampling: Optional[str] = None,
        method_overrides=None,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        modifications: Optional[list] = None,
    ) -> "Grid":
        """Create a new grid by resampling this grid onto a different lattice.

        Parameters
        ----------
        output_resolution_m : float, optional
            Output cell size in meters, anchored to the domain origin.
        align_to : Grid or str, optional
            Match the lattice of an existing grid (or its id).
        align : str, optional
            Pass ``"native"`` to keep this grid's pixel anchor.
        resampling : str, optional
            Resampling method (e.g. "bilinear", "nearest", "average").
        method_overrides : CreateResampleRequestMethodOverrides, optional
            Per-band resampling method overrides.
        name, description : str, optional
            Metadata for the new grid.
        tags : List[str], optional
            Tags for the new grid.
        modifications : list, optional
            Modification rules applied after the grid is built.

        Returns
        -------
        Grid
            The new (pending) resampled Grid.
        """
        self._require_completed("resample")
        request_body = CreateResampleRequest(
            source_grid_id=self.id,
            alignment=_build_alignment(
                output_resolution_m, align_to, align, resampling
            ),
            method_overrides=_opt(method_overrides),
            name=name,
            description=description,
            tags=_opt(tags),
            modifications=_opt(modifications),
        )
        response = create_resample.sync_detailed(
            self.domain_id, client=ensure_client(), body=request_body
        )
        return Grid._from_model(expect(response, HTTPStatus.CREATED))

    def apply_modifications(self, modifications: list) -> "Grid":
        """Apply modification rules to this grid in place.

        The grid keeps its ID; the submitted rules are appended to its
        cumulative ``modifications`` list and the data is re-derived as a
        background job — the grid returns to "pending" status, so call
        :meth:`wait` before using its data. Unlike a creator's
        ``modifications=`` argument (applied while the grid is first built),
        this modifies a grid you already hold.

        Parameters
        ----------
        modifications : list
            Modification rules (``GridModification``). Build feature masks with
            :func:`fastfuels_sdk.v2.modifications.mask` (``ff.mask``); each rule
            pairs conditions (spatial or band-value tests, ANDed) with actions
            that rewrite band values for the matching cells.

        Returns
        -------
        Grid
            ``self``, updated (so calls chain).

        Raises
        ------
        ValueError
            If the grid is not completed.
        NotFoundException
            If the grid no longer exists.

        Examples
        --------
        >>> import fastfuels_sdk.v2 as ff
        >>> grid.apply_modifications([ff.mask(roads, "fbfm", 91, buffer_m=5)])
        >>> grid.wait()
        """
        self._require_completed("apply modifications to")
        request_body = ApplyGridModificationsRequest(modifications=list(modifications))
        response = apply_grid_modifications_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def export(
        self,
        format: str = "geotiff",
        bands: Optional[List[str]] = None,
        expiration_days: int = 7,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
    ):
        """Export this grid to a downloadable file format.

        Parameters
        ----------
        format : str, optional
            Export format: "geotiff" (2D only), "netcdf", or "zarr"
            (default "geotiff").
        bands : List[str], optional
            Band keys to include (default: all bands).
        expiration_days : int, optional
            Days until the signed download URL expires (max 7, default 7).
        name, description : str, optional
            Metadata for the export.
        tags : List[str], optional
            Tags for the export.

        Returns
        -------
        Export
            The created Export object (job status "pending"). Call
            :meth:`Export.wait` and then :meth:`Export.to_file` to download
            the file.
        """
        # Lazy import so the modules stay decoupled (exports never imports
        # grids).
        from fastfuels_sdk.v2.exports import Export

        request_body = ExportGridRequest(
            bands=_opt(bands),
            expiration_days=expiration_days,
            name=name,
            description=description,
            tags=_opt(tags),
        )
        response = create_grid_export.sync_detailed(
            self.domain_id,
            self.id,
            GridExportFormat(format),
            client=ensure_client(),
            body=request_body,
        )
        return Export._from_model(expect(response, HTTPStatus.CREATED))

    def _chunk_count(self) -> int:
        """Number of chunks the completed grid's data is split into."""
        count = self.chunks.count if self.chunks is not None else None
        if count is UNSET or count is None:
            raise ValueError(
                "Grid chunk layout is unavailable. Call .refresh() once the "
                "job has completed before reading data."
            )
        return count

    def _request_chunk(self, band: str, chunk_index: int, array_format: str):
        """GET one (band, chunk) as a raw octet-stream ``httpx.Response``.

        Bypasses ``get_grid_data_binary.sync_detailed()``, whose generated
        parser JSON-decodes the binary body and raises (tracked in #184). We
        reuse its ``_get_kwargs()`` for correct URL/param construction, then
        issue the request through the shared client and read the bytes/headers
        off the response directly.
        """
        kwargs = get_grid_data_binary._get_kwargs(
            self.domain_id,
            self.id,
            band,
            chunk_index,
            array_format=GridDataArrayFormat(array_format),
            order=GridDataOrder.C,
        )
        return ensure_client().get_httpx_client().request(**kwargs)

    def _read_chunk(self, band: str, chunk_index: int, array_format: str):
        """Fetch and decode one chunk, retrying oversized dense chunks as sparse."""
        response = self._request_chunk(band, chunk_index, array_format)
        if (
            response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE
            and array_format == "dense"
        ):
            # The API returns 413 for an oversized dense chunk and suggests
            # the sparse encoding; honor that hint transparently.
            response = self._request_chunk(band, chunk_index, "sparse")
        if response.status_code != HTTPStatus.OK:
            raise_for_response(
                Response(
                    status_code=HTTPStatus(response.status_code),
                    content=response.content,
                    headers=response.headers,
                    parsed=None,
                )
            )
        return _decode_grid_chunk(response.content, response.headers)

    def band_summary(self, band: str):
        """Return summary statistics for one band, without downloading the data.

        The server computes a per-band summary when the grid completes, so this
        is a cheap overview that does not fetch the grid's cells (unlike
        :meth:`to_numpy`).

        Parameters
        ----------
        band : str
            The band key to summarize (see :attr:`bands` for available keys).

        Returns
        -------
        ContinuousBandSummary or CategoricalBandSummary or None
            The band's summary, discriminated by its ``type_``:
            ``"continuous"`` carries ``count``, ``nodata_count``, ``min_``,
            ``max_``, ``mean``, and ``std``; ``"categorical"`` carries
            ``count``, ``nodata_count``, and ``unique_count``. ``None`` until
            the grid completes (call :meth:`wait` first).

        Raises
        ------
        ValueError
            If ``band`` is not one of the grid's bands.

        Examples
        --------
        >>> grid = ff.get_grid(domain, "def456").wait()
        >>> grid.band_summary("elevation").mean
        2143.7
        """
        summary = self._band(band).summary
        return None if summary is UNSET else summary

    def to_numpy(self, band: str) -> "np.ndarray":
        """Read one band of this grid into an in-memory NumPy array.

        Fetches every chunk of ``band`` and reassembles them into a single
        array shaped like the full grid: 2D ``(y, x)`` for rasters, 3D
        ``(z, y, x)`` for voxel grids. Chunks are requested in the dense
        encoding for 2D grids and the sparse encoding for 3D grids, matching
        how the data is stored.

        Parameters
        ----------
        band : str
            The band key to read (see :attr:`bands` for available keys).

        Returns
        -------
        numpy.ndarray
            The band's values. Cells with no data carry the band's ``nodata``
            value, or NaN (floating dtypes) / 0 (integer dtypes) when the band
            defines none.

        Raises
        ------
        ValueError
            If the grid is not completed, or ``band`` is not one of its bands.

        Examples
        --------
        >>> grid = ff.get_grid(domain, "def456").wait()
        >>> elevation = grid.to_numpy("elevation")
        >>> elevation.shape
        (1200, 1600)
        """
        self._require_completed("read data from")
        nodata = self._band(band).nodata
        # 3D grids are stored sparsely; 2D rasters densely (413 falls back).
        array_format = "sparse" if len(self.georeference.shape) == 3 else "dense"

        full = None
        for chunk_index in range(self._chunk_count()):
            offset, block = self._read_chunk(band, chunk_index, array_format)
            if full is None:
                full = np.full(
                    tuple(self.georeference.shape),
                    _fill_for(block.dtype, nodata),
                    dtype=block.dtype,
                )
            slices = tuple(slice(o, o + s) for o, s in zip(offset, block.shape))
            full[slices] = block
        return full

    def to_xarray(self):
        """Read this grid's bands into an in-memory :class:`xarray.Dataset`.

        Each band becomes a data variable over ``(y, x)`` (2D) or
        ``(z, y, x)`` (3D), with ``x``/``y`` (and ``z``) coordinate vectors
        derived from the grid's affine transform and the CRS recorded on the
        dataset's ``crs`` attribute.

        Returns
        -------
        xarray.Dataset
            All bands of the grid as aligned data variables.

        Raises
        ------
        ValueError
            If the grid is not completed.

        Examples
        --------
        >>> grid = ff.get_grid(domain, "def456").wait()
        >>> ds = grid.to_xarray()
        >>> ds["elevation"].mean().item()
        2143.7
        """
        import xarray as xr

        self._require_completed("read data from")
        is_3d = len(self.georeference.shape) == 3
        dims = ("z", "y", "x") if is_3d else ("y", "x")
        data_vars = {b.key: (dims, self.to_numpy(b.key)) for b in self.bands}
        return xr.Dataset(
            data_vars=data_vars,
            coords=self._coords(is_3d),
            attrs={"crs": self.georeference.crs},
        )

    def _coords(self, is_3d: bool) -> dict:
        """Build x/y(/z) cell-center coordinate vectors from the georeference.

        Assumes a north-up affine (no rotation), the convention for FastFuels
        grids: ``transform`` is the six-element ``(a, b, c, d, e, f)`` mapping
        ``x = a*col + c`` and ``y = e*row + f``.
        """
        geo = self.georeference
        a, _b, c, _d, e, f = geo.transform[:6]
        shape = geo.shape
        ny, nx = (shape[1], shape[2]) if is_3d else (shape[0], shape[1])
        coords = {
            "x": c + a * (np.arange(nx) + 0.5),
            "y": f + e * (np.arange(ny) + 0.5),
        }
        if is_3d:
            coords["z"] = geo.z_origin + geo.z_resolution * (np.arange(shape[0]) + 0.5)
        return coords

    def to_json(self) -> str:
        """Serialize the complete Grid object to a JSON string.

        Returns
        -------
        str
            The Grid as a pretty-printed JSON string.
        """
        return json.dumps(self.to_dict(), default=str, indent=2)


# ---------------------------------------------------------------------------
# Create grids from an external source (module-level functions)
# ---------------------------------------------------------------------------


def create_topography_grid_from_3dep(
    domain,
    source_resolution_m: int = 10,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    bands: Optional[list] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a topography grid from USGS 3DEP elevation data.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    source_resolution_m : int, optional
        The 3DEP product family to draw from: 1, 10, or 30 meters
        (default 10). Use :func:`check_3dep_coverage` first for 1 m data.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin. By default
        the source resolution is kept.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method (e.g. "bilinear", "cubic").
    bands : list, optional
        Topography bands to produce (``TopographyBand`` members or their string
        keys, e.g. "elevation", "slope", "aspect"). Defaults to all.
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    request_body = CreateThreeDepTopographyRequest(
        source_resolution=ThreeDepResolution(source_resolution_m),
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        bands=_enum_list(bands, TopographyBand),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_3dep_topography.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_topography_grid_from_landfire(
    domain,
    version: Optional[str] = None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    bands: Optional[list] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a topography grid from LANDFIRE elevation data.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    version : str, optional
        LANDFIRE version (see ``LandfireTopographyVersion``). Defaults to the
        API's current version.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method (e.g. "bilinear", "cubic").
    bands : list, optional
        Topography bands to produce (``TopographyBand`` members or their string
        keys). Defaults to all.
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    request_body = CreateLandfireTopographyRequest(
        version=(LandfireTopographyVersion(version) if version is not None else UNSET),
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        bands=_enum_list(bands, TopographyBand),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_landfire_topography.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_canopy_fuel_grid_from_landfire(
    domain,
    version: Optional[str] = None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    bands: Optional[list] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a canopy fuel grid from LANDFIRE data.

    Produces canopy fuel bands (e.g. canopy bulk density, canopy base height,
    canopy cover, canopy height) within the domain.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    version : str, optional
        LANDFIRE version (see ``LandfireCanopyVersion``). Defaults to the API's
        current version.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method (e.g. "bilinear", "cubic").
    bands : list, optional
        Canopy fuel bands to produce (``LandfireCanopyFuelBand`` members or
        their string keys). Defaults to all.
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    request_body = CreateLandfireCanopyRequest(
        version=LandfireCanopyVersion(version) if version is not None else UNSET,
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        bands=_enum_list(bands, LandfireCanopyFuelBand),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_landfire_canopy.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


# Named-method aliases for the per-band canopy reduction kwargs. Each maps a
# friendly string to the request model built with its default parameters; a
# caller who needs non-default parameters passes the model instance directly.
_CBD_METHODS = {
    "load_over_depth": CanopyCbdLoadOverDepth,
    "running_mean": CanopyCbdRunningMean,
}
_CBH_METHODS = {
    "mean": CanopyCbhMean,
    "minimum": CanopyCbhMinimum,
    "percentile": CanopyCbhPercentile,
    "threshold": CanopyProfileThreshold,
}
_CHM_METHODS = {
    "percentile": CanopyChmHeightPercentile,
    "threshold": CanopyProfileThreshold,
}
_CC_METHODS = {
    "cover_fraction": CanopyCcCoverFraction,
    "crown_overlap": CanopyCcCrownOverlap,
    "crown_union": CanopyCcCrownUnion,
}


def _canopy_method(value, name: str, methods: dict):
    """Resolve a per-band canopy method kwarg to its request model or UNSET.

    ``value`` may be ``None`` (UNSET), a string naming a default-parameter
    method in ``methods``, or a prebuilt method model (passed through).
    """
    if value is None:
        return UNSET
    if isinstance(value, str):
        factory = methods.get(value)
        if factory is None:
            raise ValueError(
                f"{name} must be one of {sorted(methods)} or a canopy "
                f"{name} method object, got {value!r}."
            )
        # CanopyCbhPercentile requires an explicit percentile; steer the
        # caller to the model instead of constructing an invalid default.
        try:
            return factory()
        except TypeError:
            raise ValueError(
                f'{name}="{value}" needs parameters; pass the method object, '
                f"e.g. {factory.__name__}(...)."
            ) from None
    return value


def _canopy_biomass_source(equations, column):
    """Build the biomass source union from friendly kwargs, or UNSET."""
    if equations is not None and column is not None:
        raise ValueError("Specify at most one of biomass_equations or biomass_column.")
    if column is not None:
        return InventoryColumnCanopyBiomassSource(column=column)
    if equations is not None:
        return AllometryCanopyBiomassSource(equations=CanopyBiomassEquations(equations))
    return UNSET


def _canopy_available_fuel(foliage_fraction, branchwood_fraction, size_partition):
    """Build the available-fuel reduction from friendly kwargs, or UNSET."""
    if (
        foliage_fraction is None
        and branchwood_fraction is None
        and size_partition is None
    ):
        return UNSET
    branchwood = UNSET
    if branchwood_fraction is not None or size_partition is not None:
        branchwood = CanopyBranchwood(
            fraction=_opt(branchwood_fraction),
            size_partition=(
                CanopyBranchwoodSizePartition(size_partition)
                if size_partition is not None
                else UNSET
            ),
        )
    return CanopyAvailableFuel(
        foliage_fraction=_opt(foliage_fraction), branchwood=branchwood
    )


def _canopy_max_crown_radius_source(equations, column):
    """Build the max-crown-radius source union from friendly kwargs, or UNSET."""
    if equations is not None and column is not None:
        raise ValueError(
            "Specify at most one of max_crown_radius_equations or "
            "max_crown_radius_column."
        )
    if column is not None:
        return InventoryColumnMaxCrownRadiusSource(column=column)
    if equations is not None:
        return CanopyAllometryMaxCrownRadiusSource(
            equations=CanopyCrownWidthEquations(equations)
        )
    return UNSET


def _canopy_crown_class_adjustment(value):
    """Resolve the crown-class adjustment kwarg to its union model or UNSET."""
    if value is None:
        return UNSET
    if value == "none":
        return CanopyNoCrownClassAdjustment()
    if value == "fuelcalc_table":
        return CanopyFuelcalcCrownClassAdjustment()
    raise ValueError(
        f'crown_class_adjustment must be "none" or "fuelcalc_table", ' f"got {value!r}."
    )


def create_canopy_fuel_grid_from_inventory(
    inventory,
    bands: Optional[list] = None,
    biomass_equations: Optional[str] = None,
    biomass_column: Optional[str] = None,
    foliage_fraction: Optional[float] = None,
    branchwood_fraction: Optional[float] = None,
    branchwood_size_partition: Optional[str] = None,
    species_inclusion: Optional[str] = None,
    crown_class_adjustment: Optional[str] = None,
    min_tree_height: Optional[float] = None,
    vertical_distribution: Optional[str] = None,
    layer_depth: Optional[float] = None,
    horizontal_distribution: Optional[str] = None,
    max_crown_radius_equations: Optional[str] = None,
    max_crown_radius_column: Optional[str] = None,
    cbd=None,
    cbh=None,
    chm=None,
    cc=None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    resampling: Optional[str] = None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Grid:
    """Create a canopy fuel grid from a completed tree inventory.

    Derives the canopy metrics fire models consume — canopy bulk density
    (``cbd``), canopy base height (``cbh``), canopy height (``chm``), canopy
    cover (``cc``), and optionally canopy fuel load (``cfl``) — for each cell
    directly from the inventory's trees. Only live trees contribute canopy
    fuel. The bands share keys and units with the LANDFIRE canopy source.

    Parameters
    ----------
    inventory : Inventory or str
        A completed tree inventory (or its id) to derive canopy metrics from.
        Passing the id alone requires the inventory to be reachable for its
        domain; pass the Inventory object to avoid an extra lookup.
    bands : list, optional
        Output bands (``InventoryCanopyBand`` members or their string keys:
        "cbd", "cbh", "chm", "cc", "cfl"). Defaults to the four canopy bands
        ``cbd``, ``cbh``, ``chm``, and ``cc``.
    biomass_equations : str, optional
        Allometric equations for crown biomass: "nsvb" (default), "jenkins",
        or "brown_1978". Mutually exclusive with ``biomass_column``.
    biomass_column : str, optional
        Inventory column holding precomputed per-tree available canopy fuel,
        used in place of allometry. Mutually exclusive with
        ``biomass_equations``; when set, ``available_fuel``, species
        inclusion, and crown-class adjustment do not affect fuel magnitude.
    foliage_fraction : float, optional
        Fraction of foliage biomass counted as available fuel (allometry
        only, default 1.0).
    branchwood_fraction : float, optional
        Fraction of the branchwood size basis counted as available fuel
        (allometry only).
    branchwood_size_partition : str, optional
        Size basis for the branchwood fraction: "equations",
        "brown_proportions", or "none" (allometry only).
    species_inclusion : str, optional
        Which species contribute: "all_species" or "fuelcalc_default" (which
        excludes most hardwoods).
    crown_class_adjustment : str, optional
        Crown-weight adjustment for canopy position: "none" (default) or
        "fuelcalc_table".
    min_tree_height : float, optional
        Trees shorter than this height in meters contribute no canopy fuel
        (default 0.0).
    vertical_distribution : str, optional
        How each tree's fuel stacks over its crown: "reinhardt_2006" or
        "uniform".
    layer_depth : float, optional
        Vertical profile layer depth in meters (default 0.3048).
    horizontal_distribution : str, optional
        How a tree's fuel is attributed to cells: "crown_projected" (default)
        or "stem".
    max_crown_radius_equations : str, optional
        Allometric equations for maximum crown radius: "purves" (default) or
        "crookston_stage". Mutually exclusive with
        ``max_crown_radius_column``.
    max_crown_radius_column : str, optional
        Inventory column holding per-tree maximum crown radius in meters, used
        in place of allometry. Mutually exclusive with
        ``max_crown_radius_equations``.
    cbd : str or CanopyCbdLoadOverDepth or CanopyCbdRunningMean, optional
        Canopy bulk density method: "load_over_depth", "running_mean", or a
        method object for non-default parameters.
    cbh : str or method object, optional
        Canopy base height method: "mean", "minimum", "percentile",
        "threshold", or a method object (``CanopyCbhMean``,
        ``CanopyCbhMinimum``, ``CanopyCbhPercentile``, or
        ``CanopyProfileThreshold``) for non-default parameters.
    chm : str or method object, optional
        Canopy height method: "percentile", "threshold", or a method object
        (``CanopyChmHeightPercentile`` or ``CanopyProfileThreshold``).
    cc : str or method object, optional
        Canopy cover method: "cover_fraction", "crown_overlap", "crown_union",
        or a method object for non-default parameters.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin. Defaults to
        30 m when no alignment target is given.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    resampling : str, optional
        Resampling method for the alignment target.
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").

    Raises
    ------
    ValueError
        If ``inventory`` is passed as a bare id with no resolvable domain, if
        mutually exclusive kwargs are combined, or if a method name is
        unknown.

    Examples
    --------
    >>> import fastfuels_sdk.v2 as ff
    >>> grid = ff.grids.create_canopy_fuel_grid_from_inventory(
    ...     inventory, bands=["cbd", "cbh", "chm", "cc", "cfl"]
    ... )
    >>> grid.wait()
    """
    domain_id = getattr(inventory, "domain_id", None)
    if domain_id is None:
        raise ValueError(
            "Pass an Inventory object so its domain can be resolved; a bare "
            "inventory id does not identify a domain."
        )
    source_inventory_id = getattr(inventory, "id", inventory)

    request_body = CreateInventoryCanopyRequest(
        source_inventory_id=source_inventory_id,
        biomass_source=_canopy_biomass_source(biomass_equations, biomass_column),
        available_fuel=_canopy_available_fuel(
            foliage_fraction, branchwood_fraction, branchwood_size_partition
        ),
        species_inclusion=(
            CanopySpeciesInclusion(species_inclusion)
            if species_inclusion is not None
            else UNSET
        ),
        crown_class_adjustment=_canopy_crown_class_adjustment(crown_class_adjustment),
        min_tree_height=_opt(min_tree_height),
        vertical_distribution=(
            CanopyVerticalDistribution(vertical_distribution)
            if vertical_distribution is not None
            else UNSET
        ),
        layer_depth=_opt(layer_depth),
        horizontal_distribution=(
            CanopyHorizontalDistribution(horizontal_distribution)
            if horizontal_distribution is not None
            else UNSET
        ),
        max_crown_radius_source=_canopy_max_crown_radius_source(
            max_crown_radius_equations, max_crown_radius_column
        ),
        cbd=_canopy_method(cbd, "cbd", _CBD_METHODS),
        cbh=_canopy_method(cbh, "cbh", _CBH_METHODS),
        chm=_canopy_method(chm, "chm", _CHM_METHODS),
        cc=_canopy_method(cc, "cc", _CC_METHODS),
        bands=_enum_list(bands, InventoryCanopyBand),
        alignment=_build_alignment(
            output_resolution_m, align_to, resampling=resampling
        ),
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_inventory_canopy_grid.sync_detailed(
        domain_id, client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_canopy_height_grid_from_meta(
    domain,
    version: Optional[str] = None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a canopy height grid from the Meta Canopy Height Model.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    version : str, optional
        Meta CHM version (see ``MetaCHMVersion``). Defaults to the API's
        current version.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method (e.g. "bilinear", "cubic").
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    request_body = CreateMetaChmRequest(
        version=MetaCHMVersion(version) if version is not None else UNSET,
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_meta_chm.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_canopy_height_grid_from_naip_chm(
    domain,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a canopy height grid from the NAIP-CHM model.

    NAIP-CHM is a 0.6 m canopy height and structure model covering the
    contiguous US (CONUS). The grid carries a single continuous ``chm`` band
    (above-ground height in meters).

    NAIP-CHM is a surface model (nDSM): it captures the top of *all*
    above-ground structure — vegetation **and** buildings/infrastructure — not
    vegetation alone. To model vegetative fuels only, subtract built structures
    with ``modifications=`` (e.g. a building-footprint mask). Coverage is
    CONUS-only; domains outside it return no data.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin. The source
        is 0.6 m; coarser outputs are resampled.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method for the continuous height band (e.g. "bilinear",
        "cubic").
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").

    References
    ----------
    Morford, S. L., Allred, B. W., Coons, S. P., Marcozzi, A. A., McCord, S. E.,
    Smith, J. T., & Naugle, D. E. (2025). A 0.6-meter resolution canopy height
    and structure model for the contiguous United States. bioRxiv.
    https://doi.org/10.64898/2025.12.12.694075

    Dataset and model code: https://github.com/smorf-ntsg/naip-chm
    """
    request_body = CreateNaipChmRequest(
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_naip_chm.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_canopy_height_grid_from_point_cloud(
    point_cloud: "PointCloud",
    output_resolution_m: Optional[float] = None,
    align_to=None,
    resampling: Optional[str] = None,
    aggregation: Optional[str] = None,
    percentile: Optional[float] = None,
    spike_filter=None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a canopy height grid from a completed airborne point cloud.

    Parameters
    ----------
    point_cloud : PointCloud
        The completed airborne point cloud to rasterize.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin. Defaults to
        1 meter when no alignment target is provided.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    resampling : str, optional
        Resampling method for the continuous canopy-height band.
    aggregation : str, optional
        Statistic each cell reduces its above-ground return heights with: one of
        ``"max"``, ``"mean"``, ``"median"``, or ``"percentile"``. Defaults to the
        API's ``"max"``.
    percentile : float, optional
        Rank to take (0-100), used only with ``aggregation="percentile"``. 100 is
        the tallest return and 50 the median.
    spike_filter : bool, Mapping, or ChmSpikeFilter, optional
        Removal of lone spurious returns. ``None`` (the default) applies the
        API's default filter; ``False`` disables it, keeping every return;
        ``True`` applies a default ``ChmSpikeFilter``; a mapping of filter fields
        (``min_canopy_footprint_m``, ``min_prominence_m``) or a ``ChmSpikeFilter``
        sets custom thresholds.
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created canopy-height Grid (job status "pending" or "running").

    Raises
    ------
    ValueError
        If the point cloud is not completed or is not airborne, or if the
        aggregation and percentile arguments are inconsistent.
    """
    if point_cloud.status != JobStatus.COMPLETED:
        raise ValueError(
            f"Point cloud {point_cloud.id} must be completed before creating "
            f"a canopy height grid (current status: {point_cloud.status.value})."
        )
    if point_cloud.type_.value != "als":
        raise ValueError(
            f"Point cloud {point_cloud.id} must be airborne (ALS) to create a "
            f"canopy height grid (got {point_cloud.type_.value!r})."
        )

    request_body = CreatePointCloudChmRequest(
        source_point_cloud_id=point_cloud.id,
        alignment=_build_alignment(
            output_resolution_m,
            align_to,
            resampling=resampling,
        ),
        aggregation=_build_chm_aggregation(aggregation, percentile),
        spike_filter=_build_chm_spike_filter(spike_filter),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_point_cloud_chm.sync_detailed(
        point_cloud.domain_id,
        client=ensure_client(),
        body=request_body,
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_fuel_model_grid_from_landfire_fbfm13(
    domain,
    version: Optional[str] = None,
    remove_non_burnable: Optional[list] = None,
    boundary_scatter=None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a fuel model grid from LANDFIRE Anderson 13 fuel models.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    version : str, optional
        LANDFIRE version (``"2023"`` or ``"2024"``). Defaults to the API's
        current version.
    remove_non_burnable : list, optional
        Non-burnable fuel models to drop (``NonBurnableFuelModel`` members or
        their string keys, e.g. ``"NB1"``, ``"NB2"``).
    boundary_scatter : bool, dict, or BoundaryScatter, optional
        Stochastic scattering of fuel model boundaries to create ragged,
        natural-looking transitions instead of staircase edges from
        nearest-neighbor resampling. ``None`` (default) disables scatter.
        ``True`` or ``{}`` enables scatter with defaults (``depth=10``,
        ``seed=42``). A dict (e.g. ``{"depth": 5, "seed": 123}``) or a
        ``BoundaryScatter`` instance sets explicit parameters.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method (e.g. ``"nearest"`` for categorical fuel models).
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status ``"pending"`` or ``"running"``).
    """
    request_body = CreateLandfireFbfm13Request(
        version=LandfireFbfm13Version(version) if version is not None else UNSET,
        remove_non_burnable=_enum_list(remove_non_burnable, NonBurnableFuelModel),
        boundary_scatter=_build_boundary_scatter(boundary_scatter),
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_landfire_fbfm13.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_fuel_model_grid_from_landfire_fbfm40(
    domain,
    version: Optional[str] = None,
    season: Optional[str] = None,
    remove_non_burnable: Optional[list] = None,
    boundary_scatter=None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a fuel model grid from LANDFIRE 40 Scott & Burgan fuel models.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    version : str, optional
        LANDFIRE version (see ``LandfireFbfm40Version``). Defaults to the API's
        current version. Seasonal versions (see ``season``) are only available
        for the LANDFIRE Seasonal Fuels vintages (e.g. "2025").
    season : str, optional
        LANDFIRE Seasonal Fuels window (see ``LandfireSeason``): "ES" (early
        spring), "SP" (spring), "SU" (summer), or "FA" (fall). When set, the
        grid is fetched from the LANDFIRE Product Service for that season rather
        than the staged annual release, and ``version`` must be a seasonal
        vintage (e.g. "2025"). When omitted, ``version`` must be an annual
        vintage. ``represented_year`` reflects the projected season year.
    remove_non_burnable : list, optional
        Non-burnable fuel models to drop (``NonBurnableFuelModel`` members or
        their string keys, e.g. "NB1", "NB2").
    boundary_scatter : bool, dict, or BoundaryScatter, optional
        Stochastic scattering of fuel model boundaries to create ragged,
        natural-looking transitions instead of staircase edges from
        nearest-neighbor resampling. ``None`` (default) disables scatter.
        ``True`` or ``{}`` enables scatter with defaults (``depth=10``,
        ``seed=42``). A dict (e.g. ``{"depth": 5, "seed": 123}``) or a
        ``BoundaryScatter`` instance sets explicit parameters.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method (e.g. "nearest" for categorical fuel models).
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    request_body = CreateLandfireFbfm40Request(
        version=LandfireFbfm40Version(version) if version is not None else UNSET,
        season=LandfireSeason(season) if season is not None else UNSET,
        remove_non_burnable=_enum_list(remove_non_burnable, NonBurnableFuelModel),
        boundary_scatter=_build_boundary_scatter(boundary_scatter),
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_landfire_fbfm40.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_fuel_model_grid_from_landfire_fccs(
    domain,
    version: Optional[str] = None,
    remove_bare_ground: bool = False,
    boundary_scatter=None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a fuel model grid from LANDFIRE FCCS fuelbeds.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    version : str, optional
        LANDFIRE version (see ``LandfireFccsVersion``). Defaults to the API's
        current version.
    remove_bare_ground : bool, optional
        Drop bare-ground fuelbeds (default False).
    boundary_scatter : bool, dict, or BoundaryScatter, optional
        Stochastic scattering of fuelbed boundaries to create ragged,
        natural-looking transitions instead of staircase edges from
        nearest-neighbor resampling. ``None`` (default) disables scatter.
        ``True`` or ``{}`` enables scatter with defaults (``depth=10``,
        ``seed=42``). A dict (e.g. ``{"depth": 5, "seed": 123}``) or a
        ``BoundaryScatter`` instance sets explicit parameters.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method (e.g. "nearest" for categorical fuelbeds).
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    request_body = CreateLandfireFccsRequest(
        version=LandfireFccsVersion(version) if version is not None else UNSET,
        remove_bare_ground=remove_bare_ground,
        boundary_scatter=_build_boundary_scatter(boundary_scatter),
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_landfire_fccs.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_pim_grid_from_treemap(
    domain,
    version: Optional[str] = None,
    output_resolution_m: Optional[float] = None,
    align_to=None,
    align: Optional[str] = None,
    resampling: Optional[str] = None,
    bands: Optional[list] = None,
    extent_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a Plot Imputation Map (PIM) grid from TreeMap.

    TreeMap imputes an FIA plot to every forested 30 m pixel across the
    conterminous US. The resulting grid carries up to two categorical bands:

    - ``tm_id``: the TreeMap raster pixel value (always present)
    - ``plt_cn``: the FIA plot condition number (request via ``bands``)

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    version : str, optional
        TreeMap version (see ``TreeMapVersion``). Defaults to the API's
        current version.
    output_resolution_m : float, optional
        Output cell size in meters, anchored to the domain origin.
    align_to : Grid or str, optional
        Match the lattice of an existing grid (or its id).
    align : str, optional
        Pass ``"native"`` to keep the source raster's pixel anchor.
    resampling : str, optional
        Resampling method. TreeMap bands are categorical, so use "nearest"
        (interpolating plot ids is meaningless).
    bands : list, optional
        TreeMap bands to produce (``TreeMapBand`` members or their string
        keys: "tm_id", "plt_cn"). Defaults to ``tm_id`` only.
    extent_buffer_cells : int, optional
        Result-grid cells to buffer around the domain extent (0-10, default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    request_body = CreateTreeMapRequest(
        version=TreeMapVersion(version) if version is not None else UNSET,
        alignment=_build_alignment(output_resolution_m, align_to, align, resampling),
        bands=_enum_list(bands, TreeMapBand),
        extent_buffer_cells=extent_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_treemap.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


# ---------------------------------------------------------------------------
# Create grids from your own file / supplied values
# ---------------------------------------------------------------------------


def create_grid_from_geotiff(
    domain,
    path: str,
    bands: list,
    num_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Grid:
    """Create a grid by uploading a local GeoTIFF.

    Creates the grid resource, uploads the file to the returned signed URL, and
    returns the (pending) Grid. The GeoTIFF's CRS must match the domain CRS.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    path : str
        Path to the local ``.tif``/``.tiff`` file (max 1 GB).
    bands : list
        Band definitions (``UploadBandDefinition``) mapping 1:1 to the GeoTIFF
        raster bands in order.
    num_buffer_cells : int, optional
        Cells kept around the domain extent in the stored grid (default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.

    Returns
    -------
    Grid
        The created Grid object (job status "pending"). Call :meth:`Grid.wait`
        to block until the uploaded file is processed.
    """
    request_body = CreateGeoTIFFUploadRequest(
        bands=bands,
        num_buffer_cells=num_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_geotiff_upload.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    created = expect(response, HTTPStatus.CREATED)
    put_upload(created.upload, path)
    return Grid._from_model(created.grid)


def create_grid_from_netcdf(
    domain,
    path: str,
    num_buffer_cells: int = 0,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Grid:
    """Create a grid by uploading a local NetCDF file.

    Creates the grid resource, uploads the file to the returned signed URL, and
    returns the (pending) Grid.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    path : str
        Path to the local NetCDF file.
    num_buffer_cells : int, optional
        Cells kept around the domain extent in the stored grid (default 0).
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.

    Returns
    -------
    Grid
        The created Grid object (job status "pending"). Call :meth:`Grid.wait`
        to block until the uploaded file is processed.
    """
    request_body = CreateNetcdfUploadRequest(
        num_buffer_cells=num_buffer_cells,
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_netcdf_upload.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    created = expect(response, HTTPStatus.CREATED)
    put_upload(created.upload, path)
    return Grid._from_model(created.grid)


def create_uniform_grid(
    domain,
    resolution_m: float,
    bands: Dict[str, Union[float, int]],
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a uniform (constant-value) grid.

    Each band fills the entire domain with a single value at the given
    resolution.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the grid in.
    resolution_m : float
        Grid cell size in meters (required — uniform grids have no native
        resolution).
    bands : dict
        Mapping of band key to constant value, e.g.
        ``{"fuel_load": 0.5, "fuel_moisture": 15.0}``. Keys must be valid
        ``UniformBand`` values.
    name, description : str, optional
        Metadata for the grid.
    tags : List[str], optional
        Tags for the grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The created Grid object (job status "pending" or "running").
    """
    band_inputs = [
        UniformBandInput(key=UniformBand(key), value=value)
        for key, value in bands.items()
    ]
    request_body = CreateUniformRequest(
        resolution=resolution_m,
        bands=band_inputs,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_uniform_grid_endpoint.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_grid_from_compose(
    inputs: Mapping[str, "Grid"],
    *,
    select: Optional[list] = None,
    compute: Optional[list] = None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a grid by selecting and computing bands from aligned grids.

    Parameters
    ----------
    inputs : mapping of str to Grid
        Alias-to-grid mapping for completed, aligned 2D grids in one domain.
        Operations refer to their bands as ``"alias.band_key"``.
    select : list of ComposeSelect, optional
        Bands to copy, built with :func:`fastfuels_sdk.v2.compose.select`.
    compute : list of ComposeCompute, optional
        Bands to calculate, built with
        :func:`fastfuels_sdk.v2.compose.compute`.
    name, description : str, optional
        Metadata for the new grid.
    tags : List[str], optional
        Tags for the new grid.
    modifications : list, optional
        Modification rules applied after the grid is composed.

    Returns
    -------
    Grid
        The new pending composed Grid.

    Raises
    ------
    TypeError
        If inputs or operations have the wrong shape.
    ValueError
        If inputs are empty, incomplete, duplicated, or from different
        domains; if aliases or band references are invalid; or if operation
        outputs are empty or duplicated.

    Examples
    --------
    >>> import fastfuels_sdk.v2 as ff
    >>> composed = ff.grids.create_grid_from_compose(
    ...     {"fuels": fuel_grid},
    ...     select=[ff.compose.select("fuel_depth", "fuels.fuel_depth")],
    ...     compute=[
    ...         ff.compose.compute(
    ...             "fuel_load.1hr",
    ...             "multiply",
    ...             ["fuels.fuel_load.1hr", 0.5],
    ...         )
    ...     ],
    ... )
    >>> composed.wait()
    """
    if not isinstance(inputs, Mapping):
        raise TypeError("inputs must be an alias-to-Grid mapping.")
    if not inputs:
        raise ValueError("inputs must contain at least one aliased Grid.")

    compose_inputs = []
    grids_by_alias = {}
    seen_grid_ids = set()
    domain_id = None
    for alias, grid in inputs.items():
        if (
            not isinstance(alias, str)
            or re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", alias) is None
        ):
            raise ValueError(
                f"Invalid compose alias {alias!r}; aliases must start with a "
                "letter and contain only letters, numbers, and underscores."
            )
        if not isinstance(grid, Grid):
            raise TypeError(f"Compose input {alias!r} must be a Grid object.")
        grid._require_completed("compose")
        if grid.id in seen_grid_ids:
            raise ValueError(f"Grid {grid.id!r} is assigned more than one alias.")
        if domain_id is None:
            domain_id = grid.domain_id
        elif grid.domain_id != domain_id:
            raise ValueError("All compose input grids must belong to the same domain.")
        seen_grid_ids.add(grid.id)
        grids_by_alias[alias] = grid
        compose_inputs.append(ComposeInput(grid_id=grid.id, alias=alias))

    select_operations = _compose_operations(select, ComposeSelect, "select")
    compute_operations = _compose_operations(compute, ComposeCompute, "compute")
    operations = [*select_operations, *compute_operations]
    if not operations:
        raise ValueError("At least one select or compute operation is required.")
    outputs = [operation.output for operation in operations]
    if any(not isinstance(output, str) or not output for output in outputs):
        raise ValueError("Every compose operation requires a nonempty output band.")
    duplicates = sorted({output for output in outputs if outputs.count(output) > 1})
    if duplicates:
        raise ValueError(f"Compose output bands must be unique: {duplicates}.")
    for operation in operations:
        _validate_compose_references(operation, grids_by_alias)

    request_body = CreateComposeRequest(
        inputs=compose_inputs,
        select=select_operations if select_operations else UNSET,
        compute=compute_operations if compute_operations else UNSET,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_compose_grid.sync_detailed(
        domain_id,
        client=ensure_client(),
        body=request_body,
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def _compose_operations(value, model_type, name: str) -> list:
    """Normalize and type-check one compose operation collection."""
    if value is None:
        return []
    if isinstance(value, model_type):
        raise TypeError(f"{name} must be a list of {model_type.__name__} objects.")
    try:
        operations = list(value)
    except TypeError:
        raise TypeError(
            f"{name} must be a list of {model_type.__name__} objects."
        ) from None
    if not all(isinstance(operation, model_type) for operation in operations):
        raise TypeError(f"{name} must contain only {model_type.__name__} objects.")
    return operations


def _validate_compose_references(operation, grids_by_alias) -> None:
    """Catch alias and band typos before dispatching a compose request."""
    if isinstance(operation, ComposeSelect):
        _validate_compose_reference(operation.from_, grids_by_alias)
    else:
        _validate_compose_operands(operation.operands, grids_by_alias)

    conditions = operation.conditions
    if conditions is not UNSET and conditions is not None:
        for condition in conditions:
            if isinstance(condition, ComposeAttributeCondition):
                _validate_compose_reference(condition.band, grids_by_alias)

    else_value = operation.else_
    if (
        else_value is UNSET
        or else_value is None
        or isinstance(else_value, ComposeLiteral)
    ):
        return
    if isinstance(else_value, InlineCompute):
        _validate_compose_operands(else_value.operands, grids_by_alias)
    elif isinstance(else_value, str) and "." in else_value:
        _validate_compose_reference(else_value, grids_by_alias)


def _validate_compose_operands(operands, grids_by_alias) -> None:
    for operand in operands:
        if isinstance(operand, str):
            _validate_compose_reference(operand, grids_by_alias)


def _validate_compose_reference(reference: str, grids_by_alias) -> None:
    alias, separator, band_key = reference.partition(".")
    if not separator or alias not in grids_by_alias or not band_key:
        raise ValueError(
            f"Unknown compose band reference {reference!r}; use "
            "'alias.band_key' with an alias from inputs."
        )
    available = [band.key for band in grids_by_alias[alias].bands]
    if band_key not in available:
        raise ValueError(
            f"Grid {grids_by_alias[alias].id} has no {band_key!r} band for "
            f"compose alias {alias!r}. Available bands: {available}."
        )


# ---------------------------------------------------------------------------
# Derive a grid from a grid you hold (source-specific transforms)
# ---------------------------------------------------------------------------
#
# Universal transforms that apply to *any* grid are methods on ``Grid``
# (``resample``, ``export``). Transforms that only make sense for a particular
# kind of grid are functions here instead — keeping them off ``Grid`` so they
# never appear on a grid that cannot perform them.


def create_fuel_grid_from_fccs_lookup(
    source_grid: "Grid",
    bands: list,
    source_band: str = "fccs",
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a fuel-parameter grid by looking up FCCS codes in a grid.

    Parameters
    ----------
    source_grid : Grid
        A completed grid carrying FCCS codes (produced by
        :func:`create_fuel_model_grid_from_landfire_fccs`).
    bands : list
        The FCCS lookup bands to produce (``FccsLookupBand`` members or
        string keys such as ``"fuel_load.duff"``, ``"duff_depth"``, and
        ``"fuel_load.live_shrub"``).
    source_band : str, optional
        The band in ``source_grid`` that holds FCCS codes (default ``"fccs"``).
    name, description : str, optional
        Metadata for the new grid.
    tags : List[str], optional
        Tags for the new grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The new pending fuel-parameter Grid.

    Raises
    ------
    ValueError
        If ``source_grid`` is not completed or has no ``source_band`` band.
    """
    source_grid._require_completed("look up fuel parameters from")
    band_keys = [band.key for band in source_grid.bands]
    if source_band not in band_keys:
        raise ValueError(
            f"Grid {source_grid.id} has no {source_band!r} band to look up; pass "
            "an FCCS fuel model grid (see "
            f"create_fuel_model_grid_from_landfire_fccs). Available bands: "
            f"{band_keys}."
        )
    request_body = CreateFccsLookupRequest(
        source_grid_id=source_grid.id,
        bands=_enum_list(bands, FccsLookupBand),
        source_band=source_band,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_fccs_lookup.sync_detailed(
        source_grid.domain_id,
        client=ensure_client(),
        body=request_body,
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_fuel_grid_from_fbfm13_lookup(
    source_grid: "Grid",
    bands: list,
    source_band: str = "fbfm13",
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a fuel-parameter grid by looking up FBFM13 codes in a grid.

    Parameters
    ----------
    source_grid : Grid
        A completed grid carrying FBFM13 codes (produced by
        :func:`create_fuel_model_grid_from_landfire_fbfm13`).
    bands : list
        The FBFM13 lookup bands to produce (``Fbfm13LookupBand`` members or
        string keys such as ``"fuel_load.1hr"`` and ``"fuel_depth"``).
    source_band : str, optional
        The band in ``source_grid`` that holds FBFM13 codes (default
        ``"fbfm13"``).
    name, description : str, optional
        Metadata for the new grid.
    tags : List[str], optional
        Tags for the new grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The new pending fuel-parameter Grid.

    Raises
    ------
    ValueError
        If ``source_grid`` is not completed or has no ``source_band`` band.
    """
    source_grid._require_completed("look up fuel parameters from")
    band_keys = [band.key for band in source_grid.bands]
    if source_band not in band_keys:
        raise ValueError(
            f"Grid {source_grid.id} has no {source_band!r} band to look up; pass "
            "an FBFM13 fuel model grid (see "
            f"create_fuel_model_grid_from_landfire_fbfm13). Available bands: "
            f"{band_keys}."
        )
    request_body = CreateFbfm13LookupRequest(
        source_grid_id=source_grid.id,
        bands=_enum_list(bands, Fbfm13LookupBand),
        source_band=source_band,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_fbfm13_lookup.sync_detailed(
        source_grid.domain_id,
        client=ensure_client(),
        body=request_body,
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_fuel_grid_from_fbfm40_lookup(
    source_grid: "Grid",
    bands: list,
    source_band: str = "fbfm",
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
) -> Grid:
    """Create a fuel-parameter grid by looking up FBFM40 codes in a grid.

    The `fbfm` band of an FBFM40 fuel model grid holds categorical fuel-model
    codes, not the quantities a fire model consumes. This translates those
    codes into fuel parameters (loadings by size class, fuel-bed depth,
    surface-area-to-volume ratios), returning a new grid whose bands are the
    requested parameters.

    Parameters
    ----------
    source_grid : Grid
        A completed grid carrying FBFM40 codes (produced by
        :func:`create_fuel_model_grid_from_landfire_fbfm40`).
    bands : list
        The FBFM40 lookup bands to produce (``Fbfm40LookupBand`` members or
        their string keys, e.g. "fuel_load.1hr", "fuel_depth").
    source_band : str, optional
        The band in ``source_grid`` that holds FBFM40 codes (default "fbfm").
    name, description : str, optional
        Metadata for the new grid.
    tags : List[str], optional
        Tags for the new grid.
    modifications : list, optional
        Modification rules applied after the grid is built.

    Returns
    -------
    Grid
        The new (pending) fuel-parameter Grid.

    Raises
    ------
    ValueError
        If ``source_grid`` is not completed, or carries no ``source_band`` band
        to look up (i.e. it is not an FBFM40 fuel model grid).
    """
    source_grid._require_completed("look up fuel parameters from")
    band_keys = [b.key for b in source_grid.bands]
    if source_band not in band_keys:
        raise ValueError(
            f"Grid {source_grid.id} has no {source_band!r} band to look up; pass "
            "an FBFM40 fuel model grid (see "
            f"create_fuel_model_grid_from_landfire_fbfm40). Available bands: "
            f"{band_keys}."
        )
    request_body = CreateFbfm40LookupRequest(
        source_grid_id=source_grid.id,
        bands=_enum_list(bands, Fbfm40LookupBand),
        source_band=source_band,
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
    )
    response = create_fbfm40_lookup.sync_detailed(
        source_grid.domain_id, client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def create_surface_fuel_grid_from_duet(
    source_grid: "Grid",
    years_since_burn: int,
    wind_direction: int = 270,
    wind_variability: int = 30,
    bands: Optional[list] = None,
    calibration: Optional[DuetCalibration] = None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Grid:
    """Create a 2D DUET surface-fuel grid from a 3D tree grid.

    Parameters
    ----------
    source_grid : Grid
        A completed 3D tree grid carrying ``bulk_density.foliage.live``,
        ``spcd``, and ``fuel_moisture.live`` bands.
    years_since_burn : int
        Years of litter accumulation to simulate, from 1 through 100.
    wind_direction : int, optional
        Prevailing wind direction in whole degrees clockwise from north
        (0-359, default 270).
    wind_variability : int, optional
        Angular spread of wind direction in whole degrees (0-180, default 30).
    bands : list, optional
        DUET output bands (``DuetBand`` members or string keys). Defaults to
        ``fuel_load.grass`` and ``fuel_load.litter``.
    calibration : DuetCalibration, optional
        Per-parameter and per-fuel-type targets from
        :func:`fastfuels_sdk.v2.calibrations.duet_calibration`. If omitted,
        the grid stores raw DUET values.
    name, description : str, optional
        Metadata for the new grid.
    tags : List[str], optional
        Tags for the new grid.

    Returns
    -------
    Grid
        The new pending DUET surface-fuel Grid.

    Raises
    ------
    TypeError
        If a DUET time or wind parameter is not a whole number.
    ValueError
        If a parameter is out of range, the source is not completed, or the
        source lacks a required tree band.
    """
    source_grid._require_completed("create a DUET surface fuel grid from")
    required_bands = {
        "bulk_density.foliage.live",
        "spcd",
        "fuel_moisture.live",
    }
    band_keys = {band.key for band in source_grid.bands}
    missing = sorted(required_bands - band_keys)
    if missing:
        raise ValueError(
            f"Grid {source_grid.id} lacks DUET source bands: {missing}. "
            f"Available bands: {sorted(band_keys)}."
        )

    years_since_burn = _duet_integer(
        "years_since_burn", years_since_burn, minimum=1, maximum=100
    )
    wind_direction = _duet_integer(
        "wind_direction", wind_direction, minimum=0, maximum=359
    )
    wind_variability = _duet_integer(
        "wind_variability", wind_variability, minimum=0, maximum=180
    )
    requested_bands = _enum_list(bands, DuetBand)
    if requested_bands is not UNSET:
        if not requested_bands:
            raise ValueError("bands must contain at least one DUET band.")
        if len(set(requested_bands)) != len(requested_bands):
            raise ValueError("bands contains duplicate DUET bands.")

    request_body = CreateDuetRequest(
        source_grid_id=source_grid.id,
        years_since_burn=years_since_burn,
        wind_direction=wind_direction,
        wind_variability=wind_variability,
        bands=requested_bands,
        calibration=_opt(calibration),
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_duet_grid.sync_detailed(
        source_grid.domain_id,
        client=ensure_client(),
        body=request_body,
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def _duet_integer(name: str, value, *, minimum: int, maximum: int) -> int:
    """Validate a bounded whole-number DUET parameter."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be a whole number.")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}.")
    return value


def create_dead_fuel_moisture_grid_from_fosberg(
    source_topography_grid,
    source_irradiance_grid,
    dry_bulb_temp: float,
    relative_humidity: float,
    time: int,
    month,
    elevation=None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Grid:
    """Create a Fosberg 1-hour dead fuel moisture grid from two grids.

    Derives a grid with a single ``fuel_moisture.dead.1hr`` band (percent)
    using the Fosberg & Deeming 1-hour dead fuel moisture model. The output
    inherits the topography grid's domain, CRS, transform, and georeference.

    Parameters
    ----------
    source_topography_grid : Grid or str
        A completed 2D topography grid (or its id) carrying ``slope`` and
        ``aspect`` bands, both in degrees.
    source_irradiance_grid : Grid or str
        A completed Leaflux irradiance grid (or its id) carrying an
        ``irradiance.surface.relative`` band; per-cell shading is derived
        from it. Must belong to the same domain as the topography grid.
    dry_bulb_temp : float
        Dry-bulb air temperature in degrees Fahrenheit. Must be >= 10.
    relative_humidity : float
        Relative humidity as a percent, from 0 through 100.
    time : int
        Local time of day in 24-hour HHMM form (e.g. 1200 for noon), from
        0800 through 1959.
    month : FuelMoistureMonth or str
        Month of the burn scenario, selecting the Fosberg correction table
        (``FuelMoistureMonth`` member or a month name such as ``"July"``).
    elevation : RelativeElevation or str, optional
        Site elevation relative to the reference weather station
        (``RelativeElevation`` member or one of ``"below"``, ``"near"``,
        ``"above"``): ``below`` = 1000-2000 ft below the station, ``near`` =
        within 1000 ft (no correction), ``above`` = 1000-2000 ft above. This
        is a Fosberg correction category, not the topography elevation band.
    name, description : str, optional
        Metadata for the new grid.
    tags : List[str], optional
        Tags for the new grid.

    Returns
    -------
    Grid
        The new pending Fosberg dead fuel moisture Grid.

    Raises
    ------
    TypeError
        If ``dry_bulb_temp``, ``relative_humidity``, or ``time`` is not a
        number, or ``time`` is not a whole number.
    ValueError
        If a parameter is out of range, a source grid passed as a Grid is not
        completed or lacks a required band, or the domain cannot be resolved
        because both source grids were passed as bare ids.
    """
    # Local band/completion checks only apply when a Grid object is supplied;
    # bare ids are validated server-side. The domain id is taken from whichever
    # source grid is a Grid object.
    topo_id, topo_domain = _resolve_fosberg_source_grid(
        source_topography_grid,
        required_bands={"slope", "aspect"},
        kind="topography",
        action="derive a Fosberg dead fuel moisture grid from",
    )
    irradiance_id, irradiance_domain = _resolve_fosberg_source_grid(
        source_irradiance_grid,
        required_bands={"irradiance.surface.relative"},
        kind="irradiance",
        action="derive a Fosberg dead fuel moisture grid from",
    )
    domain_id = topo_domain if topo_domain is not None else irradiance_domain
    if domain_id is None:
        raise ValueError(
            "Cannot resolve the domain from grid ids alone. Pass at least one "
            "source grid as a Grid object, or load them with "
            "get_grid(domain, id) first."
        )

    dry_bulb_temp = _fosberg_number("dry_bulb_temp", dry_bulb_temp, minimum=10)
    relative_humidity = _fosberg_number(
        "relative_humidity", relative_humidity, minimum=0, maximum=100
    )
    time = _fosberg_time(time)
    month = month if isinstance(month, FuelMoistureMonth) else FuelMoistureMonth(month)
    if elevation is None:
        elevation = UNSET
    elif not isinstance(elevation, RelativeElevation):
        elevation = RelativeElevation(elevation)

    request_body = CreateFosbergFuelMoistureRequest(
        source_topography_grid_id=topo_id,
        source_irradiance_grid_id=irradiance_id,
        dry_bulb_temp=dry_bulb_temp,
        relative_humidity=relative_humidity,
        time=time,
        month=month,
        elevation=elevation,
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_fosberg_fuel_moisture_grid.sync_detailed(
        domain_id,
        client=ensure_client(),
        body=request_body,
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


def _resolve_fosberg_source_grid(grid, *, required_bands, kind: str, action: str):
    """Resolve a Fosberg source grid to ``(grid_id, domain_id_or_None)``.

    When ``grid`` is a Grid, require it be completed and carry every band in
    ``required_bands`` and return its domain id. When it is a bare id string,
    skip local validation (the server validates) and return ``None`` for the
    domain id.
    """
    if not isinstance(grid, Grid):
        return grid, None
    grid._require_completed(action)
    band_keys = {band.key for band in grid.bands}
    missing = sorted(set(required_bands) - band_keys)
    if missing:
        raise ValueError(
            f"{kind} grid {grid.id} lacks required bands: {missing}. "
            f"Available bands: {sorted(band_keys)}."
        )
    return grid.id, grid.domain_id


def _fosberg_number(name: str, value, *, minimum=None, maximum=None):
    """Validate a bounded Fosberg weather parameter."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number.")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be >= {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be <= {maximum}.")
    return value


def _fosberg_time(value) -> int:
    """Validate a Fosberg local time of day in 24-hour HHMM form."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("time must be a whole number in HHMM form.")
    minute = value % 100
    if not 0 <= minute <= 59:
        raise ValueError("time must be a valid HHMM clock time (minutes 00-59).")
    if not 800 <= value <= 1959:
        raise ValueError("time must be between 0800 and 1959 (HHMM).")
    return value


def create_irradiance_grid_from_leaflux(
    source_grid,
    date_time: datetime.datetime,
    source_terrain_grid=None,
    bands: Optional[list] = None,
    extinction_coefficient: float = 0.5,
    domain=None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Grid:
    """Create a 3D LeafLux solar-irradiance grid from a source fuel grid.

    Computes solar irradiance through the canopy at a single instant, attenuating
    light through the source grid's leaf area density with a Beer-Lambert
    extinction coefficient. An optional 2D terrain grid supplies surface
    elevation for the surface-irradiance band.

    Parameters
    ----------
    source_grid : Grid or str
        A completed 3D grid (or its id) carrying a ``leaf_area_density`` band.
    date_time : datetime.datetime
        The UTC instant at which to compute irradiance.
    source_terrain_grid : Grid or str, optional
        A 2D terrain grid (or its id) in the same domain, used for the
        surface-irradiance band.
    bands : list, optional
        Irradiance bands to produce (``LeafluxBand`` members or their string
        keys, e.g. "irradiance.surface.relative",
        "irradiance.canopy.relative"). Defaults to
        ``irradiance.surface.relative``.
    extinction_coefficient : float, optional
        Beer-Lambert extinction coefficient applied to the leaf area density
        (default 0.5).
    domain : Domain or str, optional
        The domain (or its id) to create the grid in. Required only when
        ``source_grid`` is given as an id; inferred from the grid otherwise.
    name, description : str, optional
        Metadata for the new grid.
    tags : List[str], optional
        Tags for the new grid.

    Returns
    -------
    Grid
        The new pending irradiance Grid.

    Raises
    ------
    ValueError
        If ``source_grid`` is a Grid that is not completed or lacks a
        ``leaf_area_density`` band, or if ``domain`` is required but not given.
    """
    if isinstance(source_grid, Grid):
        source_grid._require_completed("create a LeafLux irradiance grid from")
        band_keys = [band.key for band in source_grid.bands]
        if "leaf_area_density" not in band_keys:
            raise ValueError(
                f"Grid {source_grid.id} has no 'leaf_area_density' band; pass a "
                f"3D grid with leaf area density. Available bands: {band_keys}."
            )

    domain_id = (
        _domain_id(domain)
        if domain is not None
        else getattr(source_grid, "domain_id", None)
    )
    if domain_id is None:
        raise ValueError(
            "Pass source_grid as a Grid, or supply domain= when source_grid is "
            "an id."
        )

    request_body = CreateLeafluxIrradianceRequest(
        source_lad_grid_id=_grid_id(source_grid),
        date_time=date_time,
        source_terrain_grid_id=(
            _grid_id(source_terrain_grid) if source_terrain_grid is not None else UNSET
        ),
        bands=_enum_list(bands, LeafluxBand),
        extinction_coefficient=extinction_coefficient,
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_leaflux_irradiance_grid.sync_detailed(
        domain_id, client=ensure_client(), body=request_body
    )
    return Grid._from_model(expect(response, HTTPStatus.CREATED))


# ---------------------------------------------------------------------------
# Listing, fetching, and utilities
# ---------------------------------------------------------------------------


def list_grids(
    domain=None,
    page: int = 0,
    size: int = 100,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    source: Optional[str] = None,
    product: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[Grid]:
    """List grids in a domain, or across all domains (single page).

    Parameters
    ----------
    domain : Domain or str, optional
        The domain (or its id) to list grids in. If omitted, grids from all the
        user's domains are listed.
    page : int, optional
        The page number to retrieve, zero-indexed (default 0).
    size : int, optional
        The number of grids per page (default 100).
    sort_by : str, optional
        Field to sort by: "name", "created_on", or "modified_on".
    sort_order : str, optional
        Sort direction: "ascending" or "descending".
    source : str, optional
        Only return grids from this source (e.g. "landfire", "3dep").
    product : str, optional
        Only return grids from this source product (e.g. "fbfm40",
        "topography"). Requires ``source``.
    tag : str, optional
        Only return grids carrying this tag.

    Returns
    -------
    List[Grid]
        The requested page of Grid objects.
    """
    kwargs = dict(
        client=ensure_client(),
        page=page,
        size=size,
        sort_by=GridSortField(sort_by) if sort_by else UNSET,
        sort_order=SortOrder(sort_order) if sort_order else UNSET,
        source=_opt(source),
        product=_opt(product),
        tag=_opt(tag),
    )
    if domain is None:
        response = list_grids_cross_domain.sync_detailed(**kwargs)
    else:
        response = list_grids_endpoint.sync_detailed(_domain_id(domain), **kwargs)
    list_response: ListGridsResponse = expect(response)
    return [Grid._from_model(g) for g in list_response.grids]


def get_grid(domain, grid_id: str) -> Grid:
    """Retrieve a single grid by its ID.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) the grid belongs to.
    grid_id : str
        The unique identifier of the grid.

    Returns
    -------
    Grid
        The requested Grid object.

    Raises
    ------
    NotFoundException
        If no grid exists with the given IDs, or the user does not have access.
    """
    return Grid.from_id(_domain_id(domain), grid_id)


def check_3dep_coverage(
    domain, resolution_m: Optional[int] = None
) -> TopographyThreeDepCoverageResponse:
    """Check USGS 3DEP tile coverage for a domain before creating a grid.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to check.
    resolution_m : int, optional
        Resolution to check: 1, 10, or 30 meters. Defaults to the API's default.

    Returns
    -------
    TopographyThreeDepCoverageResponse
        Tile availability, count, URLs, and (for 1 m) acquisition dates.
    """
    response = check_3dep_coverage_endpoint.sync_detailed(
        _domain_id(domain),
        client=ensure_client(),
        resolution=ThreeDepResolution(resolution_m) if resolution_m else UNSET,
    )
    return expect(response)


def check_landfire_fbfm40_coverage(domain) -> LandfireCoverageResponse:
    """Check LANDFIRE FBFM40 release coverage for a domain.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to check.

    Returns
    -------
    LandfireCoverageResponse
        Per-release coverage, the latest fully-covering release, and
        ready-made create-request links.
    """
    response = check_landfire_fbfm40_coverage_endpoint.sync_detailed(
        _domain_id(domain),
        client=ensure_client(),
    )
    return expect(response)


def check_landfire_fbfm13_coverage(domain) -> LandfireCoverageResponse:
    """Check LANDFIRE FBFM13 release coverage for a domain.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to check.

    Returns
    -------
    LandfireCoverageResponse
        Per-release coverage, the latest fully-covering release, and
        ready-made create-request links.
    """
    response = check_landfire_fbfm13_coverage_endpoint.sync_detailed(
        _domain_id(domain),
        client=ensure_client(),
    )
    return expect(response)


def check_landfire_fccs_coverage(domain) -> LandfireCoverageResponse:
    """Check LANDFIRE FCCS release coverage for a domain.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to check.

    Returns
    -------
    LandfireCoverageResponse
        Per-release coverage, the latest fully-covering release, and
        ready-made create-request links.
    """
    response = check_landfire_fccs_coverage_endpoint.sync_detailed(
        _domain_id(domain),
        client=ensure_client(),
    )
    return expect(response)
