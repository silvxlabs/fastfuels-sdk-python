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

T = TypeVar("T", bound="CanopyCcCrownOverlap")


@_attrs_define
class CanopyCcCrownOverlap:
    """Canopy cover from the Crookston-Stage random-overlap correction.

    ``100 * (1 - exp(-total_crown_area / cell_area))`` — the expected cover
    if stems were randomly placed. This is the FuelCalc estimator; it
    ignores actual stem positions.

        Attributes:
            method (Literal['crown_overlap'] | Unset):  Default: 'crown_overlap'.
    """

    method: Literal["crown_overlap"] | Unset = "crown_overlap"

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
        method = cast(Literal["crown_overlap"] | Unset, d.pop("method", UNSET))
        if method != "crown_overlap" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'crown_overlap', got '{method}'")

        canopy_cc_crown_overlap = cls(
            method=method,
        )

        return canopy_cc_crown_overlap
