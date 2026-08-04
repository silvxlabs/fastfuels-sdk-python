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

from ..types import UNSET, Unset

T = TypeVar("T", bound="DuetMaxMinCalibrationTarget")


@_attrs_define
class DuetMaxMinCalibrationTarget:
    """Rescale a fuel type to a target maximum and minimum.

    Best when fuel data are limited, or when their distribution does not
    resemble DUET's.

        Attributes:
            max_ (float): Target maximum.
            method (Literal['maxmin'] | Unset):  Default: 'maxmin'.
            min_ (float | Unset): Target minimum. Default: 0.0.
    """

    max_: float
    method: Literal["maxmin"] | Unset = "maxmin"
    min_: float | Unset = 0.0

    def to_dict(self) -> dict[str, Any]:
        max_ = self.max_

        method = self.method

        min_ = self.min_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "max": max_,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method
        if min_ is not UNSET:
            field_dict["min"] = min_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        max_ = d.pop("max")

        method = cast(Literal["maxmin"] | Unset, d.pop("method", UNSET))
        if method != "maxmin" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'maxmin', got '{method}'")

        min_ = d.pop("min", UNSET)

        duet_max_min_calibration_target = cls(
            max_=max_,
            method=method,
            min_=min_,
        )

        return duet_max_min_calibration_target
