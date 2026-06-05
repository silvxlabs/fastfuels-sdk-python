from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateOsmWaterFeatureRequest")


@_attrs_define
class CreateOsmWaterFeatureRequest:
    """Request body for creating a water feature via OpenStreetMap.

    Attributes:
        type_ (Literal['water'] | Unset):  Default: 'water'.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        extent_buffer_m (float | Unset): Distance in meters to expand the domain extent outward before clipping fetched
            features. Lets streams and rivers that exit the domain at the boundary extend slightly past the edge, providing
            context for visualization and downstream operations (fuel breaks, perimeter analysis). Applied in the domain's
            projected CRS (reprojected to UTM if the domain CRS is geographic). Default 0 clips exactly to the domain
            boundary. Maximum: 100 meters. Default: 0.0.
    """

    type_: Literal["water"] | Unset = "water"
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    extent_buffer_m: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        extent_buffer_m = self.extent_buffer_m

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = cast(Literal["water"] | Unset, d.pop("type", UNSET))
        if type_ != "water" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'water', got '{type_}'")

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        extent_buffer_m = d.pop("extent_buffer_m", UNSET)

        create_osm_water_feature_request = cls(
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            extent_buffer_m=extent_buffer_m,
        )

        create_osm_water_feature_request.additional_properties = d
        return create_osm_water_feature_request

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
