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

T = TypeVar("T", bound="CanopyChmHeightPercentile")


@_attrs_define
class CanopyChmHeightPercentile:
    """Canopy height as a percentile of tree heights in the cell.

    Attributes:
        method (Literal['height_percentile'] | Unset):  Default: 'height_percentile'.
        percentile (float | Unset): Tree-height percentile reported as canopy height. Default: 99.0.
    """

    method: Literal["height_percentile"] | Unset = "height_percentile"
    percentile: float | Unset = 99.0

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        percentile = self.percentile

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if percentile is not UNSET:
            field_dict["percentile"] = percentile

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["height_percentile"] | Unset, d.pop("method", UNSET))
        if method != "height_percentile" and not isinstance(method, Unset):
            raise ValueError(
                f"method must match const 'height_percentile', got '{method}'"
            )

        percentile = d.pop("percentile", UNSET)

        canopy_chm_height_percentile = cls(
            method=method,
            percentile=percentile,
        )

        return canopy_chm_height_percentile
