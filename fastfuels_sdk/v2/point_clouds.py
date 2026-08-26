"""
fastfuels_sdk/v2/point_clouds.py
"""

# Core imports
import json
from http import HTTPStatus
from typing import List, Optional, Sequence, Union

# Internal imports
from fastfuels_sdk.v2._jobs import wait as _wait
from fastfuels_sdk.v2._uploads import put_upload
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect, raise_for_response
from fastfuels_sdk.v2.client_library.api.point_clouds import (
    check_3dep_point_cloud_coverage,
    create_3dep_point_cloud as create_3dep_point_cloud_endpoint,
    create_point_cloud_upload,
    delete_point_cloud,
    get_point_cloud as get_point_cloud_endpoint,
    get_point_cloud_data_binary,
    get_point_cloud_data_metadata,
    list_point_clouds as list_point_clouds_endpoint,
    list_point_clouds_cross_domain,
    update_point_cloud,
)
from fastfuels_sdk.v2.client_library.models import (
    PointCloud as PointCloudModel,
    CreatePointCloudUploadRequest,
    CreateThreeDepPointCloudRequest,
    JobStatus,
    ListPointCloudsResponse,
    PointCloudDataMetadata,
    PointCloudThreeDepCoverageResponse,
    PointCloudSortField,
    PointCloudType,
    SortOrder,
    UpdatePointCloudRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Response

# External imports
import attrs
import numpy as np

__all__ = [
    "PointCloud",
    "check_3dep_coverage",
    "create_point_cloud_from_3dep",
    "create_point_cloud_from_file",
    "list_point_clouds",
    "get_point_cloud",
]


def _domain_id(domain) -> str:
    """Resolve a Domain object or a domain-id string to the id string."""
    return getattr(domain, "id", domain)


def _opt(value):
    """Map ``None`` to the generated UNSET sentinel, else pass through."""
    return value if value is not None else UNSET


def _point_cloud_type(value) -> PointCloudType:
    """Coerce a string or enum member to a ``PointCloudType``."""
    return value if isinstance(value, PointCloudType) else PointCloudType(value)


# X/Y/Z are stored as scaled integers and decoded per axis in this order.
_XYZ = ("X", "Y", "Z")


def _csv(values) -> Optional[str]:
    """Render a scalar or sequence as the comma-separated query string the
    tile endpoints expect, or ``None`` to omit the parameter."""
    if values is None:
        return None
    if isinstance(values, str):
        return values
    return ",".join(str(v) for v in values)


def _decode_point_cloud_tile(content: bytes, headers) -> dict:
    """Decode one binary point-cloud tile into ``{column: np.ndarray}``.

    The tile endpoint returns ``application/octet-stream``: one contiguous
    little-endian column block after another in ``X-Data-Columns`` order (see
    ``get_point_cloud_data_binary``). Every block holds ``X-Data-Count`` values
    of the matching dtype in ``X-Data-Dtypes``. ``X``, ``Y``, and ``Z`` remain
    the stored scaled integers.
    """
    columns = headers["X-Data-Columns"].split(",")
    dtypes = headers["X-Data-Dtypes"].split(",")
    count = int(headers["X-Data-Count"])

    blocks = {}
    start = 0
    for name, dtype_str in zip(columns, dtypes):
        dtype = np.dtype(dtype_str).newbyteorder("<")
        stop = start + count * dtype.itemsize
        blocks[name] = np.frombuffer(content[start:stop], dtype=dtype)
        start = stop
    return blocks


class PointCloud(PointCloudModel):
    """Point cloud resource for the FastFuels v2 API.

    A point cloud is a 3D LiDAR dataset within a domain, either fetched from
    USGS 3DEP or uploaded from your own ALS (airborne) or TLS (terrestrial)
    scan. Point clouds are asynchronous job resources — creation starts a
    background job and returns a *pending* record; call :meth:`wait` to block
    until the data is processed.

    Attributes
    ----------
    id : str
        Unique identifier for the point cloud.
    domain_id : str
        Identifier of the domain the point cloud belongs to.
    type_ : PointCloudType
        Scan type: "als" (airborne) or "tls" (terrestrial).
    status : JobStatus
        Job status: "pending", "running", "completed", or "failed".
    source : PointCloudSource
        Where the point cloud data comes from.
    name : str
        Human-readable name for the point cloud.
    description : str
        Detailed description of the point cloud.
    progress : JobProgress, optional
        Progress info while the job is running.
    checksum : str, optional
        Version marker for the point cloud's content; changes each time the
        data is rebuilt, unaffected by metadata-only edits.
    georeference : PointCloudGeoreference, optional
        Spatial reference (CRS and bounds); populated when the job completes.
    summary : PointCloudSummary, optional
        Summary statistics of the points; populated when the job completes.
    error : JobError, optional
        Error details if the job failed.
    tags : List[str], optional
        User-defined tags for organization.
    created_on : datetime
        When the point cloud was created.
    modified_on : datetime
        When the point cloud was last modified.

    Examples
    --------
    Upload a point cloud and wait for it to process:
    >>> import fastfuels_sdk.v2 as ff
    >>> pc = ff.point_clouds.create_point_cloud_from_file(
    ...     domain, "scan.laz", point_cloud_type="als"
    ... )
    >>> pc.wait()

    Get a point cloud by ID:
    >>> pc = ff.get_point_cloud(domain, "abc123")

    See Also
    --------
    create_point_cloud_from_3dep : Fetch public airborne LiDAR from USGS 3DEP.
    create_point_cloud_from_file : Upload a local LiDAR file.
    list_point_clouds : List point clouds in a domain or across all domains.
    """

    @classmethod
    def _from_model(cls, model: PointCloudModel) -> "PointCloud":
        """Build a PointCloud from a generated PointCloud model instance.

        Round-trips through the generated to_dict/from_dict — from_dict
        constructs ``cls``, i.e. this subclass.
        """
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: PointCloudModel) -> "PointCloud":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(PointCloudModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    @classmethod
    def from_id(cls, domain_id: str, point_cloud_id: str) -> "PointCloud":
        """Retrieve an existing PointCloud resource by its ID.

        Parameters
        ----------
        domain_id : str
            The unique identifier of the domain the point cloud belongs to.
        point_cloud_id : str
            The unique identifier of the point cloud to retrieve.

        Returns
        -------
        PointCloud
            The requested PointCloud object.

        Raises
        ------
        NotFoundException
            If no point cloud exists with the given IDs, or the user does not
            have access to it.
        """
        response = get_point_cloud_endpoint.sync_detailed(
            domain_id, point_cloud_id, client=ensure_client()
        )
        return cls._from_model(expect(response))

    def refresh(self) -> "PointCloud":
        """Update this PointCloud in place with the latest data from the API.

        Returns
        -------
        PointCloud
            ``self``, updated with the latest data (so calls chain).

        Raises
        ------
        NotFoundException
            If the point cloud no longer exists.
        """
        response = get_point_cloud_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        return self._copy_fields_from(expect(response))

    def wait(
        self, timeout: Optional[float] = None, verbose: bool = False
    ) -> "PointCloud":
        """Poll the point cloud job until it reaches a terminal status.

        Parameters
        ----------
        timeout : float, optional
            Maximum seconds to wait. ``None`` (default) waits indefinitely; the
            job runs server-side regardless, so a bounded wait is resumable.
        verbose : bool, optional
            If True, print the job status at each poll.

        Returns
        -------
        PointCloud
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
    ) -> "PointCloud":
        """Update the point cloud's metadata (name, description, tags) in place.

        Only provided fields are sent. If no fields are provided, no API call
        is made.

        Parameters
        ----------
        name : str, optional
            New name for the point cloud.
        description : str, optional
            New description for the point cloud.
        tags : List[str], optional
            New tags for the point cloud (replaces existing tags).

        Returns
        -------
        PointCloud
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the point cloud no longer exists.
        """
        if name is None and description is None and tags is None:
            return self
        request_body = UpdatePointCloudRequestBody(
            name=_opt(name), description=_opt(description), tags=_opt(tags)
        )
        response = update_point_cloud.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def delete(self) -> None:
        """Delete this point cloud and its data.

        Raises
        ------
        NotFoundException
            If the point cloud no longer exists.
        """
        response = delete_point_cloud.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        expect(response, HTTPStatus.NO_CONTENT)

    def _require_completed(self, action: str) -> None:
        """Raise if the point cloud is not completed, before deriving from it."""
        if self.status != JobStatus.COMPLETED:
            raise ValueError(
                f"Cannot {action} a point cloud with status '{self.status}'. Call "
                ".wait() until it completes first."
            )

    def metadata(self) -> PointCloudDataMetadata:
        """Return the point cloud's tile index without downloading any points.

        The metadata is the entry point for reading data: it lists the occupied
        tiles, the stored columns and their dtypes, the coordinate encoding
        (``scales``/``offsets``), and the cumulative point count at each level
        of detail. :meth:`to_numpy` and :meth:`to_dataframe` page over the tiles
        it reports.

        Returns
        -------
        PointCloudDataMetadata
            The tile catalogue: ``tile_m``, ``lod_levels``, ``crs``,
            ``bounds``, ``scales``, ``offsets``, ``columns``, and ``tiles``.

        Raises
        ------
        ValueError
            If the point cloud is not completed.
        NotFoundException
            If the point cloud no longer exists.

        Examples
        --------
        >>> pc = ff.get_point_cloud(domain, "abc123").wait()
        >>> meta = pc.metadata()
        >>> len(meta.tiles)
        4
        """
        self._require_completed("read data metadata from")
        response = get_point_cloud_data_metadata.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        return expect(response)

    def _request_tile(self, tile_x, tile_y, lod, classes, columns):
        """GET one binary tile as a raw octet-stream ``httpx.Response``.

        Bypasses ``get_point_cloud_data_binary.sync_detailed()``, whose
        generated parser casts the binary body to ``str``. We reuse its
        ``_get_kwargs()`` for correct URL/param construction, then issue the
        request through the shared client and read the bytes/headers directly.
        """
        kwargs = get_point_cloud_data_binary._get_kwargs(
            self.domain_id,
            self.id,
            tile_x,
            tile_y,
            lod=_opt(lod),
            classes=_opt(classes),
            columns=_opt(columns),
        )
        return ensure_client().get_httpx_client().request(**kwargs)

    def _read_tile(self, tile_x, tile_y, lod, classes, columns) -> dict:
        """Fetch and decode one tile into ``{column: np.ndarray}``."""
        response = self._request_tile(tile_x, tile_y, lod, classes, columns)
        if response.status_code != HTTPStatus.OK:
            raise_for_response(
                Response(
                    status_code=HTTPStatus(response.status_code),
                    content=response.content,
                    headers=response.headers,
                    parsed=None,
                )
            )
        return _decode_point_cloud_tile(response.content, response.headers)

    def _read_columns(self, lod, classes, columns):
        """Page over every occupied tile and concatenate each column.

        Returns ``(metadata, order, columns_dict)`` where ``order`` is the
        column order the tiles reported and ``columns_dict`` maps each name to
        the points concatenated across all tiles (``X``/``Y``/``Z`` still the
        stored scaled integers).
        """
        classes_param = _csv(classes)
        columns_param = _csv(columns)

        meta = self.metadata()
        order = None
        accumulated = {}
        for tile in meta.tiles:
            blocks = self._read_tile(
                tile.tile_x, tile.tile_y, lod, classes_param, columns_param
            )
            if order is None:
                order = list(blocks.keys())
            for name, block in blocks.items():
                accumulated.setdefault(name, []).append(block)

        if order is None:
            # No occupied tiles: return empty, correctly-typed columns using the
            # dtypes the metadata advertises.
            order = list(columns) if columns else list(meta.columns.additional_keys)
            empty = {
                name: np.frombuffer(b"", dtype=np.dtype(meta.columns[name]))
                for name in order
            }
            return meta, order, empty

        result = {name: np.concatenate(accumulated[name]) for name in order}
        return meta, order, result

    def _decode_xyz(self, meta, columns: dict) -> None:
        """Decode stored ``X``/``Y``/``Z`` integers to CRS coordinates in place."""
        for axis, name in enumerate(_XYZ):
            if name in columns:
                columns[name] = columns[name] * meta.scales[axis] + meta.offsets[axis]

    def to_dataframe(
        self,
        lod: Optional[int] = None,
        classes: Optional[Union[int, Sequence[int], str]] = None,
        columns: Optional[Sequence[str]] = None,
        decode_coordinates: bool = True,
    ):
        """Read this point cloud's points into an in-memory pandas DataFrame.

        Pages over every occupied tile and stacks them into one frame, one row
        per point and one column per stored attribute (``X``, ``Y``, ``Z``,
        ``classification``, and any source columns such as ``intensity``).

        Parameters
        ----------
        lod : int, optional
            Inclusive level-of-detail ceiling. ``0`` is the coarsest sample and
            each higher value adds finer points; ``None`` (default) reads every
            point. Valid values are ``0`` through ``lod_levels - 1`` from
            :meth:`metadata`.
        classes : int or sequence of int or str, optional
            ASPRS classification codes to keep (e.g. ``[2, 5]`` for ground and
            high vegetation). ``None`` (default) keeps every class.
        columns : sequence of str, optional
            Stored columns to read, in the returned order. ``None`` (default)
            reads every stored column (see :meth:`metadata`).
        decode_coordinates : bool, optional
            If True (default), ``X``/``Y``/``Z`` are decoded to CRS coordinates
            (floats). If False, they stay the stored scaled integers.

        Returns
        -------
        pandas.DataFrame
            One row per point, columns in ``columns`` order (or the point
            cloud's stored order).

        Raises
        ------
        ValueError
            If the point cloud is not completed.

        Examples
        --------
        >>> pc = ff.get_point_cloud(domain, "abc123").wait()
        >>> df = pc.to_dataframe(classes=[2])
        >>> df.columns.tolist()
        ['X', 'Y', 'Z', 'classification']
        """
        import pandas as pd

        self._require_completed("read data from")
        meta, order, cols = self._read_columns(lod, classes, columns)
        if decode_coordinates:
            self._decode_xyz(meta, cols)
        return pd.DataFrame({name: cols[name] for name in order})

    def to_numpy(
        self,
        lod: Optional[int] = None,
        classes: Optional[Union[int, Sequence[int], str]] = None,
        columns: Sequence[str] = _XYZ,
        decode_coordinates: bool = True,
    ) -> "np.ndarray":
        """Read this point cloud's points into an in-memory NumPy array.

        Pages over every occupied tile and stacks the requested columns into a
        single ``(N, k)`` array, where ``N`` is the total number of points and
        ``k`` is the number of columns. All columns share the ``float64`` dtype
        of the returned array.

        Parameters
        ----------
        lod : int, optional
            Inclusive level-of-detail ceiling. ``0`` is the coarsest sample and
            each higher value adds finer points; ``None`` (default) reads every
            point. Valid values are ``0`` through ``lod_levels - 1`` from
            :meth:`metadata`.
        classes : int or sequence of int or str, optional
            ASPRS classification codes to keep (e.g. ``[2, 5]`` for ground and
            high vegetation). ``None`` (default) keeps every class.
        columns : sequence of str, optional
            Columns to stack into the array, in order. Defaults to the
            ``("X", "Y", "Z")`` coordinates.
        decode_coordinates : bool, optional
            If True (default), ``X``/``Y``/``Z`` are decoded to CRS coordinates.
            If False, they stay the stored scaled integers.

        Returns
        -------
        numpy.ndarray
            A ``(N, k)`` ``float64`` array of the requested columns.

        Raises
        ------
        ValueError
            If the point cloud is not completed.

        Examples
        --------
        >>> pc = ff.get_point_cloud(domain, "abc123").wait()
        >>> points = pc.to_numpy()
        >>> points.shape
        (48213, 3)
        """
        self._require_completed("read data from")
        meta, order, cols = self._read_columns(lod, classes, list(columns))
        if decode_coordinates:
            self._decode_xyz(meta, cols)
        return np.column_stack([cols[name].astype(np.float64) for name in order])

    def to_json(self) -> str:
        """Serialize the complete PointCloud object to a JSON string.

        Returns
        -------
        str
            The PointCloud as a pretty-printed JSON string.
        """
        return json.dumps(self.to_dict(), default=str, indent=2)


# ---------------------------------------------------------------------------
# Create point clouds
# ---------------------------------------------------------------------------


def check_3dep_coverage(domain) -> PointCloudThreeDepCoverageResponse:
    """Check USGS 3DEP LiDAR coverage before creating a point cloud.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to check.

    Returns
    -------
    PointCloudThreeDepCoverageResponse
        Availability, coverage fraction, estimated point count and budget,
        and the contributing acquisitions.
    """
    response = check_3dep_point_cloud_coverage.sync_detailed(
        _domain_id(domain),
        client=ensure_client(),
    )
    return expect(response)


def create_point_cloud_from_3dep(
    domain,
    datasets: Optional[List[str]] = None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> PointCloud:
    """Create an airborne point cloud from USGS 3DEP LiDAR.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the point cloud in.
    datasets : List[str], optional
        Acquisition names to read, in priority order. Use
        :func:`check_3dep_coverage` to discover names. If omitted, the API
        selects acquisitions automatically.
    name, description : str, optional
        Metadata for the point cloud.
    tags : List[str], optional
        Tags for the point cloud.

    Returns
    -------
    PointCloud
        The created airborne PointCloud (job status "pending" or "running").
    """
    request_body = CreateThreeDepPointCloudRequest(
        datasets=_opt(datasets),
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_3dep_point_cloud_endpoint.sync_detailed(
        _domain_id(domain),
        client=ensure_client(),
        body=request_body,
    )
    return PointCloud._from_model(expect(response, HTTPStatus.CREATED))


def create_point_cloud_from_file(
    domain,
    path: str,
    point_cloud_type: str,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> PointCloud:
    """Create a point cloud by uploading a local LiDAR file.

    Creates the point cloud resource, uploads the file to the returned signed
    URL, and returns the (pending) PointCloud.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the point cloud in.
    path : str
        Path to the local LiDAR file (e.g. ``.las``/``.laz``).
    point_cloud_type : str
        Scan type: "als" (airborne) or "tls" (terrestrial). A
        ``PointCloudType`` member is also accepted.
    name, description : str, optional
        Metadata for the point cloud.
    tags : List[str], optional
        Tags for the point cloud.

    Returns
    -------
    PointCloud
        The created PointCloud object (job status "pending"). Call
        :meth:`PointCloud.wait` to block until the uploaded file is processed.
    """
    request_body = CreatePointCloudUploadRequest(
        type_=_point_cloud_type(point_cloud_type),
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_point_cloud_upload.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    created = expect(response, HTTPStatus.CREATED)
    put_upload(created.upload, path)
    return PointCloud._from_model(created.point_cloud)


# ---------------------------------------------------------------------------
# Top-level fetch / list helpers
# ---------------------------------------------------------------------------


def list_point_clouds(
    domain=None,
    page: int = 0,
    size: int = 100,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    point_cloud_type: Optional[str] = None,
    source: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[PointCloud]:
    """List point clouds in a domain, or across all domains (single page).

    Parameters
    ----------
    domain : Domain or str, optional
        The domain (or its id) to list point clouds in. If omitted, point
        clouds from all the user's domains are listed.
    page : int, optional
        The page number to retrieve, zero-indexed (default 0).
    size : int, optional
        The number of point clouds per page (default 100).
    sort_by : str, optional
        Field to sort by: "name", "created_on", or "modified_on".
    sort_order : str, optional
        Sort direction: "ascending" or "descending".
    point_cloud_type : str, optional
        Only return point clouds of this scan type: "als" or "tls".
    source : str, optional
        Only return point clouds from this source.
    tag : str, optional
        Only return point clouds carrying this tag.

    Returns
    -------
    List[PointCloud]
        The requested page of PointCloud objects.
    """
    kwargs = dict(
        client=ensure_client(),
        page=page,
        size=size,
        sort_by=PointCloudSortField(sort_by) if sort_by else UNSET,
        sort_order=SortOrder(sort_order) if sort_order else UNSET,
        type_=_point_cloud_type(point_cloud_type) if point_cloud_type else UNSET,
        source=_opt(source),
        tag=_opt(tag),
    )
    if domain is None:
        response = list_point_clouds_cross_domain.sync_detailed(**kwargs)
    else:
        response = list_point_clouds_endpoint.sync_detailed(
            _domain_id(domain), **kwargs
        )
    list_response: ListPointCloudsResponse = expect(response)
    return [PointCloud._from_model(pc) for pc in list_response.point_clouds]


def get_point_cloud(domain, point_cloud_id: str) -> PointCloud:
    """Retrieve a single point cloud by its ID.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) the point cloud belongs to.
    point_cloud_id : str
        The unique identifier of the point cloud.

    Returns
    -------
    PointCloud
        The requested PointCloud object.

    Raises
    ------
    NotFoundException
        If no point cloud exists with the given IDs, or the user does not have
        access.
    """
    return PointCloud.from_id(_domain_id(domain), point_cloud_id)
