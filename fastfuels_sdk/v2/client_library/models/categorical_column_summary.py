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

T = TypeVar("T", bound="CategoricalColumnSummary")


@_attrs_define
class CategoricalColumnSummary:
    """
    Attributes:
        type_ (Literal['categorical']):
        count (int):
        null_count (int):
        unique_count (int):
    """

    type_: Literal["categorical"]
    count: int
    null_count: int
    unique_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        count = self.count

        null_count = self.null_count

        unique_count = self.unique_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "count": count,
                "null_count": null_count,
                "unique_count": unique_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = cast(Literal["categorical"], d.pop("type"))
        if type_ != "categorical":
            raise ValueError(f"type must match const 'categorical', got '{type_}'")

        count = d.pop("count")

        null_count = d.pop("null_count")

        unique_count = d.pop("unique_count")

        categorical_column_summary = cls(
            type_=type_,
            count=count,
            null_count=null_count,
            unique_count=unique_count,
        )

        categorical_column_summary.additional_properties = d
        return categorical_column_summary

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
