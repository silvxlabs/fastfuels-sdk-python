from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LineString")


@_attrs_define
class LineString:
    """LineString Model

    Attributes:
        type_ (Literal['LineString']):
        coordinates (list[list[float]]):
        bbox (list[float] | None | Unset):
    """

    type_: Literal["LineString"]
    coordinates: list[list[float]]
    bbox: list[float] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        coordinates = []
        for coordinates_item_data in self.coordinates:
            coordinates_item: list[float]
            if isinstance(coordinates_item_data, list):
                coordinates_item = []
                for componentsschemas_position_2d_item_data in coordinates_item_data:
                    componentsschemas_position_2d_item: float
                    componentsschemas_position_2d_item = (
                        componentsschemas_position_2d_item_data
                    )
                    coordinates_item.append(componentsschemas_position_2d_item)

            coordinates.append(coordinates_item)

        bbox: list[float] | None | Unset
        if isinstance(self.bbox, Unset):
            bbox = UNSET
        elif isinstance(self.bbox, list):
            bbox = []
            for bbox_type_0_item_data in self.bbox:
                bbox_type_0_item: float
                bbox_type_0_item = bbox_type_0_item_data
                bbox.append(bbox_type_0_item)

        else:
            bbox = self.bbox

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "coordinates": coordinates,
            }
        )
        if bbox is not UNSET:
            field_dict["bbox"] = bbox

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = cast(Literal["LineString"], d.pop("type"))
        if type_ != "LineString":
            raise ValueError(f"type must match const 'LineString', got '{type_}'")

        coordinates = []
        _coordinates = d.pop("coordinates")
        for coordinates_item_data in _coordinates:

            def _parse_coordinates_item(data: object) -> list[float]:
                if not isinstance(data, list):
                    raise TypeError()
                coordinates_item_type_0 = []
                _coordinates_item_type_0 = data
                for componentsschemas_position_2d_item_data in _coordinates_item_type_0:

                    def _parse_componentsschemas_position_2d_item(
                        data: object,
                    ) -> float:
                        return cast(float, data)

                    componentsschemas_position_2d_item = (
                        _parse_componentsschemas_position_2d_item(
                            componentsschemas_position_2d_item_data
                        )
                    )

                    coordinates_item_type_0.append(componentsschemas_position_2d_item)

                return coordinates_item_type_0

            coordinates_item = _parse_coordinates_item(coordinates_item_data)

            coordinates.append(coordinates_item)

        def _parse_bbox(data: object) -> list[float] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                bbox_type_0 = []
                _bbox_type_0 = data
                for bbox_type_0_item_data in _bbox_type_0:

                    def _parse_bbox_type_0_item(data: object) -> float:
                        return cast(float, data)

                    bbox_type_0_item = _parse_bbox_type_0_item(bbox_type_0_item_data)

                    bbox_type_0.append(bbox_type_0_item)

                return bbox_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[float] | None | Unset, data)

        bbox = _parse_bbox(d.pop("bbox", UNSET))

        line_string = cls(
            type_=type_,
            coordinates=coordinates,
            bbox=bbox,
        )

        line_string.additional_properties = d
        return line_string

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
