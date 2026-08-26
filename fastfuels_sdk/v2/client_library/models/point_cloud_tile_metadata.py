from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PointCloudTileMetadata")


@_attrs_define
class PointCloudTileMetadata:
    """Location and cumulative LOD costs for one occupied point-cloud tile.

    Attributes:
        tile_x (int): Horizontal tile index. Pass this value as `tile_x` to a point-cloud data endpoint. Negative
            indices are valid for boundary points that fall just west of the tiling origin.
        tile_y (int): Vertical tile index. Pass this value as `tile_y` to a point-cloud data endpoint. Negative indices
            are valid.
        bounds (list[float]): Horizontal tile bounds as `[min_x, min_y, max_x, max_y]` in the metadata response's `crs`.
            A boundary tile can extend beyond the point cloud's overall bounds.
        points_by_lod (list[int]): Cumulative point counts by LOD. Element `k` is the exact number of rows returned by
            `lod=k` before optional classification filtering. Counts never decrease; the final value is the complete tile.
            Repeated values are valid for sparse tiles.
    """

    tile_x: int
    tile_y: int
    bounds: list[float]
    points_by_lod: list[int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tile_x = self.tile_x

        tile_y = self.tile_y

        bounds = []
        for bounds_item_data in self.bounds:
            bounds_item: float
            bounds_item = bounds_item_data
            bounds.append(bounds_item)

        points_by_lod = self.points_by_lod

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tile_x": tile_x,
                "tile_y": tile_y,
                "bounds": bounds,
                "points_by_lod": points_by_lod,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        tile_x = d.pop("tile_x")

        tile_y = d.pop("tile_y")

        bounds = []
        _bounds = d.pop("bounds")
        for bounds_item_data in _bounds:

            def _parse_bounds_item(data: object) -> float:
                return cast(float, data)

            bounds_item = _parse_bounds_item(bounds_item_data)

            bounds.append(bounds_item)

        points_by_lod = cast(list[int], d.pop("points_by_lod"))

        point_cloud_tile_metadata = cls(
            tile_x=tile_x,
            tile_y=tile_y,
            bounds=bounds,
            points_by_lod=points_by_lod,
        )

        point_cloud_tile_metadata.additional_properties = d
        return point_cloud_tile_metadata

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
