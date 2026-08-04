from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feature_type import FeatureType
from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.feature_georeference import FeatureGeoreference
    from ..models.feature_source import FeatureSource
    from ..models.job_error import JobError
    from ..models.job_progress import JobProgress


T = TypeVar("T", bound="Feature")


@_attrs_define
class Feature:
    """The Feature resource.

    When status is "pending" or "running", georeference will be null.
    The backend worker populates it after successfully generating the GeoJSON
    and uploading it to GCS, at which point status transitions to "completed".

        Attributes:
            id (str):
            domain_id (str):
            type_ (FeatureType): Type of geographic feature.
            status (JobStatus): Status of an async job.
            source (FeatureSource):
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            progress (JobProgress | None | Unset): Progress info when status is 'running'. Null otherwise.
            created_on (datetime.datetime | None | Unset):
            modified_on (datetime.datetime | None | Unset):
            georeference (FeatureGeoreference | None | Unset): Spatial reference. Null until backend completes processing.
            error (JobError | None | Unset): Error details if status is 'failed'.
            tags (list[str] | Unset):
    """

    id: str
    domain_id: str
    type_: FeatureType
    status: JobStatus
    source: FeatureSource
    name: str | Unset = ""
    description: str | Unset = ""
    progress: JobProgress | None | Unset = UNSET
    created_on: datetime.datetime | None | Unset = UNSET
    modified_on: datetime.datetime | None | Unset = UNSET
    georeference: FeatureGeoreference | None | Unset = UNSET
    error: JobError | None | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.feature_georeference import FeatureGeoreference
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress

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

        georeference: dict[str, Any] | None | Unset
        if isinstance(self.georeference, Unset):
            georeference = UNSET
        elif isinstance(self.georeference, FeatureGeoreference):
            georeference = self.georeference.to_dict()
        else:
            georeference = self.georeference

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
        if georeference is not UNSET:
            field_dict["georeference"] = georeference
        if error is not UNSET:
            field_dict["error"] = error
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.feature_georeference import FeatureGeoreference
        from ..models.feature_source import FeatureSource
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress

        d = dict(src_dict)
        id = d.pop("id")

        domain_id = d.pop("domain_id")

        type_ = FeatureType(d.pop("type"))

        status = JobStatus(d.pop("status"))

        source = FeatureSource.from_dict(d.pop("source"))

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

        def _parse_georeference(data: object) -> FeatureGeoreference | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                georeference_type_0 = FeatureGeoreference.from_dict(data)

                return georeference_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FeatureGeoreference | None | Unset, data)

        georeference = _parse_georeference(d.pop("georeference", UNSET))

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

        feature = cls(
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
            georeference=georeference,
            error=error,
            tags=tags,
        )

        feature.additional_properties = d
        return feature

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
