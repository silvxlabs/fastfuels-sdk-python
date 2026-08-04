from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.export_source import ExportSource
    from ..models.job_error import JobError
    from ..models.job_progress import JobProgress


T = TypeVar("T", bound="Export")


@_attrs_define
class Export:
    """The Export resource.

    Exports are standalone artifacts that record provenance (domain_id, grid_id)
    but have independent lifecycle — deleting a domain does not delete its exports.

    When status is "completed", signed_url contains a signed URL for
    downloading the exported file.

        Attributes:
            id (str):
            domain_id (str): Domain the source grids belong to (provenance, not lifecycle dependency).
            status (JobStatus): Status of an async job.
            source (ExportSource): Format-specific export configuration. Contains 'name' (the export format) plus additional
                fields depending on the source type.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            progress (JobProgress | None | Unset): Progress info when status is 'running'. Null otherwise.
            created_on (datetime.datetime | None | Unset):
            modified_on (datetime.datetime | None | Unset):
            signed_url (None | str | Unset): Signed URL for downloading the exported file. Populated on completion.
            expires_on (datetime.datetime | None | Unset): When the signed URL expires.
            error (JobError | None | Unset): Error details if status is 'failed'.
            tags (list[str] | Unset):
    """

    id: str
    domain_id: str
    status: JobStatus
    source: ExportSource
    name: str | Unset = ""
    description: str | Unset = ""
    progress: JobProgress | None | Unset = UNSET
    created_on: datetime.datetime | None | Unset = UNSET
    modified_on: datetime.datetime | None | Unset = UNSET
    signed_url: None | str | Unset = UNSET
    expires_on: datetime.datetime | None | Unset = UNSET
    error: JobError | None | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress

        id = self.id

        domain_id = self.domain_id

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

        signed_url: None | str | Unset
        if isinstance(self.signed_url, Unset):
            signed_url = UNSET
        else:
            signed_url = self.signed_url

        expires_on: None | str | Unset
        if isinstance(self.expires_on, Unset):
            expires_on = UNSET
        elif isinstance(self.expires_on, datetime.datetime):
            expires_on = self.expires_on.isoformat()
        else:
            expires_on = self.expires_on

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
        if signed_url is not UNSET:
            field_dict["signed_url"] = signed_url
        if expires_on is not UNSET:
            field_dict["expires_on"] = expires_on
        if error is not UNSET:
            field_dict["error"] = error
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.export_source import ExportSource
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress

        d = dict(src_dict)
        id = d.pop("id")

        domain_id = d.pop("domain_id")

        status = JobStatus(d.pop("status"))

        source = ExportSource.from_dict(d.pop("source"))

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

        def _parse_signed_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        signed_url = _parse_signed_url(d.pop("signed_url", UNSET))

        def _parse_expires_on(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_on_type_0 = datetime.datetime.fromisoformat(data)

                return expires_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_on = _parse_expires_on(d.pop("expires_on", UNSET))

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

        export = cls(
            id=id,
            domain_id=domain_id,
            status=status,
            source=source,
            name=name,
            description=description,
            progress=progress,
            created_on=created_on,
            modified_on=modified_on,
            signed_url=signed_url,
            expires_on=expires_on,
            error=error,
            tags=tags,
        )

        export.additional_properties = d
        return export

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
