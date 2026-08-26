from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.point_cloud_tile_data_response_columns import (
        PointCloudTileDataResponseColumns,
    )
    from ..models.point_cloud_tile_data_response_data import (
        PointCloudTileDataResponseData,
    )


T = TypeVar("T", bound="PointCloudTileDataResponse")


@_attrs_define
class PointCloudTileDataResponse:
    """Columnar JSON values for one point-cloud tile selection.

    Attributes:
        tile_x (int): Requested horizontal tile index.
        tile_y (int): Requested vertical tile index.
        bounds (list[float]): Horizontal tile bounds as `[min_x, min_y, max_x, max_y]` in the point cloud's CRS.
        lod (int): Inclusive LOD ceiling used for this response. The response contains stored levels `0` through this
            value.
        classes (list[int] | None): Sorted ASPRS classes retained by the request, or null when no classification filter
            was applied.
        scales (list[float]): Coordinate scales in X/Y/Z order. Decode coordinate axis `i` with `stored_integer *
            scales[i] + offsets[i]`.
        offsets (list[float]): Coordinate offsets in X/Y/Z order.
        columns (PointCloudTileDataResponseColumns): Returned column names mapped to their NumPy-compatible dtypes. Only
            requested columns are present.
        data (PointCloudTileDataResponseData): Columnar point values. Every array has equal length, and values at the
            same array index describe the same point. X/Y/Z values are stored integers decoded with `scales` and `offsets`.
    """

    tile_x: int
    tile_y: int
    bounds: list[float]
    lod: int
    classes: list[int] | None
    scales: list[float]
    offsets: list[float]
    columns: PointCloudTileDataResponseColumns
    data: PointCloudTileDataResponseData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tile_x = self.tile_x

        tile_y = self.tile_y

        bounds = []
        for bounds_item_data in self.bounds:
            bounds_item: float
            bounds_item = bounds_item_data
            bounds.append(bounds_item)

        lod = self.lod

        classes: list[int] | None
        if isinstance(self.classes, list):
            classes = self.classes

        else:
            classes = self.classes

        scales = []
        for scales_item_data in self.scales:
            scales_item: float
            scales_item = scales_item_data
            scales.append(scales_item)

        offsets = []
        for offsets_item_data in self.offsets:
            offsets_item: float
            offsets_item = offsets_item_data
            offsets.append(offsets_item)

        columns = self.columns.to_dict()

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tile_x": tile_x,
                "tile_y": tile_y,
                "bounds": bounds,
                "lod": lod,
                "classes": classes,
                "scales": scales,
                "offsets": offsets,
                "columns": columns,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.point_cloud_tile_data_response_columns import (
            PointCloudTileDataResponseColumns,
        )
        from ..models.point_cloud_tile_data_response_data import (
            PointCloudTileDataResponseData,
        )

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

        lod = d.pop("lod")

        def _parse_classes(data: object) -> list[int] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                classes_type_0 = cast(list[int], data)

                return classes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[int] | None, data)

        classes = _parse_classes(d.pop("classes"))

        scales = []
        _scales = d.pop("scales")
        for scales_item_data in _scales:

            def _parse_scales_item(data: object) -> float:
                return cast(float, data)

            scales_item = _parse_scales_item(scales_item_data)

            scales.append(scales_item)

        offsets = []
        _offsets = d.pop("offsets")
        for offsets_item_data in _offsets:

            def _parse_offsets_item(data: object) -> float:
                return cast(float, data)

            offsets_item = _parse_offsets_item(offsets_item_data)

            offsets.append(offsets_item)

        columns = PointCloudTileDataResponseColumns.from_dict(d.pop("columns"))

        data = PointCloudTileDataResponseData.from_dict(d.pop("data"))

        point_cloud_tile_data_response = cls(
            tile_x=tile_x,
            tile_y=tile_y,
            bounds=bounds,
            lod=lod,
            classes=classes,
            scales=scales,
            offsets=offsets,
            columns=columns,
            data=data,
        )

        point_cloud_tile_data_response.additional_properties = d
        return point_cloud_tile_data_response

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
