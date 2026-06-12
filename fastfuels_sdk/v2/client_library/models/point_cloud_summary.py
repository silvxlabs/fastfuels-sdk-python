from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PointCloudSummary")


@_attrs_define
class PointCloudSummary:
    """Summary statistics describing the contents of a point cloud.

    Populated by the backend after the cloud is ingested and inspected; it is
    ``null`` while the point cloud is still ``pending`` or ``running``. Use it to
    gauge a cloud's size, density, and composition without downloading it.

        Attributes:
            point_count (int): Total number of points in the cloud.
            point_classes (list[int]): ASPRS standard classification codes present in the cloud, sorted ascending. Common
                codes include `1` (unclassified), `2` (ground), and `3`, `4`, `5` (low, medium, high vegetation).
            density (float): Average point density over the cloud's horizontal extent, in points per square meter.
    """

    point_count: int
    point_classes: list[int]
    density: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        point_count = self.point_count

        point_classes = self.point_classes

        density = self.density

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "point_count": point_count,
                "point_classes": point_classes,
                "density": density,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        point_count = d.pop("point_count")

        point_classes = cast(list[int], d.pop("point_classes"))

        density = d.pop("density")

        point_cloud_summary = cls(
            point_count=point_count,
            point_classes=point_classes,
            density=density,
        )

        point_cloud_summary.additional_properties = d
        return point_cloud_summary

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
