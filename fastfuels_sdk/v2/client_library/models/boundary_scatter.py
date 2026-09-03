from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BoundaryScatter")


@_attrs_define
class BoundaryScatter:
    """Controls stochastic scattering of category boundaries.

    Creates ragged, natural-looking transitions between categorical values
    (e.g. fuel model types) instead of the staircase edges that
    nearest-neighbor resampling produces. The swap probability halves with
    each cell of distance from the boundary. Non-burnable codes are
    protected from scattering.

        Attributes:
            depth (int | Unset): How many cells deep the scattering can reach. Effective scattering decays rapidly — most
                mixing happens within the first 3-4 cells. Default: 10.
            seed (int | Unset): Random seed for reproducible scattering. Default: 42.
    """

    depth: int | Unset = 10
    seed: int | Unset = 42
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        depth = self.depth

        seed = self.seed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if depth is not UNSET:
            field_dict["depth"] = depth
        if seed is not UNSET:
            field_dict["seed"] = seed

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        depth = d.pop("depth", UNSET)

        seed = d.pop("seed", UNSET)

        boundary_scatter = cls(
            depth=depth,
            seed=seed,
        )

        boundary_scatter.additional_properties = d
        return boundary_scatter

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
