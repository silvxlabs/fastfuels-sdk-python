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

T = TypeVar("T", bound="CanopyNoCrownClassAdjustment")


@_attrs_define
class CanopyNoCrownClassAdjustment:
    """Apply no crown-class adjustment: every tree keeps its full crown weight.

    Attributes:
        method (Literal['none'] | Unset):  Default: 'none'.
    """

    method: Literal["none"] | Unset = "none"

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
        method = cast(Literal["none"] | Unset, d.pop("method", UNSET))
        if method != "none" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'none', got '{method}'")

        canopy_no_crown_class_adjustment = cls(
            method=method,
        )

        return canopy_no_crown_class_adjustment
