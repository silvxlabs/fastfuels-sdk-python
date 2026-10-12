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

from ..types import UNSET, Unset

T = TypeVar("T", bound="GridLatticeDomainTarget")


@_attrs_define
class GridLatticeDomainTarget:
    """Anchor output cells to the domain origin.

    For grids computed per cell rather than resampled from a raster, so there
    is no resampling `method` and no source pixel anchor to preserve.

        Attributes:
            target (Literal['domain'] | Unset):  Default: 'domain'.
            resolution (float | None | Unset):
    """

    target: Literal["domain"] | Unset = "domain"
    resolution: float | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        resolution: float | None | Unset
        if isinstance(self.resolution, Unset):
            resolution = UNSET
        else:
            resolution = self.resolution

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target
        if resolution is not UNSET:
            field_dict["resolution"] = resolution

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        target = cast(Literal["domain"] | Unset, d.pop("target", UNSET))
        if target != "domain" and not isinstance(target, Unset):
            raise ValueError(f"target must match const 'domain', got '{target}'")

        def _parse_resolution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        resolution = _parse_resolution(d.pop("resolution", UNSET))

        grid_lattice_domain_target = cls(
            target=target,
            resolution=resolution,
        )

        return grid_lattice_domain_target
