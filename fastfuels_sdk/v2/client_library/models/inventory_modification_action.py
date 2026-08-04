from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inventory_attribute import InventoryAttribute
from ..models.modifier import Modifier
from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryModificationAction")


@_attrs_define
class InventoryModificationAction:
    """Action that modifies a tree attribute value.

    Optionally specify a unit to convert the value to the attribute's
    native unit before applying the modifier.

        Attributes:
            attribute (InventoryAttribute): Attributes available for inventory modifications.
            modifier (Modifier): Modifiers for modification actions.
            value (float | int | str): The value to use with the modifier
            unit (None | str | Unset): Optional pint-compatible unit for the value.
    """

    attribute: InventoryAttribute
    modifier: Modifier
    value: float | int | str
    unit: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute = self.attribute.value

        modifier = self.modifier.value

        value: float | int | str
        value = self.value

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attribute": attribute,
                "modifier": modifier,
                "value": value,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        attribute = InventoryAttribute(d.pop("attribute"))

        modifier = Modifier(d.pop("modifier"))

        def _parse_value(data: object) -> float | int | str:
            return cast(float | int | str, data)

        value = _parse_value(d.pop("value"))

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        inventory_modification_action = cls(
            attribute=attribute,
            modifier=modifier,
            value=value,
            unit=unit,
        )

        inventory_modification_action.additional_properties = d
        return inventory_modification_action

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
