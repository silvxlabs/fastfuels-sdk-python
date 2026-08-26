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

T = TypeVar("T", bound="ChmMeanAggregation")


@_attrs_define
class ChmMeanAggregation:
    """Average height of every return in the cell.

    Weighted by how the returns fall, so a cell that is half canopy and half
    gap reads between the two rather than at the canopy.

        Attributes:
            method (Literal['mean'] | Unset):  Default: 'mean'.
    """

    method: Literal["mean"] | Unset = "mean"

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
        method = cast(Literal["mean"] | Unset, d.pop("method", UNSET))
        if method != "mean" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'mean', got '{method}'")

        chm_mean_aggregation = cls(
            method=method,
        )

        return chm_mean_aggregation
