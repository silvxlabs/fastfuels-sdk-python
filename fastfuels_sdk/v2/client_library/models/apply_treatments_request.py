from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inventory_basal_area_treatment import InventoryBasalAreaTreatment
    from ..models.inventory_diameter_treatment import InventoryDiameterTreatment


T = TypeVar("T", bound="ApplyTreatmentsRequest")


@_attrs_define
class ApplyTreatmentsRequest:
    """Request body for applying treatments to an inventory in place.

    Metadata (name, description, tags) is not accepted here — the inventory
    keeps its identity; use PATCH to edit metadata.

        Attributes:
            treatments (list[InventoryBasalAreaTreatment | InventoryDiameterTreatment]): Treatments to append to this
                inventory and apply to its data.
    """

    treatments: list[InventoryBasalAreaTreatment | InventoryDiameterTreatment]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_diameter_treatment import InventoryDiameterTreatment

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
                "treatments": treatments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inventory_basal_area_treatment import InventoryBasalAreaTreatment
        from ..models.inventory_diameter_treatment import InventoryDiameterTreatment

        d = dict(src_dict)
        treatments = []
        _treatments = d.pop("treatments")
        for treatments_item_data in _treatments:

            def _parse_treatments_item(
                data: object,
            ) -> InventoryBasalAreaTreatment | InventoryDiameterTreatment:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    treatments_item_type_0 = InventoryDiameterTreatment.from_dict(data)

                    return treatments_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                treatments_item_type_1 = InventoryBasalAreaTreatment.from_dict(data)

                return treatments_item_type_1

            treatments_item = _parse_treatments_item(treatments_item_data)

            treatments.append(treatments_item)

        apply_treatments_request = cls(
            treatments=treatments,
        )

        apply_treatments_request.additional_properties = d
        return apply_treatments_request

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
