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
    from ..models.geojson_polygon_feature_properties_type_0 import (
        GeojsonPolygonFeaturePropertiesType0,
    )
    from ..models.multi_polygon import MultiPolygon
    from ..models.polygon import Polygon


T = TypeVar("T", bound="GeojsonPolygonFeature")


@_attrs_define
class GeojsonPolygonFeature:
    """One uploaded polygon. Its ``properties`` are stored as columns.

    Attributes:
        type_ (Literal['Feature']):
        geometry (MultiPolygon | Polygon):
        properties (GeojsonPolygonFeaturePropertiesType0 | None):
        bbox (list[float] | None | Unset):
        id (int | None | str | Unset):
    """

    type_: Literal["Feature"]
    geometry: MultiPolygon | Polygon
    properties: GeojsonPolygonFeaturePropertiesType0 | None
    bbox: list[float] | None | Unset = UNSET
    id: int | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.geojson_polygon_feature_properties_type_0 import (
            GeojsonPolygonFeaturePropertiesType0,
        )
        from ..models.polygon import Polygon

        type_ = self.type_

        geometry: dict[str, Any]
        if isinstance(self.geometry, Polygon):
            geometry = self.geometry.to_dict()
        else:
            geometry = self.geometry.to_dict()

        properties: dict[str, Any] | None
        if isinstance(self.properties, GeojsonPolygonFeaturePropertiesType0):
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
        from ..models.geojson_polygon_feature_properties_type_0 import (
            GeojsonPolygonFeaturePropertiesType0,
        )
        from ..models.multi_polygon import MultiPolygon
        from ..models.polygon import Polygon

        d = dict(src_dict)
        type_ = cast(Literal["Feature"], d.pop("type"))
        if type_ != "Feature":
            raise ValueError(f"type must match const 'Feature', got '{type_}'")

        def _parse_geometry(data: object) -> MultiPolygon | Polygon:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0 = Polygon.from_dict(data)

                return geometry_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            geometry_type_1 = MultiPolygon.from_dict(data)

            return geometry_type_1

        geometry = _parse_geometry(d.pop("geometry"))

        def _parse_properties(
            data: object,
        ) -> GeojsonPolygonFeaturePropertiesType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                properties_type_0 = GeojsonPolygonFeaturePropertiesType0.from_dict(data)

                return properties_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(GeojsonPolygonFeaturePropertiesType0 | None, data)

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

        geojson_polygon_feature = cls(
            type_=type_,
            geometry=geometry,
            properties=properties,
            bbox=bbox,
            id=id,
        )

        geojson_polygon_feature.additional_properties = d
        return geojson_polygon_feature

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
