from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.three_dep_resolution import ThreeDepResolution
from ..types import UNSET, Unset

T = TypeVar("T", bound="ThreeDepCoverageResponse")


@_attrs_define
class ThreeDepCoverageResponse:
    """Response model for 3DEP tile coverage pre-flight check.

    Attributes:
        resolution (ThreeDepResolution): Available resolutions for 3DEP data (meters).
        available (bool):
        tile_count (int):
        tiles (list[str]):
        acquisition_dates (list[str] | None | Unset):
    """

    resolution: ThreeDepResolution
    available: bool
    tile_count: int
    tiles: list[str]
    acquisition_dates: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resolution = self.resolution.value

        available = self.available

        tile_count = self.tile_count

        tiles = self.tiles

        acquisition_dates: list[str] | None | Unset
        if isinstance(self.acquisition_dates, Unset):
            acquisition_dates = UNSET
        elif isinstance(self.acquisition_dates, list):
            acquisition_dates = self.acquisition_dates

        else:
            acquisition_dates = self.acquisition_dates

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resolution": resolution,
                "available": available,
                "tile_count": tile_count,
                "tiles": tiles,
            }
        )
        if acquisition_dates is not UNSET:
            field_dict["acquisition_dates"] = acquisition_dates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resolution = ThreeDepResolution(d.pop("resolution"))

        available = d.pop("available")

        tile_count = d.pop("tile_count")

        tiles = cast(list[str], d.pop("tiles"))

        def _parse_acquisition_dates(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                acquisition_dates_type_0 = cast(list[str], data)

                return acquisition_dates_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        acquisition_dates = _parse_acquisition_dates(d.pop("acquisition_dates", UNSET))

        three_dep_coverage_response = cls(
            resolution=resolution,
            available=available,
            tile_count=tile_count,
            tiles=tiles,
            acquisition_dates=acquisition_dates,
        )

        three_dep_coverage_response.additional_properties = d
        return three_dep_coverage_response

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
