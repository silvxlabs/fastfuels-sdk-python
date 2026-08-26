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

from ..models.canopy_crown_width_equations import CanopyCrownWidthEquations
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanopyAllometryMaxCrownRadiusSource")


@_attrs_define
class CanopyAllometryMaxCrownRadiusSource:
    """Compute each tree's maximum crown radius from allometric equations.

    Supersets the voxelize allometry source with an `equations` choice,
    because canopy cover and crown biomass are separate axes here: which
    allometry supplies the radius is independent of how a cover method
    treats crowns that overlap, so a run can vary either without
    confounding the other.

        Attributes:
            type_ (Literal['allometry'] | Unset):  Default: 'allometry'.
            equations (CanopyCrownWidthEquations | Unset): Allometric equation families for a tree's maximum crown radius.

                ``purves`` (Purves et al. 2007) is the national default and the one
                the tree voxelization endpoint uses; it varies with height and
                crown ratio as well as diameter. ``crookston_stage`` (Crookston &
                Stage 1999, RMRS-GTR-24, reached through FVS) is the crown width
                behind FuelCalc's canopy cover — diameter alone above breast
                height, with regionally fitted coefficients — and is offered for
                compatibility studies.
    """

    type_: Literal["allometry"] | Unset = "allometry"
    equations: CanopyCrownWidthEquations | Unset = UNSET

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
        equations: CanopyCrownWidthEquations | Unset
        if isinstance(_equations, Unset):
            equations = UNSET
        else:
            equations = CanopyCrownWidthEquations(_equations)

        canopy_allometry_max_crown_radius_source = cls(
            type_=type_,
            equations=equations,
        )

        return canopy_allometry_max_crown_radius_source
