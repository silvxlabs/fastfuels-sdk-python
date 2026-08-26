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

T = TypeVar("T", bound="CanopyCbhPercentile")


@_attrs_define
class CanopyCbhPercentile:
    """CBH as a percentile of the per-tree crown base heights in each cell.

    A conservative alternative to the mean for multi-storied stands, where
    a mean hides low ladder fuel. 50 is the median; 20 and 25 (first
    quartile) are the lower-tail aggregations used for conservative
    screening (Fulé et al. 2002; Mast et al. 2026).

        Attributes:
            percentile (float): Percentile of per-tree crown base heights. 50 is the median; 20 and 25 (first quartile) are
                common conservative lower-tail choices.
            method (Literal['percentile'] | Unset):  Default: 'percentile'.
    """

    percentile: float
    method: Literal["percentile"] | Unset = "percentile"

    def to_dict(self) -> dict[str, Any]:
        percentile = self.percentile

        method = self.method

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "percentile": percentile,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        percentile = d.pop("percentile")

        method = cast(Literal["percentile"] | Unset, d.pop("method", UNSET))
        if method != "percentile" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'percentile', got '{method}'")

        canopy_cbh_percentile = cls(
            percentile=percentile,
            method=method,
        )

        return canopy_cbh_percentile
