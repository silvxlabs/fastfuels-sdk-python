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

T = TypeVar("T", bound="ToneyReeves2009Model")


@_attrs_define
class ToneyReeves2009Model:
    """Toney and Reeves (2009), fitted in the Interior West (ID, MT, WY, NV, UT,
    CO, AZ, NM). Covers 31 species; other species get no crown base.

        Attributes:
            name (Literal['toney_reeves_2009'] | Unset):  Default: 'toney_reeves_2009'.
    """

    name: Literal["toney_reeves_2009"] | Unset = "toney_reeves_2009"
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
        name = cast(Literal["toney_reeves_2009"] | Unset, d.pop("name", UNSET))
        if name != "toney_reeves_2009" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'toney_reeves_2009', got '{name}'")

        toney_reeves_2009_model = cls(
            name=name,
        )

        toney_reeves_2009_model.additional_properties = d
        return toney_reeves_2009_model

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
