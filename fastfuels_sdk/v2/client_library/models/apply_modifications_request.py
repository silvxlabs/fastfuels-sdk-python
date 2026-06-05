from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inventory_modification import InventoryModification


T = TypeVar("T", bound="ApplyModificationsRequest")


@_attrs_define
class ApplyModificationsRequest:
    """Request body for applying modifications to an inventory in place.

    Metadata (name, description, tags) is not accepted here — the inventory
    keeps its identity; use PATCH to edit metadata.

        Attributes:
            modifications (list[InventoryModification]): Modifications to append to this inventory and apply to its data.
    """

    modifications: list[InventoryModification]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        modifications = []
        for modifications_item_data in self.modifications:
            modifications_item = modifications_item_data.to_dict()
            modifications.append(modifications_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "modifications": modifications,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inventory_modification import InventoryModification

        d = dict(src_dict)
        modifications = []
        _modifications = d.pop("modifications")
        for modifications_item_data in _modifications:
            modifications_item = InventoryModification.from_dict(
                modifications_item_data
            )

            modifications.append(modifications_item)

        apply_modifications_request = cls(
            modifications=modifications,
        )

        apply_modifications_request.additional_properties = d
        return apply_modifications_request

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
