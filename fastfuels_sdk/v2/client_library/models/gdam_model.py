from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GdamModel")


@_attrs_define
class GdamModel:
    """GDAM's flow-matching model predicts the uncompacted crown jointly with
    dbh, crown ratio and species, conditioned on whichever of them each tree
    has. Needs only position and height; covers the conterminous US.

        Attributes:
            name (Literal['gdam'] | Unset):  Default: 'gdam'.
    """

    name: Literal["gdam"] | Unset = "gdam"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = cast(Literal["gdam"] | Unset, d.pop("name", UNSET))
        if name != "gdam" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'gdam', got '{name}'")

        gdam_model = cls(
            name=name,
        )

        gdam_model.additional_properties = d
        return gdam_model

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
