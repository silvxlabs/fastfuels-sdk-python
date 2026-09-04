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
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReimputationMethod")


@_attrs_define
class ReimputationMethod:
    """The v1 fusion algorithm (``fastfuels_core.onramps.hag_pim``).

    Resample the PIM to ``resolution``, keep a cell's plot only where the CHM's
    canopy cover — the fraction of CHM cells taller than ``min_height`` — exceeds
    ``cover_threshold``, then expand the surviving plots as ``tree/pim``.
    ``resolution`` and ``min_height`` are the v1 production values;
    ``cover_threshold`` defaults to 0.2. ``fastfuels-core``'s own defaults are
    1.0 m and 0.25.

        Attributes:
            name (Literal['reimputation'] | Unset):  Default: 'reimputation'.
            resolution (float | Unset): Resolution (meters) the PIM is resampled to before conditioning. Must be no finer
                than the CHM cell and no coarser than the PIM cell. Default: 7.5.
            min_height (float | Unset): CHM height (meters) above which a cell counts as canopy. Default: 2.0.
            cover_threshold (float | Unset): Minimum canopy cover fraction (0-1) a resampled cell needs to keep its plot.
                Cells at or below this become gaps (no trees). Default: 0.2.
    """

    name: Literal["reimputation"] | Unset = "reimputation"
    resolution: float | Unset = 7.5
    min_height: float | Unset = 2.0
    cover_threshold: float | Unset = 0.2
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        resolution = self.resolution

        min_height = self.min_height

        cover_threshold = self.cover_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if resolution is not UNSET:
            field_dict["resolution"] = resolution
        if min_height is not UNSET:
            field_dict["min_height"] = min_height
        if cover_threshold is not UNSET:
            field_dict["cover_threshold"] = cover_threshold

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = cast(Literal["reimputation"] | Unset, d.pop("name", UNSET))
        if name != "reimputation" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'reimputation', got '{name}'")

        resolution = d.pop("resolution", UNSET)

        min_height = d.pop("min_height", UNSET)

        cover_threshold = d.pop("cover_threshold", UNSET)

        reimputation_method = cls(
            name=name,
            resolution=resolution,
            min_height=min_height,
            cover_threshold=cover_threshold,
        )

        reimputation_method.additional_properties = d
        return reimputation_method

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
