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

T = TypeVar("T", bound="CanopyFuelcalcCrownClassAdjustment")


@_attrs_define
class CanopyFuelcalcCrownClassAdjustment:
    """Multiply crown weight by the FuelCalc species x crown-class factors.

    The factor is selected per tree from the inventory's crown class
    (`fia_crown_class_code`, FIA CCLCD). A tree whose code is missing — a null
    value, or an inventory that carries no crown class at all — takes the factor
    selected by `missing_crown_class`. With the `other_none` fallback that is a
    global 0.5 multiplier for most species — a large, deliberate reduction that
    reproduces how FuelCalc treats trees of unknown crown class.

        Attributes:
            method (Literal['fuelcalc_table'] | Unset):  Default: 'fuelcalc_table'.
            missing_crown_class (Literal['other_none'] | Unset): Factor column applied to trees whose `fia_crown_class_code`
                is missing — every tree in an inventory that carries no crown class. `other_none` is FuelCalc's Other/none
                column (0.5 for most species). Default: 'other_none'.
    """

    method: Literal["fuelcalc_table"] | Unset = "fuelcalc_table"
    missing_crown_class: Literal["other_none"] | Unset = "other_none"

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        missing_crown_class = self.missing_crown_class

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if missing_crown_class is not UNSET:
            field_dict["missing_crown_class"] = missing_crown_class

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["fuelcalc_table"] | Unset, d.pop("method", UNSET))
        if method != "fuelcalc_table" and not isinstance(method, Unset):
            raise ValueError(
                f"method must match const 'fuelcalc_table', got '{method}'"
            )

        missing_crown_class = cast(
            Literal["other_none"] | Unset, d.pop("missing_crown_class", UNSET)
        )
        if missing_crown_class != "other_none" and not isinstance(
            missing_crown_class, Unset
        ):
            raise ValueError(
                f"missing_crown_class must match const 'other_none', got '{missing_crown_class}'"
            )

        canopy_fuelcalc_crown_class_adjustment = cls(
            method=method,
            missing_crown_class=missing_crown_class,
        )

        return canopy_fuelcalc_crown_class_adjustment
