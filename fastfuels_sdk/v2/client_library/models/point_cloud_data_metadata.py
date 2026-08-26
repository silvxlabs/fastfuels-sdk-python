from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.point_cloud_data_metadata_columns import PointCloudDataMetadataColumns
    from ..models.point_cloud_tile_metadata import PointCloudTileMetadata


T = TypeVar("T", bound="PointCloudDataMetadata")


@_attrs_define
class PointCloudDataMetadata:
    """Public tile index used to discover and budget point-data requests.

    Attributes:
        tile_m (float): Tile width and height in the horizontal units of `crs`.
        lod_levels (int): Number of cumulative levels of detail. Valid `lod` query values are `0` through `lod_levels -
            1`; omitting `lod` reads the final, complete level.
        crs (str): Coordinate reference system for decoded X/Y coordinates and all reported horizontal bounds.
        bounds (list[float]): Overall horizontal point extent as `[min_x, min_y, max_x, max_y]` in `crs`.
        scales (list[float]): Coordinate scale factors in X/Y/Z order. Decode axis `i` with `stored_integer * scales[i]
            + offsets[i]`.
        offsets (list[float]): Coordinate offsets in X/Y/Z order. Decode axis `i` with `stored_integer * scales[i] +
            offsets[i]`.
        columns (PointCloudDataMetadataColumns): Public stored column names mapped to NumPy-compatible dtypes. Use these
            names in the comma-separated `columns` query parameter. X/Y/Z remain scaled integers on the wire.
        tiles (list[PointCloudTileMetadata]): Occupied tiles sorted by `(tile_x, tile_y)`. Empty positions are omitted;
            only listed tile coordinates are valid data requests.
    """

    tile_m: float
    lod_levels: int
    crs: str
    bounds: list[float]
    scales: list[float]
    offsets: list[float]
    columns: PointCloudDataMetadataColumns
    tiles: list[PointCloudTileMetadata]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tile_m = self.tile_m

        lod_levels = self.lod_levels

        crs = self.crs

        bounds = []
        for bounds_item_data in self.bounds:
            bounds_item: float
            bounds_item = bounds_item_data
            bounds.append(bounds_item)

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

        tiles = []
        for tiles_item_data in self.tiles:
            tiles_item = tiles_item_data.to_dict()
            tiles.append(tiles_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tile_m": tile_m,
                "lod_levels": lod_levels,
                "crs": crs,
                "bounds": bounds,
                "scales": scales,
                "offsets": offsets,
                "columns": columns,
                "tiles": tiles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.point_cloud_data_metadata_columns import (
            PointCloudDataMetadataColumns,
        )
        from ..models.point_cloud_tile_metadata import PointCloudTileMetadata

        d = dict(src_dict)
        tile_m = d.pop("tile_m")

        lod_levels = d.pop("lod_levels")

        crs = d.pop("crs")

        bounds = []
        _bounds = d.pop("bounds")
        for bounds_item_data in _bounds:

            def _parse_bounds_item(data: object) -> float:
                return cast(float, data)

            bounds_item = _parse_bounds_item(bounds_item_data)

            bounds.append(bounds_item)

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

        columns = PointCloudDataMetadataColumns.from_dict(d.pop("columns"))

        tiles = []
        _tiles = d.pop("tiles")
        for tiles_item_data in _tiles:
            tiles_item = PointCloudTileMetadata.from_dict(tiles_item_data)

            tiles.append(tiles_item)

        point_cloud_data_metadata = cls(
            tile_m=tile_m,
            lod_levels=lod_levels,
            crs=crs,
            bounds=bounds,
            scales=scales,
            offsets=offsets,
            columns=columns,
            tiles=tiles,
        )

        point_cloud_data_metadata.additional_properties = d
        return point_cloud_data_metadata

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
