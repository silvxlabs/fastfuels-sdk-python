from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Resolution3D")


@_attrs_define
class Resolution3D:
    """Voxel resolution for a 3D grid.

    `horizontal` applies to both x and y (fastfuels-core requires isotropic
    horizontal resolution). `vertical` is independent.

        Attributes:
            horizontal (float): Cell size in x and y, meters.
            vertical (float): Cell size in z, meters.
    """

    horizontal: float
    vertical: float

    def to_dict(self) -> dict[str, Any]:
        horizontal = self.horizontal

        vertical = self.vertical

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "horizontal": horizontal,
                "vertical": vertical,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        horizontal = d.pop("horizontal")

        vertical = d.pop("vertical")

        resolution_3d = cls(
            horizontal=horizontal,
            vertical=vertical,
        )

        return resolution_3d
