from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..models.fuel_moisture_month import FuelMoistureMonth
from ..models.relative_elevation import RelativeElevation
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateFosbergFuelMoistureRequest")


@_attrs_define
class CreateFosbergFuelMoistureRequest:
    """Request body for a Fosberg 1-hour dead fuel moisture content grid.

    Does not extend CreateSourceGridRequestBase: this is a grid -> grid
    derivation with no external raster and no alignment input. The output
    inherits the topography grid's domain, CRS, transform, and georeference.

        Attributes:
            source_topography_grid_id (str): ID of a completed 2D topography grid with `slope` and `aspect` bands (both in
                degrees).
            source_irradiance_grid_id (str): ID of a completed leaflux irradiance grid with an `irradiance.surface.relative`
                band, on the topography grid's exact horizontal lattice (equivalent CRS, y/x shape, and affine transform). Per-
                cell shading is derived as 1 - irradiance.surface.relative. Resample one grid onto the other when their lattices
                differ.
            dry_bulb_temp (float): Dry-bulb air temperature in degrees Fahrenheit (the Fosberg table lineage is Fahrenheit).
                Must be >= 10.
            relative_humidity (float): Relative humidity as a percent (0-100).
            time (int): Local time of day in 24-hour HHMM form (e.g. 1200 for noon). Restricted to 0800-1959; the model has
                no daytime table outside that window.
            month (FuelMoistureMonth): Month of the burn scenario, selecting the Fosberg correction table.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            elevation (RelativeElevation | Unset): Site elevation relative to the reference weather station.

                This is a Fosberg correction category, NOT the topography elevation band:
                `below` = 1000-2000 ft below the station, `near` = within 1000 ft (no
                correction), `above` = 1000-2000 ft above the station.
    """

    source_topography_grid_id: str
    source_irradiance_grid_id: str
    dry_bulb_temp: float
    relative_humidity: float
    time: int
    month: FuelMoistureMonth
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    elevation: RelativeElevation | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        source_topography_grid_id = self.source_topography_grid_id

        source_irradiance_grid_id = self.source_irradiance_grid_id

        dry_bulb_temp = self.dry_bulb_temp

        relative_humidity = self.relative_humidity

        time = self.time

        month = self.month.value

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        elevation: str | Unset = UNSET
        if not isinstance(self.elevation, Unset):
            elevation = self.elevation.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source_topography_grid_id": source_topography_grid_id,
                "source_irradiance_grid_id": source_irradiance_grid_id,
                "dry_bulb_temp": dry_bulb_temp,
                "relative_humidity": relative_humidity,
                "time": time,
                "month": month,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if elevation is not UNSET:
            field_dict["elevation"] = elevation

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        source_topography_grid_id = d.pop("source_topography_grid_id")

        source_irradiance_grid_id = d.pop("source_irradiance_grid_id")

        dry_bulb_temp = d.pop("dry_bulb_temp")

        relative_humidity = d.pop("relative_humidity")

        time = d.pop("time")

        month = FuelMoistureMonth(d.pop("month"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _elevation = d.pop("elevation", UNSET)
        elevation: RelativeElevation | Unset
        if isinstance(_elevation, Unset):
            elevation = UNSET
        else:
            elevation = RelativeElevation(_elevation)

        create_fosberg_fuel_moisture_request = cls(
            source_topography_grid_id=source_topography_grid_id,
            source_irradiance_grid_id=source_irradiance_grid_id,
            dry_bulb_temp=dry_bulb_temp,
            relative_humidity=relative_humidity,
            time=time,
            month=month,
            name=name,
            description=description,
            tags=tags,
            elevation=elevation,
        )

        return create_fosberg_fuel_moisture_request
