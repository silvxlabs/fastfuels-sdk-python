from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.distribution import Distribution
from ..types import UNSET, Unset

T = TypeVar("T", bound="LayersetProperties")


@_attrs_define
class LayersetProperties:
    """Per-feature properties — one row of input to ``rasterize_layerset``.

    Required fields match the rasterizer's required input columns. Optional
    fields map to the rasterizer's optional bands; omitting them leaves the
    corresponding output band as NaN.

        Attributes:
            fuel_type (str):
            fuel_loading (float):
            fuel_height (float):
            percent_cover (float):
            distribution (Distribution): Per-cell spatial-distribution mode for a fuelbed.

                Mirrors ``fastfuels_core.rasterize_layerset``'s ``distribution`` column.
            strata_fb (None | str | Unset):
            patch_size (float | None | Unset):
            live_fuel_moisture (float | None | Unset):
            dead_fuel_moisture (float | None | Unset):
            heat_of_combustion (float | None | Unset):
            patch_std_dev (float | None | Unset):
    """

    fuel_type: str
    fuel_loading: float
    fuel_height: float
    percent_cover: float
    distribution: Distribution
    strata_fb: None | str | Unset = UNSET
    patch_size: float | None | Unset = UNSET
    live_fuel_moisture: float | None | Unset = UNSET
    dead_fuel_moisture: float | None | Unset = UNSET
    heat_of_combustion: float | None | Unset = UNSET
    patch_std_dev: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fuel_type = self.fuel_type

        fuel_loading = self.fuel_loading

        fuel_height = self.fuel_height

        percent_cover = self.percent_cover

        distribution = self.distribution.value

        strata_fb: None | str | Unset
        if isinstance(self.strata_fb, Unset):
            strata_fb = UNSET
        else:
            strata_fb = self.strata_fb

        patch_size: float | None | Unset
        if isinstance(self.patch_size, Unset):
            patch_size = UNSET
        else:
            patch_size = self.patch_size

        live_fuel_moisture: float | None | Unset
        if isinstance(self.live_fuel_moisture, Unset):
            live_fuel_moisture = UNSET
        else:
            live_fuel_moisture = self.live_fuel_moisture

        dead_fuel_moisture: float | None | Unset
        if isinstance(self.dead_fuel_moisture, Unset):
            dead_fuel_moisture = UNSET
        else:
            dead_fuel_moisture = self.dead_fuel_moisture

        heat_of_combustion: float | None | Unset
        if isinstance(self.heat_of_combustion, Unset):
            heat_of_combustion = UNSET
        else:
            heat_of_combustion = self.heat_of_combustion

        patch_std_dev: float | None | Unset
        if isinstance(self.patch_std_dev, Unset):
            patch_std_dev = UNSET
        else:
            patch_std_dev = self.patch_std_dev

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fuel_type": fuel_type,
                "fuel_loading": fuel_loading,
                "fuel_height": fuel_height,
                "percent_cover": percent_cover,
                "distribution": distribution,
            }
        )
        if strata_fb is not UNSET:
            field_dict["strata_fb"] = strata_fb
        if patch_size is not UNSET:
            field_dict["patch_size"] = patch_size
        if live_fuel_moisture is not UNSET:
            field_dict["live_fuel_moisture"] = live_fuel_moisture
        if dead_fuel_moisture is not UNSET:
            field_dict["dead_fuel_moisture"] = dead_fuel_moisture
        if heat_of_combustion is not UNSET:
            field_dict["heat_of_combustion"] = heat_of_combustion
        if patch_std_dev is not UNSET:
            field_dict["patch_std_dev"] = patch_std_dev

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        fuel_type = d.pop("fuel_type")

        fuel_loading = d.pop("fuel_loading")

        fuel_height = d.pop("fuel_height")

        percent_cover = d.pop("percent_cover")

        distribution = Distribution(d.pop("distribution"))

        def _parse_strata_fb(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        strata_fb = _parse_strata_fb(d.pop("strata_fb", UNSET))

        def _parse_patch_size(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        patch_size = _parse_patch_size(d.pop("patch_size", UNSET))

        def _parse_live_fuel_moisture(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        live_fuel_moisture = _parse_live_fuel_moisture(
            d.pop("live_fuel_moisture", UNSET)
        )

        def _parse_dead_fuel_moisture(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        dead_fuel_moisture = _parse_dead_fuel_moisture(
            d.pop("dead_fuel_moisture", UNSET)
        )

        def _parse_heat_of_combustion(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        heat_of_combustion = _parse_heat_of_combustion(
            d.pop("heat_of_combustion", UNSET)
        )

        def _parse_patch_std_dev(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        patch_std_dev = _parse_patch_std_dev(d.pop("patch_std_dev", UNSET))

        layerset_properties = cls(
            fuel_type=fuel_type,
            fuel_loading=fuel_loading,
            fuel_height=fuel_height,
            percent_cover=percent_cover,
            distribution=distribution,
            strata_fb=strata_fb,
            patch_size=patch_size,
            live_fuel_moisture=live_fuel_moisture,
            dead_fuel_moisture=dead_fuel_moisture,
            heat_of_combustion=heat_of_combustion,
            patch_std_dev=patch_std_dev,
        )

        layerset_properties.additional_properties = d
        return layerset_properties

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
