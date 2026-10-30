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

T = TypeVar("T", bound="Randolph2010Model")


@_attrs_define
class Randolph2010Model:
    """Randolph (2010), fitted in the South (AL, AR, FL, GA, KY, LA, NC, SC, TN,
    TX, VA). Covers 24 species, 10 genera and several junipers; other species get
    no crown base.

        Attributes:
            name (Literal['randolph_2010'] | Unset):  Default: 'randolph_2010'.
    """

    name: Literal["randolph_2010"] | Unset = "randolph_2010"
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
        name = cast(Literal["randolph_2010"] | Unset, d.pop("name", UNSET))
        if name != "randolph_2010" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'randolph_2010', got '{name}'")

        randolph_2010_model = cls(
            name=name,
        )

        randolph_2010_model.additional_properties = d
        return randolph_2010_model

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
