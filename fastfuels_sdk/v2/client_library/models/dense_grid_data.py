from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DenseGridData")


@_attrs_define
class DenseGridData:
    """
    Attributes:
        format_ (Literal['dense']):
        values (list[float | int]):
    """

    format_: Literal["dense"]
    values: list[float | int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        format_ = self.format_

        values = []
        for values_item_data in self.values:
            values_item: float | int
            values_item = values_item_data
            values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "format": format_,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        format_ = cast(Literal["dense"], d.pop("format"))
        if format_ != "dense":
            raise ValueError(f"format must match const 'dense', got '{format_}'")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:

            def _parse_values_item(data: object) -> float | int:
                return cast(float | int, data)

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        dense_grid_data = cls(
            format_=format_,
            values=values,
        )

        dense_grid_data.additional_properties = d
        return dense_grid_data

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
