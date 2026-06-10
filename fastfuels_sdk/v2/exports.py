"""
fastfuels_sdk/v2/exports.py
"""

# Core imports
import json
from http import HTTPStatus
from pathlib import Path
from typing import List, Optional, Tuple, Union
from urllib.parse import urlparse

# Internal imports
from fastfuels_sdk.v2._jobs import wait as _wait
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect
from fastfuels_sdk.v2.client_library.api.exports import (
    delete_export,
    get_export as get_export_endpoint,
    list_exports as list_exports_endpoint,
    update_export,
)
from fastfuels_sdk.v2.client_library.api.grids import (
    create_quicfire_export as create_quicfire_export_endpoint,
)
from fastfuels_sdk.v2.client_library.models import (
    Export as ExportModel,
    ExportSortField,
    FieldSource,
    JobStatus,
    ListExportsResponse,
    QuicfireExportRequest,
    QuicfireExportRequestMoistMerge,
    QUICFireExportAlignmentDomainTarget,
    QUICFireExportAlignmentGridTarget,
    SortOrder,
    UpdateExportRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET

# External imports
import attrs
import requests

__all__ = [
    "Export",
    "create_quicfire_export",
    "list_exports",
    "get_export",
]

_DOWNLOAD_CHUNK_BYTES = 1024 * 1024


def _domain_id(domain) -> str:
    """Resolve a Domain object or a domain-id string to the id string."""
    return getattr(domain, "id", domain)


def _opt(value):
    """Map ``None`` to the generated UNSET sentinel, else pass through."""
    return value if value is not None else UNSET


def _field_source(value, role: str) -> FieldSource:
    """Build a FieldSource from a ``(grid, band)`` tuple or pass one through."""
    if isinstance(value, FieldSource):
        return value
    if isinstance(value, (tuple, list)) and len(value) == 2:
        grid, band = value
        return FieldSource(grid_id=_domain_id(grid), band=band)
    raise ValueError(
        f"{role} must be a (grid, band) tuple or a FieldSource, got {value!r}"
    )


class Export(ExportModel):
    """Export resource for the FastFuels v2 API.

    An export packages a resource's data — a grid, an inventory, or a
    multi-grid QUIC-Fire bundle — into a downloadable file. Exports are
    asynchronous job resources: creation returns a *pending* record, and
    the signed download URL is populated when the job completes. Call
    :meth:`wait` and then :meth:`to_file` to download.

    Attributes
    ----------
    id : str
        Unique identifier for the export.
    domain_id : str
        Identifier of the domain the exported resource belongs to.
    status : JobStatus
        Job status: "pending", "running", "completed", or "failed".
    source : ExportSource
        What was exported and in which format.
    name : str
        Human-readable name for the export.
    description : str
        Detailed description of the export.
    progress : JobProgress, optional
        Progress info while the job is running.
    signed_url : str, optional
        Download URL; populated when the job completes.
    expires_on : datetime, optional
        When the signed URL stops working.
    error : JobError, optional
        Error details if the job failed.
    tags : List[str], optional
        User-defined tags for organization.
    created_on : datetime
        When the export was created.
    modified_on : datetime
        When the export was last modified.

    Examples
    --------
    Export a grid and download the result:
    >>> export = grid.export(format="geotiff")
    >>> export.wait().to_file("elevation.tif")

    Get an export by ID:
    >>> export = ff.get_export("abc123")

    See Also
    --------
    create_quicfire_export : Bundle fuel grids into a QUIC-Fire archive.
    list_exports : List your exports.
    """

    @classmethod
    def _from_model(cls, model: ExportModel) -> "Export":
        """Build an Export from a generated Export model instance.

        Round-trips through the generated to_dict/from_dict — from_dict
        constructs ``cls``, i.e. this subclass.
        """
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: ExportModel) -> "Export":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(ExportModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    @classmethod
    def from_id(cls, export_id: str) -> "Export":
        """Retrieve an existing Export resource by its ID.

        Exports are addressed by their ID alone (no domain in the path).

        Parameters
        ----------
        export_id : str
            The unique identifier of the export to retrieve.

        Returns
        -------
        Export
            The requested Export object.

        Raises
        ------
        NotFoundException
            If no export exists with the given ID, or the user does not
            have access to it.
        """
        response = get_export_endpoint.sync_detailed(export_id, client=ensure_client())
        return cls._from_model(expect(response))

    def refresh(self) -> "Export":
        """Update this Export in place with the latest data from the API.

        Returns
        -------
        Export
            ``self``, updated with the latest data (so calls chain).

        Raises
        ------
        NotFoundException
            If the export no longer exists.
        """
        response = get_export_endpoint.sync_detailed(self.id, client=ensure_client())
        return self._copy_fields_from(expect(response))

    def wait(self, timeout: Optional[float] = None, verbose: bool = False) -> "Export":
        """Poll the export job until it reaches a terminal status.

        Parameters
        ----------
        timeout : float, optional
            Maximum seconds to wait. ``None`` (default) waits indefinitely; the
            job runs server-side regardless, so a bounded wait is resumable.
        verbose : bool, optional
            If True, print the job status at each poll.

        Returns
        -------
        Export
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
    ) -> "Export":
        """Update the export's mutable metadata (name, description, tags) in place.

        Only provided fields are sent. If no fields are provided, no API call
        is made.

        Parameters
        ----------
        name : str, optional
            New name for the export.
        description : str, optional
            New description for the export.
        tags : List[str], optional
            New tags for the export (replaces existing tags).

        Returns
        -------
        Export
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the export no longer exists.
        """
        if name is None and description is None and tags is None:
            return self
        request_body = UpdateExportRequestBody(
            name=_opt(name), description=_opt(description), tags=_opt(tags)
        )
        response = update_export.sync_detailed(
            self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def delete(self) -> None:
        """Delete this export and its packaged file.

        Raises
        ------
        NotFoundException
            If the export no longer exists.
        """
        response = delete_export.sync_detailed(self.id, client=ensure_client())
        expect(response, HTTPStatus.NO_CONTENT)

    def to_file(self, path: Union[str, Path]) -> Path:
        """Download the export's packaged file.

        Streams the signed URL to disk. The export must be completed —
        call :meth:`wait` first.

        Parameters
        ----------
        path : str or Path
            Destination file path. If ``path`` is an existing directory,
            the file is saved inside it under the export's default
            filename.

        Returns
        -------
        Path
            The path of the written file.

        Raises
        ------
        ValueError
            If the export is not completed or carries no download URL.

        Examples
        --------
        >>> export = grid.export(format="geotiff")
        >>> export.wait().to_file("elevation.tif")
        """
        if self.status != JobStatus.COMPLETED:
            raise ValueError(
                f"Cannot download an export with status '{self.status}'. "
                "Call .wait() until it completes first."
            )
        if not self.signed_url:
            raise ValueError(
                "Export carries no download URL. The signed URL may have "
                "expired — re-create the export."
            )
        destination = Path(path)
        if destination.is_dir():
            filename = Path(urlparse(self.signed_url).path).name or f"{self.id}.zip"
            destination = destination / filename
        with requests.get(self.signed_url, stream=True) as response:
            response.raise_for_status()
            with open(destination, "wb") as file_obj:
                for chunk in response.iter_content(chunk_size=_DOWNLOAD_CHUNK_BYTES):
                    file_obj.write(chunk)
        return destination

    def to_json(self) -> str:
        """Serialize the complete Export object to a JSON string.

        Returns
        -------
        str
            The Export as a pretty-printed JSON string.
        """
        return json.dumps(self.to_dict(), default=str, indent=2)


# ---------------------------------------------------------------------------
# Create exports assembled from many resources (module-level functions)
# ---------------------------------------------------------------------------


def create_quicfire_export(
    domain,
    canopy_bulk_density: Tuple,
    canopy_moisture: Tuple,
    surface_fuel_load: Tuple,
    surface_fuel_depth: Tuple,
    surface_moisture: Tuple,
    topography: Optional[Tuple] = None,
    canopy_savr: Optional[Tuple] = None,
    surface_savr: Optional[Tuple] = None,
    horizontal_resolution_m: Optional[float] = None,
    vertical_resolution_m: Optional[float] = None,
    align_to=None,
    moist_merge: Optional[str] = None,
    expiration_days: int = 7,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Export:
    """Bundle fuel and topography grids into a QUIC-Fire export.

    Packages the grids into a QUIC-Fire-loadable zip archive containing
    ``treesrhof.dat``, ``treesmoist.dat``, ``treesfueldepth.dat``,
    ``metadata.json``, and ``domain.geojson`` — plus ``topo.dat`` when
    ``topography`` is given, and ``treesss.dat`` when both SAVR roles are
    given.

    Each grid role is a ``(grid, band)`` pair naming the grid (or its id)
    and the band to read. Every role grid must be lattice-aligned with the
    fire grid and cover its full extent; the exporter crops oversized
    grids but never resamples.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) the grids belong to.
    canopy_bulk_density : tuple
        ``(grid, band)`` for 3D canopy bulk density (kg/m³).
    canopy_moisture : tuple
        ``(grid, band)`` for 3D canopy fuel moisture.
    surface_fuel_load : tuple
        ``(grid, band)`` for 2D surface fuel load (kg/m²).
    surface_fuel_depth : tuple
        ``(grid, band)`` for 2D surface fuel depth (m).
    surface_moisture : tuple
        ``(grid, band)`` for 2D surface fuel moisture.
    topography : tuple, optional
        ``(grid, band)`` for elevation; produces ``topo.dat``.
    canopy_savr, surface_savr : tuple, optional
        ``(grid, band)`` for surface-area-to-volume ratio. Give both or
        neither; together they produce ``treesss.dat``.
    horizontal_resolution_m : float, optional
        Fire-grid cell size (x and y) in meters when anchoring to the
        domain bounding box (API default 2.0). Mutually exclusive with
        ``align_to``.
    vertical_resolution_m : float, optional
        Fire-grid vertical cell size in meters (API default 1.0).
        Mutually exclusive with ``align_to``.
    align_to : Grid or str, optional
        Define the fire grid by an existing grid's lattice instead.
    moist_merge : str, optional
        How surface and canopy moisture merge in shared cells: "max"
        (API default) or "weighted_avg".
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
        the archive.

    Raises
    ------
    ValueError
        If ``align_to`` is combined with a resolution argument.

    Examples
    --------
    >>> export = ff.exports.create_quicfire_export(
    ...     domain,
    ...     canopy_bulk_density=(voxels, "bulk_density.foliage.live"),
    ...     canopy_moisture=(canopy_moist, "fuel_moisture"),
    ...     surface_fuel_load=(surface, "fuel_load.1hr"),
    ...     surface_fuel_depth=(surface, "fuel_depth"),
    ...     surface_moisture=(surface_moist, "fuel_moisture"),
    ... )
    >>> export.wait().to_file("quicfire.zip")
    """
    if align_to is not None:
        if horizontal_resolution_m is not None or vertical_resolution_m is not None:
            raise ValueError(
                "Specify either align_to or the resolution arguments, not both."
            )
        alignment = QUICFireExportAlignmentGridTarget(
            target="grid", grid_id=_domain_id(align_to)
        )
    elif horizontal_resolution_m is not None or vertical_resolution_m is not None:
        alignment = QUICFireExportAlignmentDomainTarget(
            dx=_opt(horizontal_resolution_m),
            dy=_opt(horizontal_resolution_m),
            dz=_opt(vertical_resolution_m),
        )
    else:
        alignment = UNSET

    request_body = QuicfireExportRequest(
        canopy_bulk_density=_field_source(canopy_bulk_density, "canopy_bulk_density"),
        canopy_moisture=_field_source(canopy_moisture, "canopy_moisture"),
        surface_fuel_load=_field_source(surface_fuel_load, "surface_fuel_load"),
        surface_fuel_depth=_field_source(surface_fuel_depth, "surface_fuel_depth"),
        surface_moisture=_field_source(surface_moisture, "surface_moisture"),
        topography=(
            _field_source(topography, "topography") if topography is not None else UNSET
        ),
        canopy_savr=(
            _field_source(canopy_savr, "canopy_savr")
            if canopy_savr is not None
            else UNSET
        ),
        surface_savr=(
            _field_source(surface_savr, "surface_savr")
            if surface_savr is not None
            else UNSET
        ),
        alignment=alignment,
        moist_merge=(
            QuicfireExportRequestMoistMerge(moist_merge)
            if moist_merge is not None
            else UNSET
        ),
        expiration_days=expiration_days,
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_quicfire_export_endpoint.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Export._from_model(expect(response, HTTPStatus.CREATED))


# ---------------------------------------------------------------------------
# Top-level fetch / list helpers
# ---------------------------------------------------------------------------


def list_exports(
    domain=None,
    page: int = 0,
    size: int = 100,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    source: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[Export]:
    """List your exports (single page), most filters optional.

    Parameters
    ----------
    domain : Domain or str, optional
        Only return exports of resources in this domain (or its id). If
        omitted, exports from all your domains are listed.
    page : int, optional
        The page number to retrieve, zero-indexed (default 0).
    size : int, optional
        The number of exports per page (default 100).
    sort_by : str, optional
        Field to sort by: "name", "created_on", or "modified_on".
    sort_order : str, optional
        Sort direction: "ascending" or "descending".
    source : str, optional
        Only return exports with this source name — the format for
        single-resource exports (e.g. "geotiff", "csv") or "quicfire"
        for bundles.
    tag : str, optional
        Only return exports carrying this tag.

    Returns
    -------
    List[Export]
        The requested page of Export objects.
    """
    response = list_exports_endpoint.sync_detailed(
        client=ensure_client(),
        page=page,
        size=size,
        sort_by=ExportSortField(sort_by) if sort_by else UNSET,
        sort_order=SortOrder(sort_order) if sort_order else UNSET,
        domain_id=_opt(_domain_id(domain) if domain is not None else None),
        source_name=_opt(source),
        tag=_opt(tag),
    )
    list_response: ListExportsResponse = expect(response)
    return [Export._from_model(e) for e in list_response.exports]


def get_export(export_id: str) -> Export:
    """Retrieve a single export by its ID.

    Parameters
    ----------
    export_id : str
        The unique identifier of the export.

    Returns
    -------
    Export
        The requested Export object.

    Raises
    ------
    NotFoundException
        If no export exists with the given ID, or the user does not have
        access.
    """
    return Export.from_id(export_id)
