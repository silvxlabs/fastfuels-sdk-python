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

T = TypeVar("T", bound="LandscapeExportAlignmentDomainTarget")


@_attrs_define
class LandscapeExportAlignmentDomainTarget:
    """Anchor the landscape to the Domain bounding box.

    Output cells tile the Domain bbox at `resolution`, padded outward if the
    bbox isn't already a whole multiple. The default 30 m matches LANDFIRE's
    native resolution.

        Attributes:
            target (Literal['domain'] | Unset):  Default: 'domain'.
            resolution (float | Unset): Landscape cell size in meters. Defaults to 30 m, LANDFIRE's native resolution.
                Default: 30.0.
    """

    target: Literal["domain"] | Unset = "domain"
    resolution: float | Unset = 30.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        resolution = self.resolution

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        resolution = d.pop("resolution", UNSET)

        landscape_export_alignment_domain_target = cls(
            target=target,
            resolution=resolution,
        )

        landscape_export_alignment_domain_target.additional_properties = d
        return landscape_export_alignment_domain_target

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
