from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.layerset_crs_properties import LayersetCrsProperties


T = TypeVar("T", bound="LayersetCrs")


@_attrs_define
class LayersetCrs:
    """Optional GeoJSON crs block.

    Per RFC 7946, ``crs`` is deprecated at the GeoJSON level (and
    ``geojson_pydantic`` therefore omits it), but the team's pipeline emits
    it and downstream consumers (geopandas, this server) read it to anchor
    bounds and the projected-CRS check in the upload router.

        Attributes:
            type_ (str | Unset):  Default: 'name'.
            properties (LayersetCrsProperties | Unset):
    """

    type_: str | Unset = "name"
    properties: LayersetCrsProperties | Unset = UNSET
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.layerset_crs_properties import LayersetCrsProperties

        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: LayersetCrsProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = LayersetCrsProperties.from_dict(_properties)

        layerset_crs = cls(
            type_=type_,
            properties=properties,
        )

        layerset_crs.additional_properties = d
        return layerset_crs

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
