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
    from ..models.domain_style import DomainStyle
    from ..models.geo_json_crs import GeoJsonCRS
    from ..models.geo_json_feature import GeoJsonFeature


T = TypeVar("T", bound="GeoJsonFeatureCollection")


@_attrs_define
class GeoJsonFeatureCollection:
    """
    Attributes:
        type_ (Literal['FeatureCollection']):
        features (list[GeoJsonFeature]):
        bbox (list[float] | None | Unset):
        name (str | Unset): The name of the domain. Default: ''.
        description (str | Unset): A description of the domain. Default: ''.
        crs (GeoJsonCRS | Unset):
        tags (list[str] | None | Unset): A list of tags associated with the domain.
        pad_to_resolution (float | None | Unset): Optional resolution in meters to snap the domain bounding box to. When
            set, the bounding box (the 'domain' feature) is snapped outward to the nearest multiple of this value. Grids
            whose resolutions divide evenly into this value will produce identical, aligned footprints on this domain.
        style (DomainStyle | None | Unset): Optional visual style for rendering the domain on a map.
    """

    type_: Literal["FeatureCollection"]
    features: list[GeoJsonFeature]
    bbox: list[float] | None | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    crs: GeoJsonCRS | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    pad_to_resolution: float | None | Unset = UNSET
    style: DomainStyle | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.domain_style import DomainStyle

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

        name = self.name

        description = self.description

        crs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.crs, Unset):
            crs = self.crs.to_dict()

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        pad_to_resolution: float | None | Unset
        if isinstance(self.pad_to_resolution, Unset):
            pad_to_resolution = UNSET
        else:
            pad_to_resolution = self.pad_to_resolution

        style: dict[str, Any] | None | Unset
        if isinstance(self.style, Unset):
            style = UNSET
        elif isinstance(self.style, DomainStyle):
            style = self.style.to_dict()
        else:
            style = self.style

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
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if crs is not UNSET:
            field_dict["crs"] = crs
        if tags is not UNSET:
            field_dict["tags"] = tags
        if pad_to_resolution is not UNSET:
            field_dict["pad_to_resolution"] = pad_to_resolution
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.domain_style import DomainStyle
        from ..models.geo_json_crs import GeoJsonCRS
        from ..models.geo_json_feature import GeoJsonFeature

        d = dict(src_dict)
        type_ = cast(Literal["FeatureCollection"], d.pop("type"))
        if type_ != "FeatureCollection":
            raise ValueError(
                f"type must match const 'FeatureCollection', got '{type_}'"
            )

        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = GeoJsonFeature.from_dict(features_item_data)

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

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _crs = d.pop("crs", UNSET)
        crs: GeoJsonCRS | Unset
        if isinstance(_crs, Unset):
            crs = UNSET
        else:
            crs = GeoJsonCRS.from_dict(_crs)

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_pad_to_resolution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        pad_to_resolution = _parse_pad_to_resolution(d.pop("pad_to_resolution", UNSET))

        def _parse_style(data: object) -> DomainStyle | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                style_type_0 = DomainStyle.from_dict(data)

                return style_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DomainStyle | None | Unset, data)

        style = _parse_style(d.pop("style", UNSET))

        geo_json_feature_collection = cls(
            type_=type_,
            features=features,
            bbox=bbox,
            name=name,
            description=description,
            crs=crs,
            tags=tags,
            pad_to_resolution=pad_to_resolution,
            style=style,
        )

        geo_json_feature_collection.additional_properties = d
        return geo_json_feature_collection

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
