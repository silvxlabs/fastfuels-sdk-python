from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.band import Band
    from ..models.chunks import Chunks
    from ..models.georeference import Georeference
    from ..models.georeference_3d import Georeference3D
    from ..models.grid_modification import GridModification
    from ..models.grid_source import GridSource
    from ..models.job_error import JobError
    from ..models.job_progress import JobProgress


T = TypeVar("T", bound="Grid")


@_attrs_define
class Grid:
    """The Grid resource.

    When status is "pending" or "running", georeference will be null.
    The backend populates georeference after successfully fetching data,
    at which point status transitions to "completed".

    When status is "failed", the error field contains details about what
    went wrong and suggestions for the user. The full traceback is stored
    in Firestore but not exposed in API responses.

        Attributes:
            id (str):
            domain_id (str):
            status (JobStatus): Status of an async job.
            source (GridSource):
            bands (list[Band]):
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            progress (JobProgress | None | Unset): Progress info when status is 'running'. Null otherwise.
            created_on (datetime.datetime | None | Unset):
            modified_on (datetime.datetime | None | Unset):
            checksum (None | str | Unset): Version marker for this grid's content. It changes each time the grid is rebuilt
                and is unaffected by metadata-only edits (name, description, tags). A resource derived from this grid stores the
                checksum it was built from; comparing that stored value against this field reveals whether this grid has changed
                since. May be null for grids created before checksums were introduced.
            modifications (list[GridModification] | Unset):
            georeference (Georeference | Georeference3D | None | Unset): Spatial reference. Null until backend completes
                data fetch.
            error (JobError | None | Unset): Error details if status is 'failed'. Traceback stored but not exposed.
            chunks (Chunks | None | Unset): Chunk layout. Null until the grid finishes processing. Use chunks.count to know
                how many chunks are available to fetch.
            tags (list[str] | Unset):
    """

    id: str
    domain_id: str
    status: JobStatus
    source: GridSource
    bands: list[Band]
    name: str | Unset = ""
    description: str | Unset = ""
    progress: JobProgress | None | Unset = UNSET
    created_on: datetime.datetime | None | Unset = UNSET
    modified_on: datetime.datetime | None | Unset = UNSET
    checksum: None | str | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    georeference: Georeference | Georeference3D | None | Unset = UNSET
    error: JobError | None | Unset = UNSET
    chunks: Chunks | None | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chunks import Chunks
        from ..models.georeference import Georeference
        from ..models.georeference_3d import Georeference3D
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress

        id = self.id

        domain_id = self.domain_id

        status = self.status.value

        source = self.source.to_dict()

        bands = []
        for bands_item_data in self.bands:
            bands_item = bands_item_data.to_dict()
            bands.append(bands_item)

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

        modifications: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.modifications, Unset):
            modifications = []
            for modifications_item_data in self.modifications:
                modifications_item = modifications_item_data.to_dict()
                modifications.append(modifications_item)

        georeference: dict[str, Any] | None | Unset
        if isinstance(self.georeference, Unset):
            georeference = UNSET
        elif isinstance(self.georeference, Georeference):
            georeference = self.georeference.to_dict()
        elif isinstance(self.georeference, Georeference3D):
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

        chunks: dict[str, Any] | None | Unset
        if isinstance(self.chunks, Unset):
            chunks = UNSET
        elif isinstance(self.chunks, Chunks):
            chunks = self.chunks.to_dict()
        else:
            chunks = self.chunks

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
                "bands": bands,
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
        if modifications is not UNSET:
            field_dict["modifications"] = modifications
        if georeference is not UNSET:
            field_dict["georeference"] = georeference
        if error is not UNSET:
            field_dict["error"] = error
        if chunks is not UNSET:
            field_dict["chunks"] = chunks
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.band import Band
        from ..models.chunks import Chunks
        from ..models.georeference import Georeference
        from ..models.georeference_3d import Georeference3D
        from ..models.grid_modification import GridModification
        from ..models.grid_source import GridSource
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress

        d = dict(src_dict)
        id = d.pop("id")

        domain_id = d.pop("domain_id")

        status = JobStatus(d.pop("status"))

        source = GridSource.from_dict(d.pop("source"))

        bands = []
        _bands = d.pop("bands")
        for bands_item_data in _bands:
            bands_item = Band.from_dict(bands_item_data)

            bands.append(bands_item)

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

        _modifications = d.pop("modifications", UNSET)
        modifications: list[GridModification] | Unset = UNSET
        if _modifications is not UNSET:
            modifications = []
            for modifications_item_data in _modifications:
                modifications_item = GridModification.from_dict(modifications_item_data)

                modifications.append(modifications_item)

        def _parse_georeference(
            data: object,
        ) -> Georeference | Georeference3D | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                georeference_type_0 = Georeference.from_dict(data)

                return georeference_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                georeference_type_1 = Georeference3D.from_dict(data)

                return georeference_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Georeference | Georeference3D | None | Unset, data)

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

        def _parse_chunks(data: object) -> Chunks | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                chunks_type_0 = Chunks.from_dict(data)

                return chunks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Chunks | None | Unset, data)

        chunks = _parse_chunks(d.pop("chunks", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        grid = cls(
            id=id,
            domain_id=domain_id,
            status=status,
            source=source,
            bands=bands,
            name=name,
            description=description,
            progress=progress,
            created_on=created_on,
            modified_on=modified_on,
            checksum=checksum,
            modifications=modifications,
            georeference=georeference,
            error=error,
            chunks=chunks,
            tags=tags,
        )

        grid.additional_properties = d
        return grid

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
