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

from ..types import UNSET, Unset

T = TypeVar("T", bound="StemIsolationLmf")


@_attrs_define
class StemIsolationLmf:
    """Parameters for Local Maximum Filter (LMF) stem isolation.

    Attributes:
        name (Literal['lmf'] | Unset):  Default: 'lmf'.
        min_height (float | Unset): Minimum height threshold (in CHM units) for a treetop. Default: 2.0.
        footprint_size (int | Unset): Diameter of the circular footprint in pixels. Must be an odd integer. Default: 3.
    """

    name: Literal["lmf"] | Unset = "lmf"
    min_height: float | Unset = 2.0
    footprint_size: int | Unset = 3
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        min_height = self.min_height

        footprint_size = self.footprint_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if min_height is not UNSET:
            field_dict["min_height"] = min_height
        if footprint_size is not UNSET:
            field_dict["footprint_size"] = footprint_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = cast(Literal["lmf"] | Unset, d.pop("name", UNSET))
        if name != "lmf" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'lmf', got '{name}'")

        min_height = d.pop("min_height", UNSET)

        footprint_size = d.pop("footprint_size", UNSET)

        stem_isolation_lmf = cls(
            name=name,
            min_height=min_height,
            footprint_size=footprint_size,
        )

        stem_isolation_lmf.additional_properties = d
        return stem_isolation_lmf

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
