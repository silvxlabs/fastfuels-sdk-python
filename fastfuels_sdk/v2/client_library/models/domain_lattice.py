from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DomainLattice")


@_attrs_define
class DomainLattice:
    """Pixel lattice for a domain at a given resolution.

    Uses rasterio conventions:
    - ``transform`` is ``[a, b, c, d, e, f]`` where ``a`` is pixel width,
      ``e`` is ``-pixel_height``, and ``(c, f)`` is the upper-left corner.
    - ``shape`` is ``(height, width)`` in pixels.

        Attributes:
            crs (str): e.g., 'EPSG:32611'
            resolution (float): Pixel size in meters.
            num_buffer_cells (int): Buffer cells applied on each side.
            transform (list[float]): Affine transform [a, b, c, d, e, f]
            shape (list[int]): (height, width) in pixels
    """

    crs: str
    resolution: float
    num_buffer_cells: int
    transform: list[float]
    shape: list[int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        crs = self.crs

        resolution = self.resolution

        num_buffer_cells = self.num_buffer_cells

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "crs": crs,
                "resolution": resolution,
                "num_buffer_cells": num_buffer_cells,
                "transform": transform,
                "shape": shape,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        crs = d.pop("crs")

        resolution = d.pop("resolution")

        num_buffer_cells = d.pop("num_buffer_cells")

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

        domain_lattice = cls(
            crs=crs,
            resolution=resolution,
            num_buffer_cells=num_buffer_cells,
            transform=transform,
            shape=shape,
        )

        domain_lattice.additional_properties = d
        return domain_lattice

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
