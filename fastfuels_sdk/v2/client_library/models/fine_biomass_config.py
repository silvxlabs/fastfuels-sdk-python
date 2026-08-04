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

T = TypeVar("T", bound="FineBiomassConfig")


@_attrs_define
class FineBiomassConfig:
    """Configuration for derived fine biomass.

    Attributes:
        recipe (Literal['foliage_plus_branchwood_fraction']):
        branchwood_fraction (float):
    """

    recipe: Literal["foliage_plus_branchwood_fraction"]
    branchwood_fraction: float

    def to_dict(self) -> dict[str, Any]:
        recipe = self.recipe

        branchwood_fraction = self.branchwood_fraction

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "recipe": recipe,
                "branchwood_fraction": branchwood_fraction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        recipe = cast(Literal["foliage_plus_branchwood_fraction"], d.pop("recipe"))
        if recipe != "foliage_plus_branchwood_fraction":
            raise ValueError(
                f"recipe must match const 'foliage_plus_branchwood_fraction', got '{recipe}'"
            )

        branchwood_fraction = d.pop("branchwood_fraction")

        fine_biomass_config = cls(
            recipe=recipe,
            branchwood_fraction=branchwood_fraction,
        )

        return fine_biomass_config
