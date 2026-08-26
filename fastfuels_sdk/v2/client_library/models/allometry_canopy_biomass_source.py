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

from ..models.canopy_biomass_equations import CanopyBiomassEquations
from ..types import UNSET, Unset

T = TypeVar("T", bound="AllometryCanopyBiomassSource")


@_attrs_define
class AllometryCanopyBiomassSource:
    """Estimate each tree's crown biomass from allometric equations.

    The equations produce crown component biomass (foliage, branchwood);
    the `available_fuel` settings then reduce those components to the
    available canopy fuel used in the profile.

        Attributes:
            type_ (Literal['allometry'] | Unset):  Default: 'allometry'.
            equations (CanopyBiomassEquations | Unset): Allometric equation families for estimating crown biomass.

                A superset of the voxelize biomass equations: ``brown_1978`` (Brown,
                "Weight and Density of Crowns of Rocky Mountain Conifers", INT-197) is
                offered here because it is the equation set behind FuelCalc and the
                LANDFIRE canopy layers. It is scoped to Interior West conifers and is
                intended for compatibility studies, not as a national default.
    """

    type_: Literal["allometry"] | Unset = "allometry"
    equations: CanopyBiomassEquations | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        equations: str | Unset = UNSET
        if not isinstance(self.equations, Unset):
            equations = self.equations.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if equations is not UNSET:
            field_dict["equations"] = equations

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = cast(Literal["allometry"] | Unset, d.pop("type", UNSET))
        if type_ != "allometry" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'allometry', got '{type_}'")

        _equations = d.pop("equations", UNSET)
        equations: CanopyBiomassEquations | Unset
        if isinstance(_equations, Unset):
            equations = UNSET
        else:
            equations = CanopyBiomassEquations(_equations)

        allometry_canopy_biomass_source = cls(
            type_=type_,
            equations=equations,
        )

        return allometry_canopy_biomass_source
