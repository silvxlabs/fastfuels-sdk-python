from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InventoryGeoreference")


@_attrs_define
class InventoryGeoreference:
    """Spatial reference for an inventory, computed from the domain geometry.

    Attributes:
        crs (str):
        bounds (list[float]):
    """

    crs: str
    bounds: list[float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        crs = self.crs

        bounds = []
        for bounds_item_data in self.bounds:
            bounds_item: float
            bounds_item = bounds_item_data
            bounds.append(bounds_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "crs": crs,
                "bounds": bounds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        crs = d.pop("crs")

        bounds = []
        _bounds = d.pop("bounds")
        for bounds_item_data in _bounds:

            def _parse_bounds_item(data: object) -> float:
                return cast(float, data)

            bounds_item = _parse_bounds_item(bounds_item_data)

            bounds.append(bounds_item)

        inventory_georeference = cls(
            crs=crs,
            bounds=bounds,
        )

        inventory_georeference.additional_properties = d
        return inventory_georeference

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
