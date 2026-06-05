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

T = TypeVar("T", bound="StemIsolationVwf")


@_attrs_define
class StemIsolationVwf:
    """Parameters for Variable Window Filter (VWF) stem isolation.

    Attributes:
        name (Literal['vwf'] | Unset):  Default: 'vwf'.
        min_height (float | Unset): Minimum height threshold (in CHM units) for a treetop. Default: 2.0.
        spatial_resolution (float | None | Unset): Spatial resolution of the CHM. If omitted, it will be automatically
            inferred from the source grid metadata.
        crown_ratio (float | Unset): Multiplier used to dynamically scale the search window based on pixel height.
            Default: 0.1.
        crown_offset (float | Unset): Constant offset (in meters) added to the dynamic search window. Default: 1.0.
    """

    name: Literal["vwf"] | Unset = "vwf"
    min_height: float | Unset = 2.0
    spatial_resolution: float | None | Unset = UNSET
    crown_ratio: float | Unset = 0.1
    crown_offset: float | Unset = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        min_height = self.min_height

        spatial_resolution: float | None | Unset
        if isinstance(self.spatial_resolution, Unset):
            spatial_resolution = UNSET
        else:
            spatial_resolution = self.spatial_resolution

        crown_ratio = self.crown_ratio

        crown_offset = self.crown_offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if min_height is not UNSET:
            field_dict["min_height"] = min_height
        if spatial_resolution is not UNSET:
            field_dict["spatial_resolution"] = spatial_resolution
        if crown_ratio is not UNSET:
            field_dict["crown_ratio"] = crown_ratio
        if crown_offset is not UNSET:
            field_dict["crown_offset"] = crown_offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = cast(Literal["vwf"] | Unset, d.pop("name", UNSET))
        if name != "vwf" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'vwf', got '{name}'")

        min_height = d.pop("min_height", UNSET)

        def _parse_spatial_resolution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        spatial_resolution = _parse_spatial_resolution(
            d.pop("spatial_resolution", UNSET)
        )

        crown_ratio = d.pop("crown_ratio", UNSET)

        crown_offset = d.pop("crown_offset", UNSET)

        stem_isolation_vwf = cls(
            name=name,
            min_height=min_height,
            spatial_resolution=spatial_resolution,
            crown_ratio=crown_ratio,
            crown_offset=crown_offset,
        )

        stem_isolation_vwf.additional_properties = d
        return stem_isolation_vwf

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
