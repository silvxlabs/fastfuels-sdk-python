from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.line_string import LineString
    from ..models.multi_line_string import MultiLineString
    from ..models.multi_point import MultiPoint
    from ..models.multi_polygon import MultiPolygon
    from ..models.point import Point
    from ..models.polygon import Polygon


T = TypeVar("T", bound="GeometryCollection")


@_attrs_define
class GeometryCollection:
    """GeometryCollection Model

    Attributes:
        type_ (Literal['GeometryCollection']):
        geometries (list[GeometryCollection | LineString | MultiLineString | MultiPoint | MultiPolygon | Point |
            Polygon]):
        bbox (list[float] | None | Unset):
    """

    type_: Literal["GeometryCollection"]
    geometries: list[
        GeometryCollection
        | LineString
        | MultiLineString
        | MultiPoint
        | MultiPolygon
        | Point
        | Polygon
    ]
    bbox: list[float] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.line_string import LineString
        from ..models.multi_line_string import MultiLineString
        from ..models.multi_point import MultiPoint
        from ..models.multi_polygon import MultiPolygon
        from ..models.point import Point
        from ..models.polygon import Polygon

        type_ = self.type_

        geometries = []
        for geometries_item_data in self.geometries:
            geometries_item: dict[str, Any]
            if isinstance(geometries_item_data, Point):
                geometries_item = geometries_item_data.to_dict()
            elif isinstance(geometries_item_data, MultiPoint):
                geometries_item = geometries_item_data.to_dict()
            elif isinstance(geometries_item_data, LineString):
                geometries_item = geometries_item_data.to_dict()
            elif isinstance(geometries_item_data, MultiLineString):
                geometries_item = geometries_item_data.to_dict()
            elif isinstance(geometries_item_data, Polygon):
                geometries_item = geometries_item_data.to_dict()
            elif isinstance(geometries_item_data, MultiPolygon):
                geometries_item = geometries_item_data.to_dict()
            else:
                geometries_item = geometries_item_data.to_dict()

            geometries.append(geometries_item)

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
                "geometries": geometries,
            }
        )
        if bbox is not UNSET:
            field_dict["bbox"] = bbox

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_string import LineString
        from ..models.multi_line_string import MultiLineString
        from ..models.multi_point import MultiPoint
        from ..models.multi_polygon import MultiPolygon
        from ..models.point import Point
        from ..models.polygon import Polygon

        d = dict(src_dict)
        type_ = cast(Literal["GeometryCollection"], d.pop("type"))
        if type_ != "GeometryCollection":
            raise ValueError(
                f"type must match const 'GeometryCollection', got '{type_}'"
            )

        geometries = []
        _geometries = d.pop("geometries")
        for geometries_item_data in _geometries:

            def _parse_geometries_item(
                data: object,
            ) -> (
                GeometryCollection
                | LineString
                | MultiLineString
                | MultiPoint
                | MultiPolygon
                | Point
                | Polygon
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    geometries_item_type_0 = Point.from_dict(data)

                    return geometries_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    geometries_item_type_1 = MultiPoint.from_dict(data)

                    return geometries_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    geometries_item_type_2 = LineString.from_dict(data)

                    return geometries_item_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    geometries_item_type_3 = MultiLineString.from_dict(data)

                    return geometries_item_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    geometries_item_type_4 = Polygon.from_dict(data)

                    return geometries_item_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    geometries_item_type_5 = MultiPolygon.from_dict(data)

                    return geometries_item_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                geometries_item_type_6 = GeometryCollection.from_dict(data)

                return geometries_item_type_6

            geometries_item = _parse_geometries_item(geometries_item_data)

            geometries.append(geometries_item)

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

        geometry_collection = cls(
            type_=type_,
            geometries=geometries,
            bbox=bbox,
        )

        geometry_collection.additional_properties = d
        return geometry_collection

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
