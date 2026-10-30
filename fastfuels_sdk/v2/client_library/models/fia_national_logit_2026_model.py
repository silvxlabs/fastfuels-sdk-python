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

T = TypeVar("T", bound="FiaNationalLogit2026Model")


@_attrs_define
class FiaNationalLogit2026Model:
    """National refit to FIA trees with both compacted and uncompacted crown
    ratios recorded. Covers every FIA species, using the California, Oregon and
    Washington coefficients when the domain centroid is in one of those states.

        Attributes:
            name (Literal['fia_national_logit_2026'] | Unset):  Default: 'fia_national_logit_2026'.
    """

    name: Literal["fia_national_logit_2026"] | Unset = "fia_national_logit_2026"
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
        name = cast(Literal["fia_national_logit_2026"] | Unset, d.pop("name", UNSET))
        if name != "fia_national_logit_2026" and not isinstance(name, Unset):
            raise ValueError(
                f"name must match const 'fia_national_logit_2026', got '{name}'"
            )

        fia_national_logit_2026_model = cls(
            name=name,
        )

        fia_national_logit_2026_model.additional_properties = d
        return fia_national_logit_2026_model

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
