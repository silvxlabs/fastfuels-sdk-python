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

T = TypeVar("T", bound="GridLatticeGridTarget")


@_attrs_define
class GridLatticeGridTarget:
    """Align output cells to an existing grid by id.

    `resolution=None` matches the target grid's lattice exactly. With an
    explicit `resolution`, the output keeps the target's CRS and origin at the
    new cell size.

        Attributes:
            target (Literal['grid']):
            grid_id (str):
            resolution (float | None | Unset):
    """

    target: Literal["grid"]
    grid_id: str
    resolution: float | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        grid_id = self.grid_id

        resolution: float | None | Unset
        if isinstance(self.resolution, Unset):
            resolution = UNSET
        else:
            resolution = self.resolution

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "target": target,
                "grid_id": grid_id,
            }
        )
        if resolution is not UNSET:
            field_dict["resolution"] = resolution

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        target = cast(Literal["grid"], d.pop("target"))
        if target != "grid":
            raise ValueError(f"target must match const 'grid', got '{target}'")

        grid_id = d.pop("grid_id")

        def _parse_resolution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        resolution = _parse_resolution(d.pop("resolution", UNSET))

        grid_lattice_grid_target = cls(
            target=target,
            grid_id=grid_id,
            resolution=resolution,
        )

        return grid_lattice_grid_target
