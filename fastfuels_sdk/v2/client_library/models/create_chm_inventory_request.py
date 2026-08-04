from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inventory_type import InventoryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inventory_basal_area_treatment import InventoryBasalAreaTreatment
    from ..models.inventory_diameter_treatment import InventoryDiameterTreatment
    from ..models.inventory_modification import InventoryModification
    from ..models.stem_isolation_lmf import StemIsolationLmf
    from ..models.stem_isolation_vwf import StemIsolationVwf


T = TypeVar("T", bound="CreateChmInventoryRequest")


@_attrs_define
class CreateChmInventoryRequest:
    """Request body for creating an inventory via CHM extraction.

    Attributes:
        source_chm_grid_id (str): ID of a completed CHM grid to use as the source.
        type_ (InventoryType | Unset): Type of entities in the inventory.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        algorithm (StemIsolationLmf | StemIsolationVwf | Unset): Stem isolation algorithm and its parameters.
        modifications (list[InventoryModification] | Unset): Modifications to apply after stem extraction.
        treatments (list[InventoryBasalAreaTreatment | InventoryDiameterTreatment] | Unset): Silvicultural treatments
            thin against tree diameter, so they require a diameter (`dbh`) column. CHM stem isolation produces only height
            and position (`x`, `y`, `height`), so treatments are not supported here and this must be empty.
    """

    source_chm_grid_id: str
    type_: InventoryType | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    algorithm: StemIsolationLmf | StemIsolationVwf | Unset = UNSET
    modifications: list[InventoryModification] | Unset = UNSET
    treatments: (
        list[InventoryBasalAreaTreatment | InventoryDiameterTreatment] | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_diameter_treatment import InventoryDiameterTreatment
        from ..models.stem_isolation_lmf import StemIsolationLmf

        source_chm_grid_id = self.source_chm_grid_id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        algorithm: dict[str, Any] | Unset
        if isinstance(self.algorithm, Unset):
            algorithm = UNSET
        elif isinstance(self.algorithm, StemIsolationLmf):
            algorithm = self.algorithm.to_dict()
        else:
            algorithm = self.algorithm.to_dict()

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
        if algorithm is not UNSET:
            field_dict["algorithm"] = algorithm
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
        from ..models.stem_isolation_lmf import StemIsolationLmf
        from ..models.stem_isolation_vwf import StemIsolationVwf

        d = dict(src_dict)
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

        def _parse_algorithm(
            data: object,
        ) -> StemIsolationLmf | StemIsolationVwf | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                algorithm_type_0 = StemIsolationLmf.from_dict(data)

                return algorithm_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            algorithm_type_1 = StemIsolationVwf.from_dict(data)

            return algorithm_type_1

        algorithm = _parse_algorithm(d.pop("algorithm", UNSET))

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

        create_chm_inventory_request = cls(
            source_chm_grid_id=source_chm_grid_id,
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            algorithm=algorithm,
            modifications=modifications,
            treatments=treatments,
        )

        create_chm_inventory_request.additional_properties = d
        return create_chm_inventory_request

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
