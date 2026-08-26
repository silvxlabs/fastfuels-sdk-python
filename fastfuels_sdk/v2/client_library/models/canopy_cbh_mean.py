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

T = TypeVar("T", bound="CanopyCbhMean")


@_attrs_define
class CanopyCbhMean:
    """CBH as the mean of the per-tree crown base heights in each cell.

    Van Wagner's (1977) stand-mean definition — a plain summary of the
    per-tree crown bases (`height * (1 - crown_ratio)`), one tree one vote
    unless `weight_by_available_fuel` is set. A distinct convention from
    the `bulk_density_threshold` profile method; the two diverge where tree
    height varies within a cell.

        Attributes:
            method (Literal['mean'] | Unset):  Default: 'mean'.
            weight_by_available_fuel (bool | Unset): Weight the mean by each tree's available canopy fuel so heavier crowns
                pull it, rather than one tree one vote. Van Wagner's original mean is unweighted (the default). Default: False.
    """

    method: Literal["mean"] | Unset = "mean"
    weight_by_available_fuel: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        weight_by_available_fuel = self.weight_by_available_fuel

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if weight_by_available_fuel is not UNSET:
            field_dict["weight_by_available_fuel"] = weight_by_available_fuel

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["mean"] | Unset, d.pop("method", UNSET))
        if method != "mean" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'mean', got '{method}'")

        weight_by_available_fuel = d.pop("weight_by_available_fuel", UNSET)

        canopy_cbh_mean = cls(
            method=method,
            weight_by_available_fuel=weight_by_available_fuel,
        )

        return canopy_cbh_mean
