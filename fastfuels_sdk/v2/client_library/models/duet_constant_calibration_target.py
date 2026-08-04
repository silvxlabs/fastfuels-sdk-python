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

T = TypeVar("T", bound="DuetConstantCalibrationTarget")


@_attrs_define
class DuetConstantCalibrationTarget:
    """Assign a single value to every fuel-bearing cell.

    Reasonable only when that value is the only one available.

        Attributes:
            value (float): Target value.
            method (Literal['constant'] | Unset):  Default: 'constant'.
    """

    value: float
    method: Literal["constant"] | Unset = "constant"

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        method = self.method

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "value": value,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        value = d.pop("value")

        method = cast(Literal["constant"] | Unset, d.pop("method", UNSET))
        if method != "constant" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'constant', got '{method}'")

        duet_constant_calibration_target = cls(
            value=value,
            method=method,
        )

        return duet_constant_calibration_target
