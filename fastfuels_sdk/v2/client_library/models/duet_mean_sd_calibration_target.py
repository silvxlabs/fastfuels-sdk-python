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

T = TypeVar("T", bound="DuetMeanSdCalibrationTarget")


@_attrs_define
class DuetMeanSdCalibrationTarget:
    """Rescale a fuel type to a target mean and standard deviation.

    Appropriate only when the targets come from a dataset large enough to
    approximate a normal distribution.

        Attributes:
            mean (float): Target mean.
            sd (float): Target standard deviation.
            method (Literal['meansd'] | Unset):  Default: 'meansd'.
    """

    mean: float
    sd: float
    method: Literal["meansd"] | Unset = "meansd"

    def to_dict(self) -> dict[str, Any]:
        mean = self.mean

        sd = self.sd

        method = self.method

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mean": mean,
                "sd": sd,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        mean = d.pop("mean")

        sd = d.pop("sd")

        method = cast(Literal["meansd"] | Unset, d.pop("method", UNSET))
        if method != "meansd" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'meansd', got '{method}'")

        duet_mean_sd_calibration_target = cls(
            mean=mean,
            sd=sd,
            method=method,
        )

        return duet_mean_sd_calibration_target
