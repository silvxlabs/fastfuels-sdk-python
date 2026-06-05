from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FieldSource")


@_attrs_define
class FieldSource:
    """A single physical quantity drawn from one band on one grid.

    Every per-role input to the QUIC-Fire export uses this shape so the schema
    is uniform across roles. The forward path for `nfuel>1` (when QUIC-Fire's
    multi-fuel-type capability becomes relevant) is to allow each per-fuel-type
    role to accept `FieldSource | dict[FuelType, FieldSource]`; today's scalar
    requests keep working unchanged when that lands.

        Attributes:
            grid_id (str): Grid containing the source band.
            band (str): Band key on that grid (e.g. 'fuel_load.1hr').
    """

    grid_id: str
    band: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grid_id = self.grid_id

        band = self.band

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grid_id": grid_id,
                "band": band,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grid_id = d.pop("grid_id")

        band = d.pop("band")

        field_source = cls(
            grid_id=grid_id,
            band=band,
        )

        field_source.additional_properties = d
        return field_source

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
