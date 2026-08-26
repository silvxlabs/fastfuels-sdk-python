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

T = TypeVar("T", bound="ChmMedianAggregation")


@_attrs_define
class ChmMedianAggregation:
    """Height half the cell's returns lie below.

    The same statistic as `percentile` at 50, spelled the way it is usually
    asked for.

        Attributes:
            method (Literal['median'] | Unset):  Default: 'median'.
    """

    method: Literal["median"] | Unset = "median"

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
        method = cast(Literal["median"] | Unset, d.pop("method", UNSET))
        if method != "median" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'median', got '{method}'")

        chm_median_aggregation = cls(
            method=method,
        )

        return chm_median_aggregation
