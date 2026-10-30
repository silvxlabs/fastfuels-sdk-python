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

T = TypeVar("T", bound="Westfall2019Model")


@_attrs_define
class Westfall2019Model:
    """Westfall, Westfall and Randolph (2019), fitted in the 24 northern US
    states. Covers 27 of FIA's eastern species groups; species outside them get
    no crown base.

        Attributes:
            name (Literal['westfall_2019'] | Unset):  Default: 'westfall_2019'.
    """

    name: Literal["westfall_2019"] | Unset = "westfall_2019"
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
        name = cast(Literal["westfall_2019"] | Unset, d.pop("name", UNSET))
        if name != "westfall_2019" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'westfall_2019', got '{name}'")

        westfall_2019_model = cls(
            name=name,
        )

        westfall_2019_model.additional_properties = d
        return westfall_2019_model

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
