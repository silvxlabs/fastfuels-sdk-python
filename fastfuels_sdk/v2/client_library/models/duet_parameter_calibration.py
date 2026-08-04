from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.duet_constant_calibration_target import DuetConstantCalibrationTarget
    from ..models.duet_max_min_calibration_target import DuetMaxMinCalibrationTarget
    from ..models.duet_mean_sd_calibration_target import DuetMeanSdCalibrationTarget


T = TypeVar("T", bound="DuetParameterCalibration")


@_attrs_define
class DuetParameterCalibration:
    """Per-fuel-type calibration targets for one fuel parameter.

    `all` is exclusive: it calibrates every fuel type together and cannot be
    combined with a per-type target.

        Attributes:
            grass (DuetConstantCalibrationTarget | DuetMaxMinCalibrationTarget | DuetMeanSdCalibrationTarget | None |
                Unset):
            coniferous (DuetConstantCalibrationTarget | DuetMaxMinCalibrationTarget | DuetMeanSdCalibrationTarget | None |
                Unset):
            deciduous (DuetConstantCalibrationTarget | DuetMaxMinCalibrationTarget | DuetMeanSdCalibrationTarget | None |
                Unset):
            litter (DuetConstantCalibrationTarget | DuetMaxMinCalibrationTarget | DuetMeanSdCalibrationTarget | None |
                Unset):
            all_ (DuetConstantCalibrationTarget | DuetMaxMinCalibrationTarget | DuetMeanSdCalibrationTarget | None | Unset):
    """

    grass: (
        DuetConstantCalibrationTarget
        | DuetMaxMinCalibrationTarget
        | DuetMeanSdCalibrationTarget
        | None
        | Unset
    ) = UNSET
    coniferous: (
        DuetConstantCalibrationTarget
        | DuetMaxMinCalibrationTarget
        | DuetMeanSdCalibrationTarget
        | None
        | Unset
    ) = UNSET
    deciduous: (
        DuetConstantCalibrationTarget
        | DuetMaxMinCalibrationTarget
        | DuetMeanSdCalibrationTarget
        | None
        | Unset
    ) = UNSET
    litter: (
        DuetConstantCalibrationTarget
        | DuetMaxMinCalibrationTarget
        | DuetMeanSdCalibrationTarget
        | None
        | Unset
    ) = UNSET
    all_: (
        DuetConstantCalibrationTarget
        | DuetMaxMinCalibrationTarget
        | DuetMeanSdCalibrationTarget
        | None
        | Unset
    ) = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.duet_constant_calibration_target import (
            DuetConstantCalibrationTarget,
        )
        from ..models.duet_max_min_calibration_target import DuetMaxMinCalibrationTarget
        from ..models.duet_mean_sd_calibration_target import DuetMeanSdCalibrationTarget

        grass: dict[str, Any] | None | Unset
        if isinstance(self.grass, Unset):
            grass = UNSET
        elif (
            isinstance(self.grass, DuetMaxMinCalibrationTarget)
            or isinstance(self.grass, DuetMeanSdCalibrationTarget)
            or isinstance(self.grass, DuetConstantCalibrationTarget)
        ):
            grass = self.grass.to_dict()
        else:
            grass = self.grass

        coniferous: dict[str, Any] | None | Unset
        if isinstance(self.coniferous, Unset):
            coniferous = UNSET
        elif (
            isinstance(self.coniferous, DuetMaxMinCalibrationTarget)
            or isinstance(self.coniferous, DuetMeanSdCalibrationTarget)
            or isinstance(self.coniferous, DuetConstantCalibrationTarget)
        ):
            coniferous = self.coniferous.to_dict()
        else:
            coniferous = self.coniferous

        deciduous: dict[str, Any] | None | Unset
        if isinstance(self.deciduous, Unset):
            deciduous = UNSET
        elif (
            isinstance(self.deciduous, DuetMaxMinCalibrationTarget)
            or isinstance(self.deciduous, DuetMeanSdCalibrationTarget)
            or isinstance(self.deciduous, DuetConstantCalibrationTarget)
        ):
            deciduous = self.deciduous.to_dict()
        else:
            deciduous = self.deciduous

        litter: dict[str, Any] | None | Unset
        if isinstance(self.litter, Unset):
            litter = UNSET
        elif (
            isinstance(self.litter, DuetMaxMinCalibrationTarget)
            or isinstance(self.litter, DuetMeanSdCalibrationTarget)
            or isinstance(self.litter, DuetConstantCalibrationTarget)
        ):
            litter = self.litter.to_dict()
        else:
            litter = self.litter

        all_: dict[str, Any] | None | Unset
        if isinstance(self.all_, Unset):
            all_ = UNSET
        elif (
            isinstance(self.all_, DuetMaxMinCalibrationTarget)
            or isinstance(self.all_, DuetMeanSdCalibrationTarget)
            or isinstance(self.all_, DuetConstantCalibrationTarget)
        ):
            all_ = self.all_.to_dict()
        else:
            all_ = self.all_

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if grass is not UNSET:
            field_dict["grass"] = grass
        if coniferous is not UNSET:
            field_dict["coniferous"] = coniferous
        if deciduous is not UNSET:
            field_dict["deciduous"] = deciduous
        if litter is not UNSET:
            field_dict["litter"] = litter
        if all_ is not UNSET:
            field_dict["all"] = all_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.duet_constant_calibration_target import (
            DuetConstantCalibrationTarget,
        )
        from ..models.duet_max_min_calibration_target import DuetMaxMinCalibrationTarget
        from ..models.duet_mean_sd_calibration_target import DuetMeanSdCalibrationTarget

        d = dict(src_dict)

        def _parse_grass(
            data: object,
        ) -> (
            DuetConstantCalibrationTarget
            | DuetMaxMinCalibrationTarget
            | DuetMeanSdCalibrationTarget
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                grass_type_0_type_0 = DuetMaxMinCalibrationTarget.from_dict(data)

                return grass_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                grass_type_0_type_1 = DuetMeanSdCalibrationTarget.from_dict(data)

                return grass_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                grass_type_0_type_2 = DuetConstantCalibrationTarget.from_dict(data)

                return grass_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DuetConstantCalibrationTarget
                | DuetMaxMinCalibrationTarget
                | DuetMeanSdCalibrationTarget
                | None
                | Unset,
                data,
            )

        grass = _parse_grass(d.pop("grass", UNSET))

        def _parse_coniferous(
            data: object,
        ) -> (
            DuetConstantCalibrationTarget
            | DuetMaxMinCalibrationTarget
            | DuetMeanSdCalibrationTarget
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                coniferous_type_0_type_0 = DuetMaxMinCalibrationTarget.from_dict(data)

                return coniferous_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                coniferous_type_0_type_1 = DuetMeanSdCalibrationTarget.from_dict(data)

                return coniferous_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                coniferous_type_0_type_2 = DuetConstantCalibrationTarget.from_dict(data)

                return coniferous_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DuetConstantCalibrationTarget
                | DuetMaxMinCalibrationTarget
                | DuetMeanSdCalibrationTarget
                | None
                | Unset,
                data,
            )

        coniferous = _parse_coniferous(d.pop("coniferous", UNSET))

        def _parse_deciduous(
            data: object,
        ) -> (
            DuetConstantCalibrationTarget
            | DuetMaxMinCalibrationTarget
            | DuetMeanSdCalibrationTarget
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                deciduous_type_0_type_0 = DuetMaxMinCalibrationTarget.from_dict(data)

                return deciduous_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                deciduous_type_0_type_1 = DuetMeanSdCalibrationTarget.from_dict(data)

                return deciduous_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                deciduous_type_0_type_2 = DuetConstantCalibrationTarget.from_dict(data)

                return deciduous_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DuetConstantCalibrationTarget
                | DuetMaxMinCalibrationTarget
                | DuetMeanSdCalibrationTarget
                | None
                | Unset,
                data,
            )

        deciduous = _parse_deciduous(d.pop("deciduous", UNSET))

        def _parse_litter(
            data: object,
        ) -> (
            DuetConstantCalibrationTarget
            | DuetMaxMinCalibrationTarget
            | DuetMeanSdCalibrationTarget
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                litter_type_0_type_0 = DuetMaxMinCalibrationTarget.from_dict(data)

                return litter_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                litter_type_0_type_1 = DuetMeanSdCalibrationTarget.from_dict(data)

                return litter_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                litter_type_0_type_2 = DuetConstantCalibrationTarget.from_dict(data)

                return litter_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DuetConstantCalibrationTarget
                | DuetMaxMinCalibrationTarget
                | DuetMeanSdCalibrationTarget
                | None
                | Unset,
                data,
            )

        litter = _parse_litter(d.pop("litter", UNSET))

        def _parse_all_(
            data: object,
        ) -> (
            DuetConstantCalibrationTarget
            | DuetMaxMinCalibrationTarget
            | DuetMeanSdCalibrationTarget
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                all_type_0_type_0 = DuetMaxMinCalibrationTarget.from_dict(data)

                return all_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                all_type_0_type_1 = DuetMeanSdCalibrationTarget.from_dict(data)

                return all_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                all_type_0_type_2 = DuetConstantCalibrationTarget.from_dict(data)

                return all_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DuetConstantCalibrationTarget
                | DuetMaxMinCalibrationTarget
                | DuetMeanSdCalibrationTarget
                | None
                | Unset,
                data,
            )

        all_ = _parse_all_(d.pop("all", UNSET))

        duet_parameter_calibration = cls(
            grass=grass,
            coniferous=coniferous,
            deciduous=deciduous,
            litter=litter,
            all_=all_,
        )

        return duet_parameter_calibration
