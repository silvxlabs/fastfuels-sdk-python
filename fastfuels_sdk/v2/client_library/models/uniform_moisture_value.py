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

T = TypeVar("T", bound="UniformMoistureValue")


@_attrs_define
class UniformMoistureValue:
    """Uniform fuel moisture for one fuel state.

    Attributes:
        method (Literal['uniform'] | Unset):  Default: 'uniform'.
        value (float | Unset): Fuel moisture content (%), applied uniformly. Default: 100.0.
    """

    method: Literal["uniform"] | Unset = "uniform"
    value: float | Unset = 100.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["uniform"] | Unset, d.pop("method", UNSET))
        if method != "uniform" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'uniform', got '{method}'")

        value = d.pop("value", UNSET)

        uniform_moisture_value = cls(
            method=method,
            value=value,
        )

        uniform_moisture_value.additional_properties = d
        return uniform_moisture_value

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
