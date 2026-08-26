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

from ..models.biomass_unit import BiomassUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryColumnCanopyBiomassSource")


@_attrs_define
class InventoryColumnCanopyBiomassSource:
    """Read each tree's available canopy fuel directly from an inventory column.

    The column value is used as-is: it must already be the per-tree mass of
    canopy fuel available to a crown fire (foliage plus the burnable fine
    branchwood). This bypasses allometry, `available_fuel`, species
    inclusion, and crown-class adjustment for fuel magnitude.

        Attributes:
            column (str): Inventory column holding per-tree available canopy fuel.
            type_ (Literal['inventory_column'] | Unset):  Default: 'inventory_column'.
            unit (BiomassUnit | Unset): Accepted inventory biomass units.
    """

    column: str
    type_: Literal["inventory_column"] | Unset = "inventory_column"
    unit: BiomassUnit | Unset = UNSET

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
        unit: BiomassUnit | Unset
        if isinstance(_unit, Unset):
            unit = UNSET
        else:
            unit = BiomassUnit(_unit)

        inventory_column_canopy_biomass_source = cls(
            column=column,
            type_=type_,
            unit=unit,
        )

        return inventory_column_canopy_biomass_source
