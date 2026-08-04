from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_model import BaseModel
    from ..models.geo_json_feature_properties_type_0 import (
        GeoJsonFeaturePropertiesType0,
    )
    from ..models.geometry_collection import GeometryCollection
    from ..models.line_string import LineString
    from ..models.multi_line_string import MultiLineString
    from ..models.multi_point import MultiPoint
    from ..models.multi_polygon import MultiPolygon
    from ..models.point import Point
    from ..models.polygon import Polygon


T = TypeVar("T", bound="GeoJsonFeature")


@_attrs_define
class GeoJsonFeature:
    """Generic GeoJSON feature with a generator-safe OpenAPI title.

    Attributes:
        type_ (Literal['Feature']):
        geometry (GeometryCollection | LineString | MultiLineString | MultiPoint | MultiPolygon | None | Point |
            Polygon):
        properties (BaseModel | GeoJsonFeaturePropertiesType0 | None):
        bbox (list[float] | None | Unset):
        id (int | None | str | Unset):
    """

    type_: Literal["Feature"]
    geometry: (
        GeometryCollection
        | LineString
        | MultiLineString
        | MultiPoint
        | MultiPolygon
        | None
        | Point
        | Polygon
    )
    properties: BaseModel | GeoJsonFeaturePropertiesType0 | None
    bbox: list[float] | None | Unset = UNSET
    id: int | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_model import BaseModel
        from ..models.geo_json_feature_properties_type_0 import (
            GeoJsonFeaturePropertiesType0,
        )
        from ..models.geometry_collection import GeometryCollection
        from ..models.line_string import LineString
        from ..models.multi_line_string import MultiLineString
        from ..models.multi_point import MultiPoint
        from ..models.multi_polygon import MultiPolygon
        from ..models.point import Point
        from ..models.polygon import Polygon

        type_ = self.type_

        geometry: dict[str, Any] | None
        if (
            isinstance(self.geometry, Point)
            or isinstance(self.geometry, MultiPoint)
            or isinstance(self.geometry, LineString)
            or isinstance(self.geometry, MultiLineString)
            or isinstance(self.geometry, Polygon)
            or isinstance(self.geometry, MultiPolygon)
            or isinstance(self.geometry, GeometryCollection)
        ):
            geometry = self.geometry.to_dict()
        else:
            geometry = self.geometry

        properties: dict[str, Any] | None
        if isinstance(self.properties, GeoJsonFeaturePropertiesType0) or isinstance(
            self.properties, BaseModel
        ):
            properties = self.properties.to_dict()
        else:
            properties = self.properties

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

        id: int | None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "geometry": geometry,
                "properties": properties,
            }
        )
        if bbox is not UNSET:
            field_dict["bbox"] = bbox
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.base_model import BaseModel
        from ..models.geo_json_feature_properties_type_0 import (
            GeoJsonFeaturePropertiesType0,
        )
        from ..models.geometry_collection import GeometryCollection
        from ..models.line_string import LineString
        from ..models.multi_line_string import MultiLineString
        from ..models.multi_point import MultiPoint
        from ..models.multi_polygon import MultiPolygon
        from ..models.point import Point
        from ..models.polygon import Polygon

        d = dict(src_dict)
        type_ = cast(Literal["Feature"], d.pop("type"))
        if type_ != "Feature":
            raise ValueError(f"type must match const 'Feature', got '{type_}'")

        def _parse_geometry(
            data: object,
        ) -> (
            GeometryCollection
            | LineString
            | MultiLineString
            | MultiPoint
            | MultiPolygon
            | None
            | Point
            | Polygon
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0_type_0 = Point.from_dict(data)

                return geometry_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0_type_1 = MultiPoint.from_dict(data)

                return geometry_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0_type_2 = LineString.from_dict(data)

                return geometry_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0_type_3 = MultiLineString.from_dict(data)

                return geometry_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0_type_4 = Polygon.from_dict(data)

                return geometry_type_0_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0_type_5 = MultiPolygon.from_dict(data)

                return geometry_type_0_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0_type_6 = GeometryCollection.from_dict(data)

                return geometry_type_0_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                GeometryCollection
                | LineString
                | MultiLineString
                | MultiPoint
                | MultiPolygon
                | None
                | Point
                | Polygon,
                data,
            )

        geometry = _parse_geometry(d.pop("geometry"))

        def _parse_properties(
            data: object,
        ) -> BaseModel | GeoJsonFeaturePropertiesType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                properties_type_0 = GeoJsonFeaturePropertiesType0.from_dict(data)

                return properties_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                properties_type_1 = BaseModel.from_dict(data)

                return properties_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BaseModel | GeoJsonFeaturePropertiesType0 | None, data)

        properties = _parse_properties(d.pop("properties"))

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

        def _parse_id(data: object) -> int | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        geo_json_feature = cls(
            type_=type_,
            geometry=geometry,
            properties=properties,
            bbox=bbox,
            id=id,
        )

        geo_json_feature.additional_properties = d
        return geo_json_feature

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
