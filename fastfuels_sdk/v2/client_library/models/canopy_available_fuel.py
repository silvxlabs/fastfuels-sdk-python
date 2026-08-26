from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.canopy_branchwood import CanopyBranchwood


T = TypeVar("T", bound="CanopyAvailableFuel")


@_attrs_define
class CanopyAvailableFuel:
    """Which crown biomass counts as available canopy fuel.

    Available fuel is the mass consumed in the flaming front of a crown
    fire: foliage plus a fraction of the fine (0-1/4 inch) branchwood.
    Fine branchwood is the finest class any published crown allometry
    resolves, so the size line is fixed; the caller-adjustable choices are
    the fractions and how the fine class is obtained from the biomass
    equations.

        Attributes:
            foliage_fraction (float | Unset): Fraction of foliage biomass counted as available fuel. Default: 1.0.
            branchwood (CanopyBranchwood | Unset): Branchwood availability: the size basis and how much of it counts.

                `fraction` multiplies the branchwood mass `size_partition` produces —
                the fine (0-1/4 inch) class under `equations` and `brown_proportions`,
                or total branchwood under `none` — so the fraction's referent is always
                an explicit choice, never an artifact of the biomass source.
    """

    foliage_fraction: float | Unset = 1.0
    branchwood: CanopyBranchwood | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        foliage_fraction = self.foliage_fraction

        branchwood: dict[str, Any] | Unset = UNSET
        if not isinstance(self.branchwood, Unset):
            branchwood = self.branchwood.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if foliage_fraction is not UNSET:
            field_dict["foliage_fraction"] = foliage_fraction
        if branchwood is not UNSET:
            field_dict["branchwood"] = branchwood

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.canopy_branchwood import CanopyBranchwood

        d = dict(src_dict)
        foliage_fraction = d.pop("foliage_fraction", UNSET)

        _branchwood = d.pop("branchwood", UNSET)
        branchwood: CanopyBranchwood | Unset
        if isinstance(_branchwood, Unset):
            branchwood = UNSET
        else:
            branchwood = CanopyBranchwood.from_dict(_branchwood)

        canopy_available_fuel = cls(
            foliage_fraction=foliage_fraction,
            branchwood=branchwood,
        )

        return canopy_available_fuel
