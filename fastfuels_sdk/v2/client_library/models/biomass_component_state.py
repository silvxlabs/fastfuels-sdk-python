from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BiomassComponentState")


@_attrs_define
class BiomassComponentState:
    """Live/dead partition for one biomass component.

    Attributes:
        live (float | Unset):  Default: 1.0.
        dead (float | Unset):  Default: 0.0.
    """

    live: float | Unset = 1.0
    dead: float | Unset = 0.0

    def to_dict(self) -> dict[str, Any]:
        live = self.live

        dead = self.dead

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if live is not UNSET:
            field_dict["live"] = live
        if dead is not UNSET:
            field_dict["dead"] = dead

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        live = d.pop("live", UNSET)

        dead = d.pop("dead", UNSET)

        biomass_component_state = cls(
            live=live,
            dead=dead,
        )

        return biomass_component_state
