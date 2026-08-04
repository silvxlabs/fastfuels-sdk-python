from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inventory_type import InventoryType
from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column import Column
    from ..models.inventory_basal_area_treatment import InventoryBasalAreaTreatment
    from ..models.inventory_diameter_treatment import InventoryDiameterTreatment
    from ..models.inventory_georeference import InventoryGeoreference
    from ..models.inventory_modification import InventoryModification
    from ..models.inventory_source import InventorySource
    from ..models.job_error import JobError
    from ..models.job_progress import JobProgress
    from ..models.tree_forestry_metrics import TreeForestryMetrics


T = TypeVar("T", bound="Inventory")


@_attrs_define
class Inventory:
    """The Inventory resource.

    When status is "pending" or "running", georeference will be null.
    The backend populates it after successfully processing data,
    at which point status transitions to "completed".

        Attributes:
            id (str):
            domain_id (str):
            type_ (InventoryType): Type of entities in the inventory.
            status (JobStatus): Status of an async job.
            source (InventorySource):
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            progress (JobProgress | None | Unset): Progress info when status is 'running'. Null otherwise.
            created_on (datetime.datetime | None | Unset):
            modified_on (datetime.datetime | None | Unset):
            checksum (None | str | Unset): Version marker for this inventory's content. It changes each time the inventory
                is rebuilt and is unaffected by metadata-only edits (name, description, tags). A resource derived from this
                inventory stores the checksum it was built from; comparing that stored value against this field reveals whether
                this inventory has changed since. May be null for inventories created before checksums were introduced.
            modifications (list[InventoryModification] | Unset):
            treatments (list[InventoryBasalAreaTreatment | InventoryDiameterTreatment] | Unset):
            columns (list[Column] | Unset):
            forestry_metrics (None | TreeForestryMetrics | Unset):
            georeference (InventoryGeoreference | None | Unset): Spatial reference. Null until backend completes processing.
            error (JobError | None | Unset): Error details if status is 'failed'.
            tags (list[str] | Unset):
    """

    id: str
    domain_id: str
    type_: InventoryType
    status: JobStatus
    source: InventorySource
    name: str | Unset = ""
    description: str | Unset = ""
    progress: JobProgress | None | Unset = UNSET
    created_on: datetime.datetime | None | Unset = UNSET
    modified_on: datetime.datetime | None | Unset = UNSET
    checksum: None | str | Unset = UNSET
    modifications: list[InventoryModification] | Unset = UNSET
    treatments: (
        list[InventoryBasalAreaTreatment | InventoryDiameterTreatment] | Unset
    ) = UNSET
    columns: list[Column] | Unset = UNSET
    forestry_metrics: None | TreeForestryMetrics | Unset = UNSET
    georeference: InventoryGeoreference | None | Unset = UNSET
    error: JobError | None | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_diameter_treatment import InventoryDiameterTreatment
        from ..models.inventory_georeference import InventoryGeoreference
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress
        from ..models.tree_forestry_metrics import TreeForestryMetrics

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

        modifications: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.modifications, Unset):
            modifications = []
            for modifications_item_data in self.modifications:
                modifications_item = modifications_item_data.to_dict()
                modifications.append(modifications_item)

        treatments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.treatments, Unset):
            treatments = []
            for treatments_item_data in self.treatments:
                treatments_item: dict[str, Any]
                if isinstance(treatments_item_data, InventoryDiameterTreatment):
                    treatments_item = treatments_item_data.to_dict()
                else:
                    treatments_item = treatments_item_data.to_dict()

                treatments.append(treatments_item)

        columns: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()
                columns.append(columns_item)

        forestry_metrics: dict[str, Any] | None | Unset
        if isinstance(self.forestry_metrics, Unset):
            forestry_metrics = UNSET
        elif isinstance(self.forestry_metrics, TreeForestryMetrics):
            forestry_metrics = self.forestry_metrics.to_dict()
        else:
            forestry_metrics = self.forestry_metrics

        georeference: dict[str, Any] | None | Unset
        if isinstance(self.georeference, Unset):
            georeference = UNSET
        elif isinstance(self.georeference, InventoryGeoreference):
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
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if modifications is not UNSET:
            field_dict["modifications"] = modifications
        if treatments is not UNSET:
            field_dict["treatments"] = treatments
        if columns is not UNSET:
            field_dict["columns"] = columns
        if forestry_metrics is not UNSET:
            field_dict["forestry_metrics"] = forestry_metrics
        if georeference is not UNSET:
            field_dict["georeference"] = georeference
        if error is not UNSET:
            field_dict["error"] = error
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.column import Column
        from ..models.inventory_basal_area_treatment import InventoryBasalAreaTreatment
        from ..models.inventory_diameter_treatment import InventoryDiameterTreatment
        from ..models.inventory_georeference import InventoryGeoreference
        from ..models.inventory_modification import InventoryModification
        from ..models.inventory_source import InventorySource
        from ..models.job_error import JobError
        from ..models.job_progress import JobProgress
        from ..models.tree_forestry_metrics import TreeForestryMetrics

        d = dict(src_dict)
        id = d.pop("id")

        domain_id = d.pop("domain_id")

        type_ = InventoryType(d.pop("type"))

        status = JobStatus(d.pop("status"))

        source = InventorySource.from_dict(d.pop("source"))

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
        modifications: list[InventoryModification] | Unset = UNSET
        if _modifications is not UNSET:
            modifications = []
            for modifications_item_data in _modifications:
                modifications_item = InventoryModification.from_dict(
                    modifications_item_data
                )

                modifications.append(modifications_item)

        _treatments = d.pop("treatments", UNSET)
        treatments: (
            list[InventoryBasalAreaTreatment | InventoryDiameterTreatment] | Unset
        ) = UNSET
        if _treatments is not UNSET:
            treatments = []
            for treatments_item_data in _treatments:

                def _parse_treatments_item(
                    data: object,
                ) -> InventoryBasalAreaTreatment | InventoryDiameterTreatment:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        treatments_item_type_0 = InventoryDiameterTreatment.from_dict(
                            data
                        )

                        return treatments_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    treatments_item_type_1 = InventoryBasalAreaTreatment.from_dict(data)

                    return treatments_item_type_1

                treatments_item = _parse_treatments_item(treatments_item_data)

                treatments.append(treatments_item)

        _columns = d.pop("columns", UNSET)
        columns: list[Column] | Unset = UNSET
        if _columns is not UNSET:
            columns = []
            for columns_item_data in _columns:
                columns_item = Column.from_dict(columns_item_data)

                columns.append(columns_item)

        def _parse_forestry_metrics(data: object) -> None | TreeForestryMetrics | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                forestry_metrics_type_0 = TreeForestryMetrics.from_dict(data)

                return forestry_metrics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TreeForestryMetrics | Unset, data)

        forestry_metrics = _parse_forestry_metrics(d.pop("forestry_metrics", UNSET))

        def _parse_georeference(data: object) -> InventoryGeoreference | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                georeference_type_0 = InventoryGeoreference.from_dict(data)

                return georeference_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InventoryGeoreference | None | Unset, data)

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

        inventory = cls(
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
            modifications=modifications,
            treatments=treatments,
            columns=columns,
            forestry_metrics=forestry_metrics,
            georeference=georeference,
            error=error,
            tags=tags,
        )

        inventory.additional_properties = d
        return inventory

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
