from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.geojson_crs_properties import GeojsonCrsProperties


T = TypeVar("T", bound="GeojsonCrs")


@_attrs_define
class GeojsonCrs:
    """Optional GeoJSON ``crs`` block (deprecated by RFC 7946, but widely emitted).

    Attributes:
        type_ (str | Unset):  Default: 'name'.
        properties (GeojsonCrsProperties | Unset):
    """

    type_: str | Unset = "name"
    properties: GeojsonCrsProperties | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.geojson_crs_properties import GeojsonCrsProperties

        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: GeojsonCrsProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = GeojsonCrsProperties.from_dict(_properties)

        geojson_crs = cls(
            type_=type_,
            properties=properties,
        )

        geojson_crs.additional_properties = d
        return geojson_crs

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
