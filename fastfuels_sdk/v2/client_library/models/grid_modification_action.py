from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.modifier import Modifier

T = TypeVar("T", bound="GridModificationAction")


@_attrs_define
class GridModificationAction:
    """Action to perform when grid modification conditions are met.

    Uses dot-notation band keys (e.g., "fuel_load.1hr", "fbfm").

        Attributes:
            band (str): The band to modify (dot-notation key)
            modifier (Modifier): Modifiers for modification actions.
            value (float | int | str): The value to use with the modifier
    """

    band: str
    modifier: Modifier
    value: float | int | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        band = self.band

        modifier = self.modifier.value

        value: float | int | str
        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "band": band,
                "modifier": modifier,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        band = d.pop("band")

        modifier = Modifier(d.pop("modifier"))

        def _parse_value(data: object) -> float | int | str:
            return cast(float | int | str, data)

        value = _parse_value(d.pop("value"))

        grid_modification_action = cls(
            band=band,
            modifier=modifier,
            value=value,
        )

        grid_modification_action.additional_properties = d
        return grid_modification_action

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
