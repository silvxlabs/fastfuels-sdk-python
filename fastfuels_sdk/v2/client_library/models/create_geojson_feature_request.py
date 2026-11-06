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
    from ..models.geojson_crs import GeojsonCrs
    from ..models.geojson_polygon_feature import GeojsonPolygonFeature


T = TypeVar("T", bound="CreateGeojsonFeatureRequest")


@_attrs_define
class CreateGeojsonFeatureRequest:
    """Request body for uploading a road, water or building feature.

    The body **is** the GeoJSON FeatureCollection, as for ``POST /domains`` and
    layerset uploads, extended with the resource-metadata fields. ``name``
    overrides the optional GeoJSON ``name`` member and is the resource name.

        Attributes:
            type_ (Literal['FeatureCollection']):
            features (list[GeojsonPolygonFeature]):
            bbox (list[float] | None | Unset):
            crs (GeojsonCrs | None | Unset):
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            extent_buffer_m (float | Unset): Distance in meters to expand the domain extent outward before clipping the
                uploaded polygons. Default 0 clips exactly to the domain boundary. Maximum: 100 meters. Default: 0.0.
    """

    type_: Literal["FeatureCollection"]
    features: list[GeojsonPolygonFeature]
    bbox: list[float] | None | Unset = UNSET
    crs: GeojsonCrs | None | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    extent_buffer_m: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.geojson_crs import GeojsonCrs

        type_ = self.type_

        features = []
        for features_item_data in self.features:
            features_item = features_item_data.to_dict()
            features.append(features_item)

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

        crs: dict[str, Any] | None | Unset
        if isinstance(self.crs, Unset):
            crs = UNSET
        elif isinstance(self.crs, GeojsonCrs):
            crs = self.crs.to_dict()
        else:
            crs = self.crs

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        extent_buffer_m = self.extent_buffer_m

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "features": features,
            }
        )
        if bbox is not UNSET:
            field_dict["bbox"] = bbox
        if crs is not UNSET:
            field_dict["crs"] = crs
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if extent_buffer_m is not UNSET:
            field_dict["extent_buffer_m"] = extent_buffer_m

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.geojson_crs import GeojsonCrs
        from ..models.geojson_polygon_feature import GeojsonPolygonFeature

        d = dict(src_dict)
        type_ = cast(Literal["FeatureCollection"], d.pop("type"))
        if type_ != "FeatureCollection":
            raise ValueError(
                f"type must match const 'FeatureCollection', got '{type_}'"
            )

        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = GeojsonPolygonFeature.from_dict(features_item_data)

            features.append(features_item)

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

        def _parse_crs(data: object) -> GeojsonCrs | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crs_type_0 = GeojsonCrs.from_dict(data)

                return crs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(GeojsonCrs | None | Unset, data)

        crs = _parse_crs(d.pop("crs", UNSET))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        extent_buffer_m = d.pop("extent_buffer_m", UNSET)

        create_geojson_feature_request = cls(
            type_=type_,
            features=features,
            bbox=bbox,
            crs=crs,
            name=name,
            description=description,
            tags=tags,
            extent_buffer_m=extent_buffer_m,
        )

        create_geojson_feature_request.additional_properties = d
        return create_geojson_feature_request

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
