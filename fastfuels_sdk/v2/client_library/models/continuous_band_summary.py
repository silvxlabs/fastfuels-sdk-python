from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ContinuousBandSummary")


@_attrs_define
class ContinuousBandSummary:
    """
    Attributes:
        type_ (Literal['continuous']):
        count (int):
        nodata_count (int):
        min_ (float | None):
        max_ (float | None):
        mean (float | None):
        std (float | None):
    """

    type_: Literal["continuous"]
    count: int
    nodata_count: int
    min_: float | None
    max_: float | None
    mean: float | None
    std: float | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        count = self.count

        nodata_count = self.nodata_count

        min_: float | None
        min_ = self.min_

        max_: float | None
        max_ = self.max_

        mean: float | None
        mean = self.mean

        std: float | None
        std = self.std

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "count": count,
                "nodata_count": nodata_count,
                "min": min_,
                "max": max_,
                "mean": mean,
                "std": std,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = cast(Literal["continuous"], d.pop("type"))
        if type_ != "continuous":
            raise ValueError(f"type must match const 'continuous', got '{type_}'")

        count = d.pop("count")

        nodata_count = d.pop("nodata_count")

        def _parse_min_(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        min_ = _parse_min_(d.pop("min"))

        def _parse_max_(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        max_ = _parse_max_(d.pop("max"))

        def _parse_mean(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        mean = _parse_mean(d.pop("mean"))

        def _parse_std(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        std = _parse_std(d.pop("std"))

        continuous_band_summary = cls(
            type_=type_,
            count=count,
            nodata_count=nodata_count,
            min_=min_,
            max_=max_,
            mean=mean,
            std=std,
        )

        continuous_band_summary.additional_properties = d
        return continuous_band_summary

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
