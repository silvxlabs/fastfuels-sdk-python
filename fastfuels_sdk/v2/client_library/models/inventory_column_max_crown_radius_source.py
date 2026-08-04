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

from ..models.max_crown_radius_unit import MaxCrownRadiusUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryColumnMaxCrownRadiusSource")


@_attrs_define
class InventoryColumnMaxCrownRadiusSource:
    """Read per-tree max crown radius from an inventory column.

    The crown profile model still drives the crown shape — the supplied
    radius rescales it so the maximum radius matches the per-tree value.

        Attributes:
            column (str):
            type_ (Literal['inventory_column'] | Unset):  Default: 'inventory_column'.
            unit (MaxCrownRadiusUnit | Unset): Accepted inventory max crown radius units.
    """

    column: str
    type_: Literal["inventory_column"] | Unset = "inventory_column"
    unit: MaxCrownRadiusUnit | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        column = self.column

        type_ = self.type_

        unit: str | Unset = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "column": column,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        column = d.pop("column")

        type_ = cast(Literal["inventory_column"] | Unset, d.pop("type", UNSET))
        if type_ != "inventory_column" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'inventory_column', got '{type_}'")

        _unit = d.pop("unit", UNSET)
        unit: MaxCrownRadiusUnit | Unset
        if isinstance(_unit, Unset):
            unit = UNSET
        else:
            unit = MaxCrownRadiusUnit(_unit)

        inventory_column_max_crown_radius_source = cls(
            column=column,
            type_=type_,
            unit=unit,
        )

        return inventory_column_max_crown_radius_source
