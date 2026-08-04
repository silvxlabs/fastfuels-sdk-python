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

T = TypeVar("T", bound="QUICFireExportAlignmentDomainTarget")


@_attrs_define
class QUICFireExportAlignmentDomainTarget:
    """Anchor the fire grid to the Domain bounding box.

    Output cells tile the Domain bbox at the given `dx` / `dy`, padded
    outward if the bbox isn't already a whole multiple. `dz` sets the
    uniform vertical cell size; the exporter always writes `aa1=1` so
    fuel layers map 1:1 to QUIC-Fire cells. Defaults are QUIC-Fire's
    recommended values (2 m horizontal, 1 m vertical).

        Attributes:
            target (Literal['domain'] | Unset):  Default: 'domain'.
            dx (float | Unset): Horizontal fire-grid cell size in x (UTM east-west), in meters. QUIC-Fire recommends 2 m.
                Default: 2.0.
            dy (float | Unset): Horizontal fire-grid cell size in y (UTM north-south), in meters. Must equal `dx` — non-
                square fire-grid cells are not supported. Default: 2.0.
            dz (float | Unset): Vertical fire-grid cell size, in meters. QUIC-Fire recommends 1 m. Must equal the 3D tree
                grid's voxelization vertical resolution (`resolution.vertical`): the exporter never resamples vertically, so a
                mismatch is rejected with 422 rather than silently applied. Default: 1.0.
    """

    target: Literal["domain"] | Unset = "domain"
    dx: float | Unset = 2.0
    dy: float | Unset = 2.0
    dz: float | Unset = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        dx = self.dx

        dy = self.dy

        dz = self.dz

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target
        if dx is not UNSET:
            field_dict["dx"] = dx
        if dy is not UNSET:
            field_dict["dy"] = dy
        if dz is not UNSET:
            field_dict["dz"] = dz

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        target = cast(Literal["domain"] | Unset, d.pop("target", UNSET))
        if target != "domain" and not isinstance(target, Unset):
            raise ValueError(f"target must match const 'domain', got '{target}'")

        dx = d.pop("dx", UNSET)

        dy = d.pop("dy", UNSET)

        dz = d.pop("dz", UNSET)

        quic_fire_export_alignment_domain_target = cls(
            target=target,
            dx=dx,
            dy=dy,
            dz=dz,
        )

        quic_fire_export_alignment_domain_target.additional_properties = d
        return quic_fire_export_alignment_domain_target

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
