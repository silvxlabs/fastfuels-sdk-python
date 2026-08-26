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

from ..models.canopy_cbd_depth import CanopyCbdDepth
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanopyCbdLoadOverDepth")


@_attrs_define
class CanopyCbdLoadOverDepth:
    """CBD as canopy fuel load divided by a canopy depth.

    The van Wagner-consistent average-density convention (load over
    depth). Produces systematically lower values than the running-mean
    maximum. Cruz et al. (2003) used this convention with
    `mean_crown_length` as the depth and foliage-only available fuel.

        Attributes:
            method (Literal['load_over_depth'] | Unset):  Default: 'load_over_depth'.
            depth (CanopyCbdDepth | Unset): Depth definitions for the load-over-depth CBD method.

                `canopy_depth` is chm - cbh (the van Wagner convention), computed from
                the requested `cbh`/`chm` threshold settings — those bands must be
                requested with the `bulk_density_threshold` method so the depth's
                definition is recorded on the grid. `mean_crown_length` is the mean of
                per-tree crown lengths (the depth Cruz et al. 2003 used).
                `biomass_percentile` is the height span holding the central 80% of
                canopy biomass (10th to 90th percentile; Albini 1996).
                `height_percentile` is the 90th-percentile tree height minus the
                median crown base height.
    """

    method: Literal["load_over_depth"] | Unset = "load_over_depth"
    depth: CanopyCbdDepth | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        depth: str | Unset = UNSET
        if not isinstance(self.depth, Unset):
            depth = self.depth.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if depth is not UNSET:
            field_dict["depth"] = depth

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["load_over_depth"] | Unset, d.pop("method", UNSET))
        if method != "load_over_depth" and not isinstance(method, Unset):
            raise ValueError(
                f"method must match const 'load_over_depth', got '{method}'"
            )

        _depth = d.pop("depth", UNSET)
        depth: CanopyCbdDepth | Unset
        if isinstance(_depth, Unset):
            depth = UNSET
        else:
            depth = CanopyCbdDepth(_depth)

        canopy_cbd_load_over_depth = cls(
            method=method,
            depth=depth,
        )

        return canopy_cbd_load_over_depth
