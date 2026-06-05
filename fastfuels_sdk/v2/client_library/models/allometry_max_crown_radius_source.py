from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AllometryMaxCrownRadiusSource")


@_attrs_define
class AllometryMaxCrownRadiusSource:
    """Use the crown profile model's allometric max crown radius (default).

    Attributes:
        type_ (Literal['allometry'] | Unset):  Default: 'allometry'.
    """

    type_: Literal["allometry"] | Unset = "allometry"

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = cast(Literal["allometry"] | Unset, d.pop("type", UNSET))
        if type_ != "allometry" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'allometry', got '{type_}'")

        allometry_max_crown_radius_source = cls(
            type_=type_,
        )

        return allometry_max_crown_radius_source
