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
    from ..models.geo_json_crs_properties import GeoJsonCRSProperties


T = TypeVar("T", bound="GeoJsonCRS")


@_attrs_define
class GeoJsonCRS:
    """
    Attributes:
        properties (GeoJsonCRSProperties):
        type_ (Literal['name'] | Unset):  Default: 'name'.
    """

    properties: GeoJsonCRSProperties
    type_: Literal["name"] | Unset = "name"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        properties = self.properties.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "properties": properties,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.geo_json_crs_properties import GeoJsonCRSProperties

        d = dict(src_dict)
        properties = GeoJsonCRSProperties.from_dict(d.pop("properties"))

        type_ = cast(Literal["name"] | Unset, d.pop("type", UNSET))
        if type_ != "name" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'name', got '{type_}'")

        geo_json_crs = cls(
            properties=properties,
            type_=type_,
        )

        geo_json_crs.additional_properties = d
        return geo_json_crs

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
