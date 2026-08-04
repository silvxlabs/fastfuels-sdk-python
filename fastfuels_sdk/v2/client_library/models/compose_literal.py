from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComposeLiteral")


@_attrs_define
class ComposeLiteral:
    """Typed literal value for compose operands and fallback values.

    Attributes:
        value (float | int | str):
        type_ (Literal['literal'] | Unset):  Default: 'literal'.
        unit (None | str | Unset): Canonical unit for numeric values. Must be null for string literals.
    """

    value: float | int | str
    type_: Literal["literal"] | Unset = "literal"
    unit: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value: float | int | str
        value = self.value

        type_ = self.type_

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_value(data: object) -> float | int | str:
            return cast(float | int | str, data)

        value = _parse_value(d.pop("value"))

        type_ = cast(Literal["literal"] | Unset, d.pop("type", UNSET))
        if type_ != "literal" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'literal', got '{type_}'")

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        compose_literal = cls(
            value=value,
            type_=type_,
            unit=unit,
        )

        compose_literal.additional_properties = d
        return compose_literal

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
