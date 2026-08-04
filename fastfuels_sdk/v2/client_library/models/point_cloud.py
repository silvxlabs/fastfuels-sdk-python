from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..models.point_cloud_type import PointCloudType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_error import JobError
    from ..models.job_progress import JobProgress
    from ..models.point_cloud_georeference import PointCloudGeoreference
    from ..models.point_cloud_source import PointCloudSource
    from ..models.point_cloud_summary import PointCloudSummary


T = TypeVar("T", bound="PointCloud")


@_attrs_define
class PointCloud:
    """A laser-scanned point cloud scoped to a single domain.

    Point clouds are created asynchronously: a creation request returns
    immediately with ``status="pending"`` and the file is ingested in the
    background. While ``status`` is ``"pending"`` or ``"running"`` the
    derived fields (`georeference`) are ``null``; the backend fills them in once
    ingestion succeeds and flips ``status`` to ``"completed"``. If ingestion
    fails, ``status`` becomes ``"failed"`` and `error` explains why.

    A completed point cloud is an input you compose with other resources — most
    directly, an ALS cloud feeds a canopy-height-model grid, which feeds a tree
    inventory.

        Attributes:
            id (str): Unique 32-character hex identifier for this point cloud.
            domain_id (str): Identifier of the domain this point cloud belongs to.
            type_ (PointCloudType): How a point cloud was acquired.

                The acquisition platform determines the cloud's geometry and which downstream
                products it can feed, so it is recorded as a first-class, filterable field.

                - ``als`` — **Airborne Laser Scanning.** Captured from an aircraft or drone
                  looking down. Covers large areas from above and is the basis for canopy
                  height models and individual-tree detection. Available from an upload or
                  from USGS 3DEP.
                - ``tls`` — **Terrestrial Laser Scanning.** Captured from a tripod-mounted
                  scanner on the ground looking out and up. Resolves fine sub-canopy and
                  stem structure over a small plot. Available from an upload only (3DEP is
                  airborne and cannot produce terrestrial scans).
            status (JobStatus): Status of an async job.
            source (PointCloudSource): Provenance of the point cloud — where its points came from. Always carries a `name`
                discriminator (`upload` for a user-supplied file, `3dep` for a USGS 3DEP fetch) alongside source-specific
                parameters. Stored verbatim so the cloud can be reproduced from its origin.
            name (str | Unset): Human-readable name for the point cloud. Default: ''.
            description (str | Unset): Longer free-text description of the point cloud. Default: ''.
            progress (JobProgress | None | Unset): Progress info while `status` is `running`. Null otherwise.
            created_on (datetime.datetime | None | Unset): When the point cloud was created.
            modified_on (datetime.datetime | None | Unset): When the point cloud was last modified.
            checksum (None | str | Unset): Version marker for this point cloud's content. It changes each time the point
                cloud is rebuilt and is unaffected by metadata-only edits (name, description, tags). A resource derived from
                this point cloud stores the checksum it was built from; comparing that stored value against this field reveals
                whether this point cloud has changed since. May be null for point clouds created before checksums were
                introduced.
            georeference (None | PointCloudGeoreference | Unset): Coordinate reference system and 3D extent of the points.
                Null until the backend finishes ingesting the cloud.
            summary (None | PointCloudSummary | Unset): Summary statistics — point count, classification codes present, and
                density — describing the cloud's contents. Null until the backend finishes ingesting the cloud.
            error (JobError | None | Unset): Details when `status` is `failed`. The traceback is stored but not exposed in
                API responses.
            tags (list[str] | Unset): User-assigned tags for organizing and filtering point clouds.
    """

    id: str
    domain_id: str
    type_: PointCloudType
    status: JobStatus
    source: PointCloudSource
    name: str | Unset = ""
    description: str | Unset = ""
    progress: JobProgress | None | Unset = UNSET
    created_on: datetime.datetime | None | Unset = UNSET
    modified_on: datetime.datetime | None | Unset = UNSET
    checksum: None | str | Unset = UNSET
    georeference: None | PointCloudGeoreference | Unset = UNSET
    summary: None | PointCloudSummary | Unset = UNSET
    error: JobError | None | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress
        from ..models.point_cloud_georeference import PointCloudGeoreference
        from ..models.point_cloud_summary import PointCloudSummary

        id = self.id

        domain_id = self.domain_id

        type_ = self.type_.value

        status = self.status.value

        source = self.source.to_dict()

        name = self.name

        description = self.description

        progress: dict[str, Any] | None | Unset
        if isinstance(self.progress, Unset):
            progress = UNSET
        elif isinstance(self.progress, JobProgress):
            progress = self.progress.to_dict()
        else:
            progress = self.progress

        created_on: None | str | Unset
        if isinstance(self.created_on, Unset):
            created_on = UNSET
        elif isinstance(self.created_on, datetime.datetime):
            created_on = self.created_on.isoformat()
        else:
            created_on = self.created_on

        modified_on: None | str | Unset
        if isinstance(self.modified_on, Unset):
            modified_on = UNSET
        elif isinstance(self.modified_on, datetime.datetime):
            modified_on = self.modified_on.isoformat()
        else:
            modified_on = self.modified_on

        checksum: None | str | Unset
        if isinstance(self.checksum, Unset):
            checksum = UNSET
        else:
            checksum = self.checksum

        georeference: dict[str, Any] | None | Unset
        if isinstance(self.georeference, Unset):
            georeference = UNSET
        elif isinstance(self.georeference, PointCloudGeoreference):
            georeference = self.georeference.to_dict()
        else:
            georeference = self.georeference

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, PointCloudSummary):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        error: dict[str, Any] | None | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, JobError):
            error = self.error.to_dict()
        else:
            error = self.error

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "domain_id": domain_id,
                "type": type_,
                "status": status,
                "source": source,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if progress is not UNSET:
            field_dict["progress"] = progress
        if created_on is not UNSET:
            field_dict["created_on"] = created_on
        if modified_on is not UNSET:
            field_dict["modified_on"] = modified_on
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if georeference is not UNSET:
            field_dict["georeference"] = georeference
        if summary is not UNSET:
            field_dict["summary"] = summary
        if error is not UNSET:
            field_dict["error"] = error
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress
        from ..models.point_cloud_georeference import PointCloudGeoreference
        from ..models.point_cloud_source import PointCloudSource
        from ..models.point_cloud_summary import PointCloudSummary

        d = dict(src_dict)
        id = d.pop("id")

        domain_id = d.pop("domain_id")

        type_ = PointCloudType(d.pop("type"))

        status = JobStatus(d.pop("status"))

        source = PointCloudSource.from_dict(d.pop("source"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        def _parse_progress(data: object) -> JobProgress | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                progress_type_0 = JobProgress.from_dict(data)

                return progress_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobProgress | None | Unset, data)

        progress = _parse_progress(d.pop("progress", UNSET))

        def _parse_created_on(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_on_type_0 = datetime.datetime.fromisoformat(data)

                return created_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_on = _parse_created_on(d.pop("created_on", UNSET))

        def _parse_modified_on(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                modified_on_type_0 = datetime.datetime.fromisoformat(data)

                return modified_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        modified_on = _parse_modified_on(d.pop("modified_on", UNSET))

        def _parse_checksum(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        checksum = _parse_checksum(d.pop("checksum", UNSET))

        def _parse_georeference(data: object) -> None | PointCloudGeoreference | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                georeference_type_0 = PointCloudGeoreference.from_dict(data)

                return georeference_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PointCloudGeoreference | Unset, data)

        georeference = _parse_georeference(d.pop("georeference", UNSET))

        def _parse_summary(data: object) -> None | PointCloudSummary | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0 = PointCloudSummary.from_dict(data)

                return summary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PointCloudSummary | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_error(data: object) -> JobError | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = JobError.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobError | None | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        point_cloud = cls(
            id=id,
            domain_id=domain_id,
            type_=type_,
            status=status,
            source=source,
            name=name,
            description=description,
            progress=progress,
            created_on=created_on,
            modified_on=modified_on,
            checksum=checksum,
            georeference=georeference,
            summary=summary,
            error=error,
            tags=tags,
        )

        point_cloud.additional_properties = d
        return point_cloud

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
