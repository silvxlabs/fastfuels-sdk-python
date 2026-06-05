from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.uniform_band import UniformBand

T = TypeVar("T", bound="UniformBandInput")


@_attrs_define
class UniformBandInput:
    """A single band specification for a uniform grid.

    Users provide a band key (from the predefined list) and a constant value.
    The API resolves the key to unit and type.

        Attributes:
            key (UniformBand): Predefined bands available for uniform grids.
            value (float | int):
    """

    key: UniformBand
    value: float | int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key.value

        value: float | int
        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = UniformBand(d.pop("key"))

        def _parse_value(data: object) -> float | int:
            return cast(float | int, data)

        value = _parse_value(d.pop("value"))

        uniform_band_input = cls(
            key=key,
            value=value,
        )

        uniform_band_input.additional_properties = d
        return uniform_band_input

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
