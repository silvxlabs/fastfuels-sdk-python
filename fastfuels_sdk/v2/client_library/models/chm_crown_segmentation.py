from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.crown_segmentation_method import CrownSegmentationMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChmCrownSegmentation")


@_attrs_define
class ChmCrownSegmentation:
    """Crown segmentation settings for a crown Feature.

    When set, ``max_height`` must be greater than ``min_height``.

        Attributes:
            method (CrownSegmentationMethod | Unset):
            min_relative_height (float | Unset): A cell joins a crown only if its CHM height is at least this fraction of
                the treetop cell's height. Provisional default. Default: 0.45.
            min_relative_crown_height (float | Unset): A cell joins a crown only if its CHM height is at least this fraction
                of the crown's current mean height. Provisional default. Default: 0.55.
            max_crown_radius (float | Unset): A cell joins a crown only if its center lies within this distance (m) of the
                treetop cell's center. Provisional default. Default: 10.0.
            min_height (float | Unset): A cell joins a crown only if its CHM height is at least this (m). Default: 2.0.
            max_height (float | None | Unset): A cell joins a crown only if its CHM height is at most this (m). Set to null
                for no ceiling. Default: 120.0.
    """

    method: CrownSegmentationMethod | Unset = UNSET
    min_relative_height: float | Unset = 0.45
    min_relative_crown_height: float | Unset = 0.55
    max_crown_radius: float | Unset = 10.0
    min_height: float | Unset = 2.0
    max_height: float | None | Unset = 120.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        min_relative_height = self.min_relative_height

        min_relative_crown_height = self.min_relative_crown_height

        max_crown_radius = self.max_crown_radius

        min_height = self.min_height

        max_height: float | None | Unset
        if isinstance(self.max_height, Unset):
            max_height = UNSET
        else:
            max_height = self.max_height

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if min_relative_height is not UNSET:
            field_dict["min_relative_height"] = min_relative_height
        if min_relative_crown_height is not UNSET:
            field_dict["min_relative_crown_height"] = min_relative_crown_height
        if max_crown_radius is not UNSET:
            field_dict["max_crown_radius"] = max_crown_radius
        if min_height is not UNSET:
            field_dict["min_height"] = min_height
        if max_height is not UNSET:
            field_dict["max_height"] = max_height

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _method = d.pop("method", UNSET)
        method: CrownSegmentationMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = CrownSegmentationMethod(_method)

        min_relative_height = d.pop("min_relative_height", UNSET)

        min_relative_crown_height = d.pop("min_relative_crown_height", UNSET)

        max_crown_radius = d.pop("max_crown_radius", UNSET)

        min_height = d.pop("min_height", UNSET)

        def _parse_max_height(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_height = _parse_max_height(d.pop("max_height", UNSET))

        chm_crown_segmentation = cls(
            method=method,
            min_relative_height=min_relative_height,
            min_relative_crown_height=min_relative_crown_height,
            max_crown_radius=max_crown_radius,
            min_height=min_height,
            max_height=max_height,
        )

        chm_crown_segmentation.additional_properties = d
        return chm_crown_segmentation

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
