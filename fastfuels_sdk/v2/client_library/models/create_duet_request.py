from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..models.duet_band import DuetBand
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.duet_calibration import DuetCalibration


T = TypeVar("T", bound="CreateDuetRequest")


@_attrs_define
class CreateDuetRequest:
    """Request body for creating a DUET surface fuel grid from a tree grid.

    Does not extend CreateGridRequestBase: like the 3D grids it derives from,
    DUET grids do not support modifications.

        Attributes:
            years_since_burn (int): Years of litter accumulation to simulate. DUET begins the year of the last burn, when
                standing grass and litter have been consumed, so this is the stand's time since fire. It is the highest-leverage
                parameter in the model and also drives runtime.
            source_grid_id (str): ID of a completed 3D tree grid carrying the `bulk_density.foliage.live`, `spcd`, and
                `fuel_moisture.live` bands.
            wind_direction (int | Unset): Prevailing wind direction in whole degrees clockwise from north. Default: 270.
            wind_variability (int | Unset): Angular spread of wind direction, in whole degrees. Default: 30.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            bands (list[DuetBand] | Unset): Which output bands to produce. Defaults to `fuel_load.grass` and
                `fuel_load.litter`.
            calibration (DuetCalibration | None | Unset): Optional calibration targets. DUET supplies the spatial pattern of
                surface fuels; its raw magnitudes are not physical. Without calibration the raw values are stored as-is.
    """

    years_since_burn: int
    source_grid_id: str
    wind_direction: int | Unset = 270
    wind_variability: int | Unset = 30
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    bands: list[DuetBand] | Unset = UNSET
    calibration: DuetCalibration | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.duet_calibration import DuetCalibration

        years_since_burn = self.years_since_burn

        source_grid_id = self.source_grid_id

        wind_direction = self.wind_direction

        wind_variability = self.wind_variability

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        bands: list[str] | Unset = UNSET
        if not isinstance(self.bands, Unset):
            bands = []
            for bands_item_data in self.bands:
                bands_item = bands_item_data.value
                bands.append(bands_item)

        calibration: dict[str, Any] | None | Unset
        if isinstance(self.calibration, Unset):
            calibration = UNSET
        elif isinstance(self.calibration, DuetCalibration):
            calibration = self.calibration.to_dict()
        else:
            calibration = self.calibration

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "years_since_burn": years_since_burn,
                "source_grid_id": source_grid_id,
            }
        )
        if wind_direction is not UNSET:
            field_dict["wind_direction"] = wind_direction
        if wind_variability is not UNSET:
            field_dict["wind_variability"] = wind_variability
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if bands is not UNSET:
            field_dict["bands"] = bands
        if calibration is not UNSET:
            field_dict["calibration"] = calibration

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.duet_calibration import DuetCalibration

        d = dict(src_dict)
        years_since_burn = d.pop("years_since_burn")

        source_grid_id = d.pop("source_grid_id")

        wind_direction = d.pop("wind_direction", UNSET)

        wind_variability = d.pop("wind_variability", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _bands = d.pop("bands", UNSET)
        bands: list[DuetBand] | Unset = UNSET
        if _bands is not UNSET:
            bands = []
            for bands_item_data in _bands:
                bands_item = DuetBand(bands_item_data)

                bands.append(bands_item)

        def _parse_calibration(data: object) -> DuetCalibration | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                calibration_type_0 = DuetCalibration.from_dict(data)

                return calibration_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DuetCalibration | None | Unset, data)

        calibration = _parse_calibration(d.pop("calibration", UNSET))

        create_duet_request = cls(
            years_since_burn=years_since_burn,
            source_grid_id=source_grid_id,
            wind_direction=wind_direction,
            wind_variability=wind_variability,
            name=name,
            description=description,
            tags=tags,
            bands=bands,
            calibration=calibration,
        )

        return create_duet_request
