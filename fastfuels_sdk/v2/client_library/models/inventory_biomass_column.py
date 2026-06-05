from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.biomass_unit import BiomassUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryBiomassColumn")


@_attrs_define
class InventoryBiomassColumn:
    """Inventory column containing per-tree biomass for one component.

    Attributes:
        column (str):
        unit (BiomassUnit | Unset): Accepted inventory biomass units.
    """

    column: str
    unit: BiomassUnit | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        column = self.column

        unit: str | Unset = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "column": column,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column = d.pop("column")

        _unit = d.pop("unit", UNSET)
        unit: BiomassUnit | Unset
        if isinstance(_unit, Unset):
            unit = UNSET
        else:
            unit = BiomassUnit(_unit)

        inventory_biomass_column = cls(
            column=column,
            unit=unit,
        )

        return inventory_biomass_column
