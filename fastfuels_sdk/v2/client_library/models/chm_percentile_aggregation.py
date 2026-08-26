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

T = TypeVar("T", bound="ChmPercentileAggregation")


@_attrs_define
class ChmPercentileAggregation:
    """Height a given fraction of the cell's returns lie below.

    Attributes:
        percentile (float): Rank to take, as a percentage of the cell's returns. 100 is the tallest return and 50 the
            median. Between two returns the height is interpolated linearly.
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

        chm_percentile_aggregation = cls(
            percentile=percentile,
            method=method,
        )

        return chm_percentile_aggregation
