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

T = TypeVar("T", bound="CanopyCcCrownUnion")


@_attrs_define
class CanopyCcCrownUnion:
    """Canopy cover as the geometric union of projected crown areas.

    Measures the vertically projected crown cover directly from stem
    positions and crown radii, respecting the inventory's actual spatial
    pattern (clumping, gaps).

        Attributes:
            method (Literal['crown_union'] | Unset):  Default: 'crown_union'.
    """

    method: Literal["crown_union"] | Unset = "crown_union"

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["crown_union"] | Unset, d.pop("method", UNSET))
        if method != "crown_union" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'crown_union', got '{method}'")

        canopy_cc_crown_union = cls(
            method=method,
        )

        return canopy_cc_crown_union
