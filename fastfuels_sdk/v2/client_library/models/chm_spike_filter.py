from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChmSpikeFilter")


@_attrs_define
class ChmSpikeFilter:
    """Removal of lone spurious returns from a point-cloud canopy height model.

    Under the default `max` aggregation a cell takes the tallest return that
    falls in it, so one bad return — a bird, haze, a multiple-time-around
    artifact — becomes the cell's height unless the cloud classified it as
    noise. Many do not.

    Such a return leaves a shape real canopy cannot: a single cell towering
    over everything around it. Both fields are the two halves of that shape, in
    meters, so they mean the same thing at any `alignment.resolution`. A `mean`,
    `median`, or `percentile` aggregation already resists a lone return, so this
    filter is aimed at the `max` case.

        Attributes:
            min_canopy_footprint_m (float | Unset): Narrowest ground footprint real canopy can occupy, in meters. A cell is
                judged against everything within this distance, and only a cell narrower than it can be rejected — so the filter
                does not run at all once `alignment.resolution` reaches this value, where one cell holds a stand rather than a
                crown. Default: 3.0.
            min_prominence_m (float | Unset): How far above every neighbour a cell must rise to be rejected, in meters.
                Measured noise returns stood 40-80 m above their surroundings; a real crown's peak is within a few meters of the
                cells beside it. Default: 25.0.
    """

    min_canopy_footprint_m: float | Unset = 3.0
    min_prominence_m: float | Unset = 25.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_canopy_footprint_m = self.min_canopy_footprint_m

        min_prominence_m = self.min_prominence_m

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if min_canopy_footprint_m is not UNSET:
            field_dict["min_canopy_footprint_m"] = min_canopy_footprint_m
        if min_prominence_m is not UNSET:
            field_dict["min_prominence_m"] = min_prominence_m

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        min_canopy_footprint_m = d.pop("min_canopy_footprint_m", UNSET)

        min_prominence_m = d.pop("min_prominence_m", UNSET)

        chm_spike_filter = cls(
            min_canopy_footprint_m=min_canopy_footprint_m,
            min_prominence_m=min_prominence_m,
        )

        chm_spike_filter.additional_properties = d
        return chm_spike_filter

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
