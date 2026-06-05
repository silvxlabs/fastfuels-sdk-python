from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.uniform_moisture_value import UniformMoistureValue


T = TypeVar("T", bound="MoistureModel")


@_attrs_define
class MoistureModel:
    """Live/dead fuel moisture settings.

    Attributes:
        live (None | UniformMoistureValue | Unset):
        dead (None | UniformMoistureValue | Unset):
    """

    live: None | UniformMoistureValue | Unset = UNSET
    dead: None | UniformMoistureValue | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.uniform_moisture_value import UniformMoistureValue

        live: dict[str, Any] | None | Unset
        if isinstance(self.live, Unset):
            live = UNSET
        elif isinstance(self.live, UniformMoistureValue):
            live = self.live.to_dict()
        else:
            live = self.live

        dead: dict[str, Any] | None | Unset
        if isinstance(self.dead, Unset):
            dead = UNSET
        elif isinstance(self.dead, UniformMoistureValue):
            dead = self.dead.to_dict()
        else:
            dead = self.dead

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if live is not UNSET:
            field_dict["live"] = live
        if dead is not UNSET:
            field_dict["dead"] = dead

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.uniform_moisture_value import UniformMoistureValue

        d = dict(src_dict)

        def _parse_live(data: object) -> None | UniformMoistureValue | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                live_type_0 = UniformMoistureValue.from_dict(data)

                return live_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UniformMoistureValue | Unset, data)

        live = _parse_live(d.pop("live", UNSET))

        def _parse_dead(data: object) -> None | UniformMoistureValue | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dead_type_0 = UniformMoistureValue.from_dict(data)

                return dead_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UniformMoistureValue | Unset, data)

        dead = _parse_dead(d.pop("dead", UNSET))

        moisture_model = cls(
            live=live,
            dead=dead,
        )

        return moisture_model
