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

T = TypeVar("T", bound="LandscapeExportAlignmentGridTarget")


@_attrs_define
class LandscapeExportAlignmentGridTarget:
    """Anchor the landscape to an existing grid's lattice.

    Useful when role grids share a non-Domain-anchored lattice (e.g. all
    chained off a `target="native"` master grid). The referenced grid's
    CRS, transform, and shape become the landscape lattice.

        Attributes:
            target (Literal['grid']):
            grid_id (str): Existing grid whose lattice (CRS, transform, shape) the landscape should match exactly.
    """

    target: Literal["grid"]
    grid_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        grid_id = self.grid_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target": target,
                "grid_id": grid_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        target = cast(Literal["grid"], d.pop("target"))
        if target != "grid":
            raise ValueError(f"target must match const 'grid', got '{target}'")

        grid_id = d.pop("grid_id")

        landscape_export_alignment_grid_target = cls(
            target=target,
            grid_id=grid_id,
        )

        landscape_export_alignment_grid_target.additional_properties = d
        return landscape_export_alignment_grid_target

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
