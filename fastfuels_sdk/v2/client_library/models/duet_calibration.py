from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.duet_parameter_calibration import DuetParameterCalibration


T = TypeVar("T", bound="DuetCalibration")


@_attrs_define
class DuetCalibration:
    """Calibration targets, keyed by fuel parameter.

    Each parameter is calibrated independently; omitted parameters keep DUET's
    raw values.

        Attributes:
            fuel_load (DuetParameterCalibration | None | Unset):
            fuel_depth (DuetParameterCalibration | None | Unset):
            fuel_moisture (DuetParameterCalibration | None | Unset):
    """

    fuel_load: DuetParameterCalibration | None | Unset = UNSET
    fuel_depth: DuetParameterCalibration | None | Unset = UNSET
    fuel_moisture: DuetParameterCalibration | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.duet_parameter_calibration import DuetParameterCalibration

        fuel_load: dict[str, Any] | None | Unset
        if isinstance(self.fuel_load, Unset):
            fuel_load = UNSET
        elif isinstance(self.fuel_load, DuetParameterCalibration):
            fuel_load = self.fuel_load.to_dict()
        else:
            fuel_load = self.fuel_load

        fuel_depth: dict[str, Any] | None | Unset
        if isinstance(self.fuel_depth, Unset):
            fuel_depth = UNSET
        elif isinstance(self.fuel_depth, DuetParameterCalibration):
            fuel_depth = self.fuel_depth.to_dict()
        else:
            fuel_depth = self.fuel_depth

        fuel_moisture: dict[str, Any] | None | Unset
        if isinstance(self.fuel_moisture, Unset):
            fuel_moisture = UNSET
        elif isinstance(self.fuel_moisture, DuetParameterCalibration):
            fuel_moisture = self.fuel_moisture.to_dict()
        else:
            fuel_moisture = self.fuel_moisture

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if fuel_load is not UNSET:
            field_dict["fuel_load"] = fuel_load
        if fuel_depth is not UNSET:
            field_dict["fuel_depth"] = fuel_depth
        if fuel_moisture is not UNSET:
            field_dict["fuel_moisture"] = fuel_moisture

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.duet_parameter_calibration import DuetParameterCalibration

        d = dict(src_dict)

        def _parse_fuel_load(data: object) -> DuetParameterCalibration | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fuel_load_type_0 = DuetParameterCalibration.from_dict(data)

                return fuel_load_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DuetParameterCalibration | None | Unset, data)

        fuel_load = _parse_fuel_load(d.pop("fuel_load", UNSET))

        def _parse_fuel_depth(data: object) -> DuetParameterCalibration | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fuel_depth_type_0 = DuetParameterCalibration.from_dict(data)

                return fuel_depth_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DuetParameterCalibration | None | Unset, data)

        fuel_depth = _parse_fuel_depth(d.pop("fuel_depth", UNSET))

        def _parse_fuel_moisture(
            data: object,
        ) -> DuetParameterCalibration | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fuel_moisture_type_0 = DuetParameterCalibration.from_dict(data)

                return fuel_moisture_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DuetParameterCalibration | None | Unset, data)

        fuel_moisture = _parse_fuel_moisture(d.pop("fuel_moisture", UNSET))

        duet_calibration = cls(
            fuel_load=fuel_load,
            fuel_depth=fuel_depth,
            fuel_moisture=fuel_moisture,
        )

        return duet_calibration
