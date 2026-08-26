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

T = TypeVar("T", bound="ChmMaxAggregation")


@_attrs_define
class ChmMaxAggregation:
    """Tallest return in the cell.

    The height of whatever the cell's tallest thing is, which is a crown at a
    cell narrower than one and a stand's tallest tree at a cell wider than one.

        Attributes:
            method (Literal['max'] | Unset):  Default: 'max'.
    """

    method: Literal["max"] | Unset = "max"

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
        method = cast(Literal["max"] | Unset, d.pop("method", UNSET))
        if method != "max" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'max', got '{method}'")

        chm_max_aggregation = cls(
            method=method,
        )

        return chm_max_aggregation
