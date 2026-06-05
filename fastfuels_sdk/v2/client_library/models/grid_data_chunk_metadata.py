from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GridDataChunkMetadata")


@_attrs_define
class GridDataChunkMetadata:
    """
    Attributes:
        index (int):
        shape (list[int]):
        offset (list[int]):
        transform (list[float]):
        z_origin (float | None | Unset):
        z_resolution (float | None | Unset):
    """

    index: int
    shape: list[int]
    offset: list[int]
    transform: list[float]
    z_origin: float | None | Unset = UNSET
    z_resolution: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        shape: list[int]
        if isinstance(self.shape, list):
            shape = []
            for shape_type_0_item_data in self.shape:
                shape_type_0_item: int
                shape_type_0_item = shape_type_0_item_data
                shape.append(shape_type_0_item)

        offset: list[int]
        if isinstance(self.offset, list):
            offset = []
            for offset_type_0_item_data in self.offset:
                offset_type_0_item: int
                offset_type_0_item = offset_type_0_item_data
                offset.append(offset_type_0_item)

        transform = []
        for transform_item_data in self.transform:
            transform_item: float
            transform_item = transform_item_data
            transform.append(transform_item)

        z_origin: float | None | Unset
        if isinstance(self.z_origin, Unset):
            z_origin = UNSET
        else:
            z_origin = self.z_origin

        z_resolution: float | None | Unset
        if isinstance(self.z_resolution, Unset):
            z_resolution = UNSET
        else:
            z_resolution = self.z_resolution

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index": index,
                "shape": shape,
                "offset": offset,
                "transform": transform,
            }
        )
        if z_origin is not UNSET:
            field_dict["z_origin"] = z_origin
        if z_resolution is not UNSET:
            field_dict["z_resolution"] = z_resolution

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        index = d.pop("index")

        def _parse_shape(data: object) -> list[int]:
            if not isinstance(data, list):
                raise TypeError()
            shape_type_0 = []
            _shape_type_0 = data
            for shape_type_0_item_data in _shape_type_0:

                def _parse_shape_type_0_item(data: object) -> int:
                    return cast(int, data)

                shape_type_0_item = _parse_shape_type_0_item(shape_type_0_item_data)

                shape_type_0.append(shape_type_0_item)

            return shape_type_0

        shape = _parse_shape(d.pop("shape"))

        def _parse_offset(data: object) -> list[int]:
            if not isinstance(data, list):
                raise TypeError()
            offset_type_0 = []
            _offset_type_0 = data
            for offset_type_0_item_data in _offset_type_0:

                def _parse_offset_type_0_item(data: object) -> int:
                    return cast(int, data)

                offset_type_0_item = _parse_offset_type_0_item(offset_type_0_item_data)

                offset_type_0.append(offset_type_0_item)

            return offset_type_0

        offset = _parse_offset(d.pop("offset"))

        transform = []
        _transform = d.pop("transform")
        for transform_item_data in _transform:

            def _parse_transform_item(data: object) -> float:
                return cast(float, data)

            transform_item = _parse_transform_item(transform_item_data)

            transform.append(transform_item)

        def _parse_z_origin(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        z_origin = _parse_z_origin(d.pop("z_origin", UNSET))

        def _parse_z_resolution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        z_resolution = _parse_z_resolution(d.pop("z_resolution", UNSET))

        grid_data_chunk_metadata = cls(
            index=index,
            shape=shape,
            offset=offset,
            transform=transform,
            z_origin=z_origin,
            z_resolution=z_resolution,
        )

        grid_data_chunk_metadata.additional_properties = d
        return grid_data_chunk_metadata

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
