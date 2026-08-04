from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.band_type import BandType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.categorical_band_summary import CategoricalBandSummary
    from ..models.continuous_band_summary import ContinuousBandSummary


T = TypeVar("T", bound="Band")


@_attrs_define
class Band:
    """A single band in a grid.

    Attributes:
        key (str): Dot-notation key (e.g., 'fuel_load.1hr')
        type_ (BandType): Type of band data.
        index (int):
        name (None | str | Unset): Human-readable display name for the band (e.g. 'TreeMap ID', '1-hour Fuel Load').
        description (None | str | Unset): Longer-form description of what the band represents and how to interpret its
            values.
        unit (None | str | Unset): Physical unit of the band's pixel values, in UDUNITS-2-conformant ASCII form with
            `**` for exponents (e.g. `kg/m**3`, `1/m`, `%`). `None` for categorical/identifier bands. See docs/units.md.
        nodata (float | int | None | Unset): Value marking missing pixels in this band; pixels equal to it carry no data
            and should be excluded from analysis. `null` when the band has no missing pixels, or when they are represented
            as floating-point NaN.
        summary (CategoricalBandSummary | ContinuousBandSummary | None | Unset):
    """

    key: str
    type_: BandType
    index: int
    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    unit: None | str | Unset = UNSET
    nodata: float | int | None | Unset = UNSET
    summary: CategoricalBandSummary | ContinuousBandSummary | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.categorical_band_summary import CategoricalBandSummary
        from ..models.continuous_band_summary import ContinuousBandSummary

        key = self.key

        type_ = self.type_.value

        index = self.index

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        nodata: float | int | None | Unset
        if isinstance(self.nodata, Unset):
            nodata = UNSET
        else:
            nodata = self.nodata

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, ContinuousBandSummary) or isinstance(
            self.summary, CategoricalBandSummary
        ):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "type": type_,
                "index": index,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if unit is not UNSET:
            field_dict["unit"] = unit
        if nodata is not UNSET:
            field_dict["nodata"] = nodata
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.categorical_band_summary import CategoricalBandSummary
        from ..models.continuous_band_summary import ContinuousBandSummary

        d = dict(src_dict)
        key = d.pop("key")

        type_ = BandType(d.pop("type"))

        index = d.pop("index")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_nodata(data: object) -> float | int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | int | None | Unset, data)

        nodata = _parse_nodata(d.pop("nodata", UNSET))

        def _parse_summary(
            data: object,
        ) -> CategoricalBandSummary | ContinuousBandSummary | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0_type_0 = ContinuousBandSummary.from_dict(data)

                return summary_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0_type_1 = CategoricalBandSummary.from_dict(data)

                return summary_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CategoricalBandSummary | ContinuousBandSummary | None | Unset, data
            )

        summary = _parse_summary(d.pop("summary", UNSET))

        band = cls(
            key=key,
            type_=type_,
            index=index,
            name=name,
            description=description,
            unit=unit,
            nodata=nodata,
            summary=summary,
        )

        band.additional_properties = d
        return band

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
