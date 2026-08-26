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

T = TypeVar("T", bound="CanopyCbhMinimum")


@_attrs_define
class CanopyCbhMinimum:
    """CBH as the lowest per-tree crown base height in each cell.

    The most conservative characterization — any tree can carry fire into
    the canopy (Mast et al. 2026), suited to risk-averse screening and
    firefighter-safety assessments.

        Attributes:
            method (Literal['minimum'] | Unset):  Default: 'minimum'.
    """

    method: Literal["minimum"] | Unset = "minimum"

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
        method = cast(Literal["minimum"] | Unset, d.pop("method", UNSET))
        if method != "minimum" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'minimum', got '{method}'")

        canopy_cbh_minimum = cls(
            method=method,
        )

        return canopy_cbh_minimum
