from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PointCloudGeoreference")


@_attrs_define
class PointCloudGeoreference:
    """The coordinate reference system and 3D extent of a point cloud.

    Populated by the backend after the cloud is ingested and inspected; it is
    ``null`` while the point cloud is still ``pending`` or ``running``.

        Attributes:
            crs (str): Coordinate reference system the points are stored in, as an authority code (e.g. `EPSG:32613`). This
                is always the domain's CRS: uploads in a different CRS are reprojected during ingestion. Only horizontal
                coordinates are transformed — elevations are stored exactly as the source provided them and are never converted
                between reference surfaces.
            bounds (list[float]): Axis-aligned 3D bounding box of every point, given as `[min_x, min_y, min_z, max_x, max_y,
                max_z]` in the units of `crs`. Point clouds are three-dimensional, so the box includes a vertical (z) extent.
                Use it to check coverage against a domain before deriving products from the cloud.
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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        crs = d.pop("crs")

        bounds = []
        _bounds = d.pop("bounds")
        for bounds_item_data in _bounds:

            def _parse_bounds_item(data: object) -> float:
                return cast(float, data)

            bounds_item = _parse_bounds_item(bounds_item_data)

            bounds.append(bounds_item)

        point_cloud_georeference = cls(
            crs=crs,
            bounds=bounds,
        )

        point_cloud_georeference.additional_properties = d
        return point_cloud_georeference

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
