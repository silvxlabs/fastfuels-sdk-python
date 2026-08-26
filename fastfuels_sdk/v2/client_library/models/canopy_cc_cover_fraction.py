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

T = TypeVar("T", bound="CanopyCcCoverFraction")


@_attrs_define
class CanopyCcCoverFraction:
    """Canopy cover as the fraction of the cell with canopy above a height.

    A CHM-style cover measure, distinct from projected crown cover: it
    reports where canopy *surface* exceeds `height_threshold` rather than
    the projection of all suspended canopy.

        Attributes:
            method (Literal['cover_fraction'] | Unset):  Default: 'cover_fraction'.
            height_threshold (float | Unset): Height in meters above which canopy counts as cover. Default: 2.0.
    """

    method: Literal["cover_fraction"] | Unset = "cover_fraction"
    height_threshold: float | Unset = 2.0

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        height_threshold = self.height_threshold

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if height_threshold is not UNSET:
            field_dict["height_threshold"] = height_threshold

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["cover_fraction"] | Unset, d.pop("method", UNSET))
        if method != "cover_fraction" and not isinstance(method, Unset):
            raise ValueError(
                f"method must match const 'cover_fraction', got '{method}'"
            )

        height_threshold = d.pop("height_threshold", UNSET)

        canopy_cc_cover_fraction = cls(
            method=method,
            height_threshold=height_threshold,
        )

        return canopy_cc_cover_fraction
