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
    from ..models.layerset_crs import LayersetCrs
    from ..models.layerset_feature import LayersetFeature


T = TypeVar("T", bound="CreateLayersetRequestBody")


@_attrs_define
class CreateLayersetRequestBody:
    """Request body for uploading a flat GeoJSON layerset.

    The body **is** the GeoJSON FeatureCollection (matching ``POST /domains``,
    whose body is a ``FeatureCollection`` directly), extended with the
    resource-metadata fields. No ``type`` discriminator: the URL
    ``/features/layerset/geojson`` already discriminates layersets from
    road/water uploads.

    ``name`` overrides the optional GeoJSON ``name`` member inherited from
    ``LayersetFeatureCollection`` — the FeatureCollection's name doubles as the
    resource name, exactly as ``CreateDomainRequestBody`` treats it.

        Attributes:
            type_ (Literal['FeatureCollection']):
            features (list[LayersetFeature]):
            bbox (list[float] | None | Unset):
            name (str | Unset):  Default: ''.
            crs (LayersetCrs | None | Unset):
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
    """

    type_: Literal["FeatureCollection"]
    features: list[LayersetFeature]
    bbox: list[float] | None | Unset = UNSET
    name: str | Unset = ""
    crs: LayersetCrs | None | Unset = UNSET
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.layerset_crs import LayersetCrs

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

        crs: dict[str, Any] | None | Unset
        if isinstance(self.crs, Unset):
            crs = UNSET
        elif isinstance(self.crs, LayersetCrs):
            crs = self.crs.to_dict()
        else:
            crs = self.crs

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

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
        if crs is not UNSET:
            field_dict["crs"] = crs
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.layerset_crs import LayersetCrs
        from ..models.layerset_feature import LayersetFeature

        d = dict(src_dict)
        type_ = cast(Literal["FeatureCollection"], d.pop("type"))
        if type_ != "FeatureCollection":
            raise ValueError(
                f"type must match const 'FeatureCollection', got '{type_}'"
            )

        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = LayersetFeature.from_dict(features_item_data)

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

        def _parse_crs(data: object) -> LayersetCrs | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crs_type_0 = LayersetCrs.from_dict(data)

                return crs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LayersetCrs | None | Unset, data)

        crs = _parse_crs(d.pop("crs", UNSET))

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        create_layerset_request_body = cls(
            type_=type_,
            features=features,
            bbox=bbox,
            name=name,
            crs=crs,
            description=description,
            tags=tags,
        )

        create_layerset_request_body.additional_properties = d
        return create_layerset_request_body

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
