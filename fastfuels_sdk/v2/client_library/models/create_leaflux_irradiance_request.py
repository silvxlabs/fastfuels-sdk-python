from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..models.leaflux_band import LeafluxBand
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateLeafluxIrradianceRequest")


@_attrs_define
class CreateLeafluxIrradianceRequest:
    """Request body for creating a LeafLux irradiance grid from a 3D fuel grid.

    Does not extend CreateGridRequestBase because 3D grids do not support
    modifications. This is a grid -> grid derivation aligned to the source
    grid's geometry, so there is no resolution input.

        Attributes:
            source_lad_grid_id (str): ID of the completed 3D fuel grid whose `leaf_area_density` (LAD) band drives the Beer-
                Lambert light attenuation. This is the primary input the irradiance field is computed from. Named for the band
                it consumes so it reads unambiguously alongside `source_terrain_grid_id`.
            date_time (datetime.datetime): UTC instant at which to compute irradiance.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            source_terrain_grid_id (None | str | Unset): (optional) ID of a completed 2D terrain grid (with an `elevation`
                band) in the same domain and on the LAD grid's exact horizontal lattice (equivalent CRS, shape, and affine
                transform), used to drape the surface irradiance band over real terrain instead of a flat plane. Resample the
                terrain with the LAD grid as its alignment target when their lattices differ.
            bands (list[LeafluxBand] | Unset): Which output bands to produce. Defaults to `irradiance.surface.relative`.
            extinction_coefficient (float | Unset): Beer-Lambert extinction coefficient (leaflux `extn`). Default: 0.5.
    """

    source_lad_grid_id: str
    date_time: datetime.datetime
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    source_terrain_grid_id: None | str | Unset = UNSET
    bands: list[LeafluxBand] | Unset = UNSET
    extinction_coefficient: float | Unset = 0.5

    def to_dict(self) -> dict[str, Any]:
        source_lad_grid_id = self.source_lad_grid_id

        date_time = self.date_time.isoformat()

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        source_terrain_grid_id: None | str | Unset
        if isinstance(self.source_terrain_grid_id, Unset):
            source_terrain_grid_id = UNSET
        else:
            source_terrain_grid_id = self.source_terrain_grid_id

        bands: list[str] | Unset = UNSET
        if not isinstance(self.bands, Unset):
            bands = []
            for bands_item_data in self.bands:
                bands_item = bands_item_data.value
                bands.append(bands_item)

        extinction_coefficient = self.extinction_coefficient

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source_lad_grid_id": source_lad_grid_id,
                "date_time": date_time,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if source_terrain_grid_id is not UNSET:
            field_dict["source_terrain_grid_id"] = source_terrain_grid_id
        if bands is not UNSET:
            field_dict["bands"] = bands
        if extinction_coefficient is not UNSET:
            field_dict["extinction_coefficient"] = extinction_coefficient

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        source_lad_grid_id = d.pop("source_lad_grid_id")

        date_time = datetime.datetime.fromisoformat(d.pop("date_time"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_source_terrain_grid_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_terrain_grid_id = _parse_source_terrain_grid_id(
            d.pop("source_terrain_grid_id", UNSET)
        )

        _bands = d.pop("bands", UNSET)
        bands: list[LeafluxBand] | Unset = UNSET
        if _bands is not UNSET:
            bands = []
            for bands_item_data in _bands:
                bands_item = LeafluxBand(bands_item_data)

                bands.append(bands_item)

        extinction_coefficient = d.pop("extinction_coefficient", UNSET)

        create_leaflux_irradiance_request = cls(
            source_lad_grid_id=source_lad_grid_id,
            date_time=date_time,
            name=name,
            description=description,
            tags=tags,
            source_terrain_grid_id=source_terrain_grid_id,
            bands=bands,
            extinction_coefficient=extinction_coefficient,
        )

        return create_leaflux_irradiance_request
