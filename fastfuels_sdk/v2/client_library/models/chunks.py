from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chunks_count_by_axis_type_0 import ChunksCountByAxisType0


T = TypeVar("T", bound="Chunks")


@_attrs_define
class Chunks:
    """Chunk layout for a grid.

    Attributes:
        shape (list[int]): Size of a single chunk. 2D grids: (y, x). 3D grids: (z, y, x). Edge chunks may be smaller.
        count (int | None | Unset): Total number of chunks in the grid.
        count_by_axis (ChunksCountByAxisType0 | None | Unset): Number of chunks along each axis. Keys are 'y','x' for 2D
            grids and 'z','y','x' for 3D grids.
    """

    shape: list[int]
    count: int | None | Unset = UNSET
    count_by_axis: ChunksCountByAxisType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chunks_count_by_axis_type_0 import ChunksCountByAxisType0

        shape: list[int]
        if isinstance(self.shape, list):
            shape = []
            for shape_type_0_item_data in self.shape:
                shape_type_0_item: int
                shape_type_0_item = shape_type_0_item_data
                shape.append(shape_type_0_item)

        count: int | None | Unset
        if isinstance(self.count, Unset):
            count = UNSET
        else:
            count = self.count

        count_by_axis: dict[str, Any] | None | Unset
        if isinstance(self.count_by_axis, Unset):
            count_by_axis = UNSET
        elif isinstance(self.count_by_axis, ChunksCountByAxisType0):
            count_by_axis = self.count_by_axis.to_dict()
        else:
            count_by_axis = self.count_by_axis

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shape": shape,
            }
        )
        if count is not UNSET:
            field_dict["count"] = count
        if count_by_axis is not UNSET:
            field_dict["count_by_axis"] = count_by_axis

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chunks_count_by_axis_type_0 import ChunksCountByAxisType0

        d = dict(src_dict)

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

        def _parse_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        count = _parse_count(d.pop("count", UNSET))

        def _parse_count_by_axis(data: object) -> ChunksCountByAxisType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                count_by_axis_type_0 = ChunksCountByAxisType0.from_dict(data)

                return count_by_axis_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ChunksCountByAxisType0 | None | Unset, data)

        count_by_axis = _parse_count_by_axis(d.pop("count_by_axis", UNSET))

        chunks = cls(
            shape=shape,
            count=count,
            count_by_axis=count_by_axis,
        )

        chunks.additional_properties = d
        return chunks

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
