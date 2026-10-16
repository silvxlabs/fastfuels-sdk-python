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
        key (str): Band key `<quantity>` or `<quantity>.<label>`, e.g. `fbfm`, `fuel_load.1hr`,
            `fuel_moisture.live.shrub`. The quantity sets the band's type and unit: `annual_disturbance` (categorical),
            `aspect` (continuous, deg), `bulk_density` (continuous, kg/m**3), `cbd` (continuous, kg/m**3), `cbh`
            (continuous, m), `cc` (continuous, %), `cfl` (continuous, kg/m**2), `chm` (continuous, m), `curing` (continuous,
            %), `duff_depth` (continuous, m), `elevation` (continuous, m), `fbfm` (categorical), `fbfm13` (categorical),
            `fccs` (categorical), `fuel_depth` (continuous, m), `fuel_load` (continuous, kg/m**2), `fuel_moisture`
            (continuous, %), `heat_content` (continuous, kJ/kg), `irradiance` (continuous), `leaf_area_density` (continuous,
            1/m), `plt_cn` (categorical), `savr` (continuous, 1/m), `slope` (continuous, deg), `spcd` (categorical), `tm_id`
            (categorical), `tree_id` (categorical), `volume_fraction` (continuous). The label is lowercase letters, digits
            and underscores.
        type_ (BandType | None | Unset): Optional; set by the key's quantity. If given, it must match.
        unit (None | str | Unset): Optional; set by the key's quantity. If given, it must match, in UDUNITS-2-conformant
            ASCII form with `**` for exponents (e.g. `kg/m**3`, `1/m`, `%`). See docs/units.md.
    """

    key: str
    type_: BandType | None | Unset = UNSET
    unit: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, BandType):
            type_ = self.type_.value
        else:
            type_ = self.type_

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
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        key = d.pop("key")

        def _parse_type_(data: object) -> BandType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = BandType(data)

                return type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BandType | None | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

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
