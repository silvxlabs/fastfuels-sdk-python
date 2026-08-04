from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Georeference3D")


@_attrs_define
class Georeference3D:
    """Spatial reference for a 3D grid.

    Attributes:
        crs (str): e.g., 'EPSG:32610'
        transform (list[float]): Affine transform [a, b, c, d, e, f]
        shape (list[int]): (z, height, width)
        z_resolution (float):
        z_origin (float):
    """

    crs: str
    transform: list[float]
    shape: list[int]
    z_resolution: float
    z_origin: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        crs = self.crs

        transform = []
        for transform_item_data in self.transform:
            transform_item: float
            transform_item = transform_item_data
            transform.append(transform_item)

        shape = []
        for shape_item_data in self.shape:
            shape_item: int
            shape_item = shape_item_data
            shape.append(shape_item)

        z_resolution = self.z_resolution

        z_origin = self.z_origin

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "crs": crs,
                "transform": transform,
                "shape": shape,
                "z_resolution": z_resolution,
                "z_origin": z_origin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        crs = d.pop("crs")

        transform = []
        _transform = d.pop("transform")
        for transform_item_data in _transform:

            def _parse_transform_item(data: object) -> float:
                return cast(float, data)

            transform_item = _parse_transform_item(transform_item_data)

            transform.append(transform_item)

        shape = []
        _shape = d.pop("shape")
        for shape_item_data in _shape:

            def _parse_shape_item(data: object) -> int:
                return cast(int, data)

            shape_item = _parse_shape_item(shape_item_data)

            shape.append(shape_item)

        z_resolution = d.pop("z_resolution")

        z_origin = d.pop("z_origin")

        georeference_3d = cls(
            crs=crs,
            transform=transform,
            shape=shape,
            z_resolution=z_resolution,
            z_origin=z_origin,
        )

        georeference_3d.additional_properties = d
        return georeference_3d

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
