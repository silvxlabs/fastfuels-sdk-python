"""
fastfuels_sdk/v2/point_clouds.py
"""

# Core imports
import json
from http import HTTPStatus
from typing import List, Optional

# Internal imports
from fastfuels_sdk.v2._jobs import wait as _wait
from fastfuels_sdk.v2._uploads import put_upload
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect
from fastfuels_sdk.v2.client_library.api.point_clouds import (
    create_point_cloud_upload,
    delete_point_cloud,
    get_point_cloud as get_point_cloud_endpoint,
    list_point_clouds as list_point_clouds_endpoint,
    list_point_clouds_cross_domain,
    update_point_cloud,
)
from fastfuels_sdk.v2.client_library.models import (
    PointCloud as PointCloudModel,
    CreatePointCloudUploadRequest,
    ListPointCloudsResponse,
    PointCloudSortField,
    PointCloudType,
    SortOrder,
    UpdatePointCloudRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET

# External imports
import attrs

__all__ = [
    "PointCloud",
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


class PointCloud(PointCloudModel):
    """Point cloud resource for the FastFuels v2 API.

    A point cloud is a 3D LiDAR dataset within a domain, uploaded from your own
    ALS (airborne) or TLS (terrestrial) scan. Point clouds are asynchronous job
    resources — creation starts a background job and returns a *pending* record;
    call :meth:`wait` to block until the uploaded file is processed.

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
    >>> import fastfuels_sdk as ff
    >>> pc = ff.point_clouds.create_point_cloud_from_file(
    ...     domain, "scan.laz", point_cloud_type="als"
    ... )
    >>> pc.wait()

    Get a point cloud by ID:
    >>> pc = ff.get_point_cloud(domain, "abc123")

    See Also
    --------
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

    def to_json(self) -> str:
        """Serialize the complete PointCloud object to a JSON string.

        Returns
        -------
        str
            The PointCloud as a pretty-printed JSON string.
        """
        return json.dumps(self.to_dict(), default=str, indent=2)


# ---------------------------------------------------------------------------
# Create a point cloud from your own file
# ---------------------------------------------------------------------------


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
