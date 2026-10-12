from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.crown_radius_estimator import CrownRadiusEstimator
from ..models.crown_segmentation_method import CrownSegmentationMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChmInventoryCrownSegmentation")


@_attrs_define
class ChmInventoryCrownSegmentation:
    """Crown segmentation run after stem isolation. Each tree gets a
    `crown_radius` column measured from its segmented crown.

        Attributes:
            method (CrownSegmentationMethod | Unset):
            min_relative_height (float | Unset): A cell joins a crown only if its CHM height is at least this fraction of
                the treetop cell's height. Provisional default. Default: 0.45.
            min_relative_crown_height (float | Unset): A cell joins a crown only if its CHM height is at least this fraction
                of the crown's current mean height. Provisional default. Default: 0.55.
            max_crown_radius (float | Unset): A cell joins a crown only if its center lies within this distance (m) of the
                treetop cell's center. Provisional default. Default: 10.0.
            radius_estimator (CrownRadiusEstimator | Unset):
    """

    method: CrownSegmentationMethod | Unset = UNSET
    min_relative_height: float | Unset = 0.45
    min_relative_crown_height: float | Unset = 0.55
    max_crown_radius: float | Unset = 10.0
    radius_estimator: CrownRadiusEstimator | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        min_relative_height = self.min_relative_height

        min_relative_crown_height = self.min_relative_crown_height

        max_crown_radius = self.max_crown_radius

        radius_estimator: str | Unset = UNSET
        if not isinstance(self.radius_estimator, Unset):
            radius_estimator = self.radius_estimator.value

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
        if radius_estimator is not UNSET:
            field_dict["radius_estimator"] = radius_estimator

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

        _radius_estimator = d.pop("radius_estimator", UNSET)
        radius_estimator: CrownRadiusEstimator | Unset
        if isinstance(_radius_estimator, Unset):
            radius_estimator = UNSET
        else:
            radius_estimator = CrownRadiusEstimator(_radius_estimator)

        chm_inventory_crown_segmentation = cls(
            method=method,
            min_relative_height=min_relative_height,
            min_relative_crown_height=min_relative_crown_height,
            max_crown_radius=max_crown_radius,
            radius_estimator=radius_estimator,
        )

        chm_inventory_crown_segmentation.additional_properties = d
        return chm_inventory_crown_segmentation

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
