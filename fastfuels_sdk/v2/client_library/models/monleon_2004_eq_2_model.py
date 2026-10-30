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

T = TypeVar("T", bound="Monleon2004Eq2Model")


@_attrs_define
class Monleon2004Eq2Model:
    """Monleon, Azuma and Gedney (2004) Eq. 2, fitted in California, Oregon and
    Washington from crown ratio and dbh. Covers the Eq. 1 species plus other
    pines and oaks; other species get no crown base.

        Attributes:
            name (Literal['monleon_2004_eq2'] | Unset):  Default: 'monleon_2004_eq2'.
    """

    name: Literal["monleon_2004_eq2"] | Unset = "monleon_2004_eq2"
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
        name = cast(Literal["monleon_2004_eq2"] | Unset, d.pop("name", UNSET))
        if name != "monleon_2004_eq2" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'monleon_2004_eq2', got '{name}'")

        monleon_2004_eq_2_model = cls(
            name=name,
        )

        monleon_2004_eq_2_model.additional_properties = d
        return monleon_2004_eq_2_model

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
