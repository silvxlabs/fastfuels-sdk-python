from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..models.canopy_branchwood_size_partition import CanopyBranchwoodSizePartition
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanopyBranchwood")


@_attrs_define
class CanopyBranchwood:
    """Branchwood availability: the size basis and how much of it counts.

    `fraction` multiplies the branchwood mass `size_partition` produces —
    the fine (0-1/4 inch) class under `equations` and `brown_proportions`,
    or total branchwood under `none` — so the fraction's referent is always
    an explicit choice, never an artifact of the biomass source.

        Attributes:
            size_partition (CanopyBranchwoodSizePartition | None | Unset): Size basis for the branchwood fraction. Omitted
                (`null`), it resolves by equation family: `equations` for `brown_1978` (which reports the fine class directly),
                `none` for `nsvb` and `jenkins` — total branchwood, the only basis that prices every species, since the
                `brown_proportions` fine-share crosswalk covers ~16 species and errors on common ones (quaking aspen, jack pine,
                water birch). Set `brown_proportions` explicitly to reduce an `nsvb`/`jenkins` total to the fine class where the
                species are covered.
            fraction (float | None | Unset): Fraction of the size basis counted as available fuel. Omitted (`null`), it
                resolves by partition: 0.5 against the fine class (`equations` / `brown_proportions`), the Brown & Reinhardt
                (1991) / FuelCalc consumed fraction, and 0.075 against total branchwood (`none`), which folds the fine-branch
                share and the consumed share into one number. Conrad et al. (2024) measured species-specific consumable
                fractions of the fine class from 0.0 to 0.99.
    """

    size_partition: CanopyBranchwoodSizePartition | None | Unset = UNSET
    fraction: float | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        size_partition: None | str | Unset
        if isinstance(self.size_partition, Unset):
            size_partition = UNSET
        elif isinstance(self.size_partition, CanopyBranchwoodSizePartition):
            size_partition = self.size_partition.value
        else:
            size_partition = self.size_partition

        fraction: float | None | Unset
        if isinstance(self.fraction, Unset):
            fraction = UNSET
        else:
            fraction = self.fraction

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if size_partition is not UNSET:
            field_dict["size_partition"] = size_partition
        if fraction is not UNSET:
            field_dict["fraction"] = fraction

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_size_partition(
            data: object,
        ) -> CanopyBranchwoodSizePartition | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                size_partition_type_0 = CanopyBranchwoodSizePartition(data)

                return size_partition_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CanopyBranchwoodSizePartition | None | Unset, data)

        size_partition = _parse_size_partition(d.pop("size_partition", UNSET))

        def _parse_fraction(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        fraction = _parse_fraction(d.pop("fraction", UNSET))

        canopy_branchwood = cls(
            size_partition=size_partition,
            fraction=fraction,
        )

        return canopy_branchwood
