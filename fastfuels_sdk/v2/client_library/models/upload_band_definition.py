from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.band_type import BandType
from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadBandDefinition")


@_attrs_define
class UploadBandDefinition:
    """
    Attributes:
        key (str): Dot-notation variable name, e.g. 'bulk_density.foliage'
        type_ (BandType): Type of band data.
        unit (None | str | Unset): Physical unit of the band's pixel values, in UDUNITS-2-conformant ASCII form with
            `**` for exponents (e.g. `kg/m**3`, `1/m`, `%`). Optional for categorical/identifier bands. Non-canonical forms
            (`kg/m³`, `kg/m^3`, `kg/m3`) are rejected. See docs/units.md.
    """

    key: str
    type_: BandType
    unit: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        type_ = self.type_.value

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "type": type_,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        key = d.pop("key")

        type_ = BandType(d.pop("type"))

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        upload_band_definition = cls(
            key=key,
            type_=type_,
            unit=unit,
        )

        upload_band_definition.additional_properties = d
        return upload_band_definition

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
