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

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParametricCrownGeometrySource")


@_attrs_define
class ParametricCrownGeometrySource:
    """Draw every crown from `crown_profile_model` (default).

    Attributes:
        type_ (Literal['parametric'] | Unset):  Default: 'parametric'.
    """

    type_: Literal["parametric"] | Unset = "parametric"

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = cast(Literal["parametric"] | Unset, d.pop("type", UNSET))
        if type_ != "parametric" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'parametric', got '{type_}'")

        parametric_crown_geometry_source = cls(
            type_=type_,
        )

        return parametric_crown_geometry_source
