from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inventory_attribute import InventoryAttribute
from ..models.operator import Operator
from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryModificationCondition")


@_attrs_define
class InventoryModificationCondition:
    """Condition that checks a tree attribute against a value.

    Optionally specify a unit (e.g., "in", "ft") to convert the value
    to the attribute's native unit before comparison.

        Attributes:
            attribute (InventoryAttribute): Attributes available for inventory modifications.
            operator (Operator): Comparison operators for attribute-based conditions.
            value (float | int | list[float | int | str] | str): The value(s) to compare against
            unit (None | str | Unset): Optional pint-compatible unit for the value (e.g., 'in', 'ft', 'mm'). Converted to
                the attribute's native unit before comparison.
    """

    attribute: InventoryAttribute
    operator: Operator
    value: float | int | list[float | int | str] | str
    unit: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute = self.attribute.value

        operator = self.operator.value

        value: float | int | list[float | int | str] | str
        if isinstance(self.value, list):
            value = []
            for value_type_3_item_data in self.value:
                value_type_3_item: float | int | str
                value_type_3_item = value_type_3_item_data
                value.append(value_type_3_item)

        else:
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
                "operator": operator,
                "value": value,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attribute = InventoryAttribute(d.pop("attribute"))

        operator = Operator(d.pop("operator"))

        def _parse_value(data: object) -> float | int | list[float | int | str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = []
                _value_type_3 = data
                for value_type_3_item_data in _value_type_3:

                    def _parse_value_type_3_item(data: object) -> float | int | str:
                        return cast(float | int | str, data)

                    value_type_3_item = _parse_value_type_3_item(value_type_3_item_data)

                    value_type_3.append(value_type_3_item)

                return value_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(float | int | list[float | int | str] | str, data)

        value = _parse_value(d.pop("value"))

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        inventory_modification_condition = cls(
            attribute=attribute,
            operator=operator,
            value=value,
            unit=unit,
        )

        inventory_modification_condition.additional_properties = d
        return inventory_modification_condition

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
