from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inventory_type import InventoryType
from ..models.point_process import PointProcess
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inventory_basal_area_treatment import InventoryBasalAreaTreatment
    from ..models.inventory_diameter_treatment import InventoryDiameterTreatment
    from ..models.inventory_modification import InventoryModification
    from ..models.reimputation_method import ReimputationMethod


T = TypeVar("T", bound="CreatePimChmFusionInventoryRequest")


@_attrs_define
class CreatePimChmFusionInventoryRequest:
    """Request body for creating an inventory by fusing a PIM with a CHM.

    Attributes:
        source_pim_grid_id (str): ID of a completed PIM grid to use as the primary source.
        source_chm_grid_id (str): ID of a completed CHM grid used to condition the PIM.
        type_ (InventoryType | Unset): Type of entities in the inventory.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        method (ReimputationMethod | Unset): The v1 fusion algorithm (``fastfuels_core.onramps.hag_pim``).

            Resample the PIM to ``resolution``, keep a cell's plot only where the CHM's
            canopy cover — the fraction of CHM cells taller than ``min_height`` — exceeds
            ``cover_threshold``, then expand the surviving plots as ``tree/pim``.
            ``resolution`` and ``min_height`` are the v1 production values;
            ``cover_threshold`` defaults to 0.2. ``fastfuels-core``'s own defaults are
            1.0 m and 0.25.
        seed (int | Unset): Random seed for reproducibility. Generated randomly if omitted.
        point_process (PointProcess | Unset): Spatial point process for tree coordinate assignment.
        modifications (list[InventoryModification] | Unset): Modifications to apply after point process expansion.
        treatments (list[InventoryBasalAreaTreatment | InventoryDiameterTreatment] | Unset): Silvicultural treatments to
            apply after modifications.
    """

    source_pim_grid_id: str
    source_chm_grid_id: str
    type_: InventoryType | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    method: ReimputationMethod | Unset = UNSET
    seed: int | Unset = UNSET
    point_process: PointProcess | Unset = UNSET
    modifications: list[InventoryModification] | Unset = UNSET
    treatments: (
        list[InventoryBasalAreaTreatment | InventoryDiameterTreatment] | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_diameter_treatment import InventoryDiameterTreatment

        source_pim_grid_id = self.source_pim_grid_id

        source_chm_grid_id = self.source_chm_grid_id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        method: dict[str, Any] | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.to_dict()

        seed = self.seed

        point_process: str | Unset = UNSET
        if not isinstance(self.point_process, Unset):
            point_process = self.point_process.value

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_pim_grid_id": source_pim_grid_id,
                "source_chm_grid_id": source_chm_grid_id,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if method is not UNSET:
            field_dict["method"] = method
        if seed is not UNSET:
            field_dict["seed"] = seed
        if point_process is not UNSET:
            field_dict["point_process"] = point_process
        if modifications is not UNSET:
            field_dict["modifications"] = modifications
        if treatments is not UNSET:
            field_dict["treatments"] = treatments

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inventory_basal_area_treatment import InventoryBasalAreaTreatment
        from ..models.inventory_diameter_treatment import InventoryDiameterTreatment
        from ..models.inventory_modification import InventoryModification
        from ..models.reimputation_method import ReimputationMethod

        d = dict(src_dict)
        source_pim_grid_id = d.pop("source_pim_grid_id")

        source_chm_grid_id = d.pop("source_chm_grid_id")

        _type_ = d.pop("type", UNSET)
        type_: InventoryType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = InventoryType(_type_)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _method = d.pop("method", UNSET)
        method: ReimputationMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = ReimputationMethod.from_dict(_method)

        seed = d.pop("seed", UNSET)

        _point_process = d.pop("point_process", UNSET)
        point_process: PointProcess | Unset
        if isinstance(_point_process, Unset):
            point_process = UNSET
        else:
            point_process = PointProcess(_point_process)

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

        create_pim_chm_fusion_inventory_request = cls(
            source_pim_grid_id=source_pim_grid_id,
            source_chm_grid_id=source_chm_grid_id,
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            method=method,
            seed=seed,
            point_process=point_process,
            modifications=modifications,
            treatments=treatments,
        )

        create_pim_chm_fusion_inventory_request.additional_properties = d
        return create_pim_chm_fusion_inventory_request

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
