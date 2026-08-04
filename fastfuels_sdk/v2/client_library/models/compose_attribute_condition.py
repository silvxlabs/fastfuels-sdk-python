from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.compose_comparison_operator import ComposeComparisonOperator

T = TypeVar("T", bound="ComposeAttributeCondition")


@_attrs_define
class ComposeAttributeCondition:
    """Attribute condition using an alias-qualified input band reference.

    Attributes:
        band (str): Alias-qualified band ref, e.g. `a.fbfm`.
        operator (ComposeComparisonOperator): Comparison operators for compose attribute conditions.
        value (float | int | list[float | int | str] | str):
    """

    band: str
    operator: ComposeComparisonOperator
    value: float | int | list[float | int | str] | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        band = self.band

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "band": band,
                "operator": operator,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        band = d.pop("band")

        operator = ComposeComparisonOperator(d.pop("operator"))

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

        compose_attribute_condition = cls(
            band=band,
            operator=operator,
            value=value,
        )

        compose_attribute_condition.additional_properties = d
        return compose_attribute_condition

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
