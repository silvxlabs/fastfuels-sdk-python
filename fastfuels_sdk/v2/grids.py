"""
fastfuels_sdk/v2/grids.py
"""

# Core imports
import json
from http import HTTPStatus
from typing import Dict, List, Optional, Union

# Internal imports
from fastfuels_sdk.v2._jobs import wait as _wait
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect
from fastfuels_sdk.v2.client_library.api.grids import (
    check_3dep_coverage as check_3dep_coverage_endpoint,
    create_3dep_topography,
    create_fbfm40_lookup,
    create_geotiff_upload,
    create_grid_export,
    create_landfire_canopy,
    create_landfire_fbfm40,
    create_landfire_fccs,
    create_landfire_topography,
    create_meta_chm,
    create_naip_chm,
    create_netcdf_upload,
    create_resample,
    create_treemap,
    create_uniform_grid as create_uniform_grid_endpoint,
    delete_grid,
    get_grid as get_grid_endpoint,
    list_grids as list_grids_endpoint,
    list_grids_cross_domain,
    update_grid,
)
from fastfuels_sdk.v2.client_library.models import (
    Grid as GridModel,
    CreateFbfm40LookupRequest,
    CreateGeoTIFFUploadRequest,
    CreateLandfireCanopyRequest,
    CreateLandfireFbfm40Request,
    CreateLandfireFccsRequest,
    CreateLandfireTopographyRequest,
    CreateMetaChmRequest,
    CreateNaipChmRequest,
    CreateNetcdfUploadRequest,
    CreateResampleRequest,
    CreateThreeDepTopographyRequest,
    CreateTreeMapRequest,
    CreateUniformRequest,
    ExportGridRequest,
    Fbfm40LookupBand,
    GridAlignmentDomainTarget,
    GridAlignmentGridTarget,
    GridAlignmentNativeTarget,
    GridExportFormat,
    GridSortField,
    JobStatus,
    LandfireCanopyFuelBand,
    LandfireCanopyVersion,
    LandfireFbfm40Version,
    LandfireFccsVersion,
    LandfireTopographyVersion,
    ListGridsResponse,
    MetaCHMVersion,
    NonBurnableFuelModel,
    ResamplingMethod,
    SortOrder,
    ThreeDepResolution,
    TopographyBand,
    TreeMapBand,
    TreeMapVersion,
    UniformBand,
    UniformBandInput,
    UpdateGridRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET

# External imports
import attrs
import requests

__all__ = [
    "Grid",
    "create_topography_grid_from_3dep",
    "create_topography_grid_from_landfire",
    "create_canopy_fuel_grid_from_landfire",
    "create_canopy_height_grid_from_meta",
    "create_canopy_height_grid_from_naip_chm",
    "create_fuel_model_grid_from_landfire_fbfm40",
    "create_fuel_model_grid_from_landfire_fccs",
    "create_grid_from_geotiff",
    "create_grid_from_netcdf",
    "create_uniform_grid",
    "list_grids",
    "get_grid",
    "check_3dep_coverage",
]


def _domain_id(domain) -> str:
    """Resolve a Domain object or a domain-id string to the id string."""
    return getattr(domain, "id", domain)


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


def _put_upload(spec, path: str) -> None:
    """Upload a local file to a signed upload URL with HTTP PUT."""
    with open(path, "rb") as file_obj:
        response = requests.put(
            spec.url, data=file_obj, headers={"Content-Type": spec.content_type}
        )
    response.raise_for_status()


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

    def lookup_fuel_model_values(
        self,
        bands: list,
        source_band: str = "fbfm",
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        modifications: Optional[list] = None,
    ) -> "Grid":
        """Create a fuel-parameter grid by looking up FBFM40 codes in this grid.

        Parameters
        ----------
        bands : list
            The FBFM40 lookup bands to produce (``Fbfm40LookupBand`` members or
            their string keys, e.g. "fuel_load_1hr").
        source_band : str, optional
            The band in this grid that holds FBFM40 codes (default "fbfm").
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
        """
        self._require_completed("look up fuel parameters from")
        request_body = CreateFbfm40LookupRequest(
            source_grid_id=self.id,
            bands=_enum_list(bands, Fbfm40LookupBand),
            source_band=source_band,
            name=name,
            description=description,
            tags=_opt(tags),
            modifications=_opt(modifications),
        )
        response = create_fbfm40_lookup.sync_detailed(
            self.domain_id, client=ensure_client(), body=request_body
        )
        return Grid._from_model(expect(response, HTTPStatus.CREATED))

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
            The generated Export resource (job status "pending"). Poll it until
            completed to obtain the signed download URL.
        """
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
        return expect(response, HTTPStatus.CREATED)

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


def create_fuel_model_grid_from_landfire_fbfm40(
    domain,
    version: Optional[str] = None,
    remove_non_burnable: Optional[list] = None,
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
        current version.
    remove_non_burnable : list, optional
        Non-burnable fuel models to drop (``NonBurnableFuelModel`` members or
        their string keys, e.g. "NB1", "NB2").
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
        remove_non_burnable=_enum_list(remove_non_burnable, NonBurnableFuelModel),
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
    # FCCS is alignment-free: CreateLandfireFccsRequest has no `alignment` or
    # `extent_buffer_cells` field, unlike the other LANDFIRE creators, so there
    # are no output_resolution_m/align_to/align/resampling kwargs here.
    # See fastfuels_sdk/v2/v2_api_design.md.
    request_body = CreateLandfireFccsRequest(
        version=LandfireFccsVersion(version) if version is not None else UNSET,
        remove_bare_ground=remove_bare_ground,
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
    _put_upload(created.upload, path)
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
    _put_upload(created.upload, path)
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


def check_3dep_coverage(domain, resolution_m: Optional[int] = None):
    """Check USGS 3DEP tile coverage for a domain before creating a grid.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to check.
    resolution_m : int, optional
        Resolution to check: 1, 10, or 30 meters. Defaults to the API's default.

    Returns
    -------
    ThreeDepCoverageResponse
        Tile availability, count, URLs, and (for 1 m) acquisition dates.
    """
    response = check_3dep_coverage_endpoint.sync_detailed(
        _domain_id(domain),
        client=ensure_client(),
        resolution=ThreeDepResolution(resolution_m) if resolution_m else UNSET,
    )
    return expect(response)
