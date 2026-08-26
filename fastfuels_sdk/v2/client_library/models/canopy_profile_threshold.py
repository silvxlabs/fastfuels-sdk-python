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

from ..models.canopy_running_mean_edge import CanopyRunningMeanEdge
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanopyProfileThreshold")


@_attrs_define
class CanopyProfileThreshold:
    """A height where the vertical fuel profile crosses a bulk-density threshold.

    Shared by `cbh` (lowest crossing) and `chm` (highest crossing), so the
    two bands are consistent by construction (cbh <= chm). The effective
    threshold is ``min(relative_threshold_fraction * CBD_max, threshold)``
    — FuelCalc's rule, in which the relative branch engages whenever the
    cell's maximum profile density is below threshold / fraction (0.12
    kg/m**3 at the defaults). `CBD_max` is the maximum of the profile
    this method scans, so `smoothing_window` changes it; it is
    independent of the `cbd` band's own window, which is a separate
    setting.

        Attributes:
            method (Literal['bulk_density_threshold'] | Unset):  Default: 'bulk_density_threshold'.
            threshold (float | Unset): Bulk-density threshold ceiling in kg/m**3. Default 0.012, the FuelCalc value, also
                used by LANDFIRE to define canopy base height. Published alternatives: 0.011 (Scott & Reinhardt 2001 / FFE-FVS,
                30 lb/acre/ft), 0.037 (Sando & Wick 1972, 100 lb/acre/ft), 0.074 (Williams 1977). Default: 0.012.
            relative_threshold_fraction (float | None | Unset): Fraction of the cell's maximum profile density used as the
                threshold when that is lower than `threshold`. `null` applies `threshold` flat, with no relative branch.
                Default: 0.1.
            smoothing_window (float | None | Unset): Running-mean window in meters applied to the profile before locating
                threshold crossings. `null` reads raw layers. FuelCalc 1.7 crosses a 1.524 m (5 ft) running mean, the same
                window it reduces CBD over; FFE-FVS crosses 0.9144 m (3 ft); the original FuelCalc method (RMRS-P-41) crosses
                its full 4.572 m (15 ft) window.
            smoothing_edge (CanopyRunningMeanEdge | Unset): What a running mean takes to lie past the ends of the profile.

                The three answers in use agree everywhere except the lowest and
                highest few layers, which is exactly where the threshold heights are
                read, so the choice can move a reported `cbh` or `chm` by a layer
                and shift `cbd` in a canopy that reaches the ground.

                `fixed_depth` divides by the window depth at every height, padding
                with zeros at both ends, so a slab of fuel reports the same bulk
                density wherever it sits — the reading Reinhardt et al. (2006)
                define. `ground_clamped` shortens the window where it would run
                below the ground and divides by what it actually covered, while
                still dividing by the full depth above the canopy; this is
                FuelCalc's, and it concentrates density against the ground while
                letting it fall away above the crowns. `truncated` divides by
                whatever the window covered at either end, which is FFE-FVS's and
                inflates the topmost layers.
    """

    method: Literal["bulk_density_threshold"] | Unset = "bulk_density_threshold"
    threshold: float | Unset = 0.012
    relative_threshold_fraction: float | None | Unset = 0.1
    smoothing_window: float | None | Unset = UNSET
    smoothing_edge: CanopyRunningMeanEdge | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        threshold = self.threshold

        relative_threshold_fraction: float | None | Unset
        if isinstance(self.relative_threshold_fraction, Unset):
            relative_threshold_fraction = UNSET
        else:
            relative_threshold_fraction = self.relative_threshold_fraction

        smoothing_window: float | None | Unset
        if isinstance(self.smoothing_window, Unset):
            smoothing_window = UNSET
        else:
            smoothing_window = self.smoothing_window

        smoothing_edge: str | Unset = UNSET
        if not isinstance(self.smoothing_edge, Unset):
            smoothing_edge = self.smoothing_edge.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if threshold is not UNSET:
            field_dict["threshold"] = threshold
        if relative_threshold_fraction is not UNSET:
            field_dict["relative_threshold_fraction"] = relative_threshold_fraction
        if smoothing_window is not UNSET:
            field_dict["smoothing_window"] = smoothing_window
        if smoothing_edge is not UNSET:
            field_dict["smoothing_edge"] = smoothing_edge

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["bulk_density_threshold"] | Unset, d.pop("method", UNSET))
        if method != "bulk_density_threshold" and not isinstance(method, Unset):
            raise ValueError(
                f"method must match const 'bulk_density_threshold', got '{method}'"
            )

        threshold = d.pop("threshold", UNSET)

        def _parse_relative_threshold_fraction(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        relative_threshold_fraction = _parse_relative_threshold_fraction(
            d.pop("relative_threshold_fraction", UNSET)
        )

        def _parse_smoothing_window(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        smoothing_window = _parse_smoothing_window(d.pop("smoothing_window", UNSET))

        _smoothing_edge = d.pop("smoothing_edge", UNSET)
        smoothing_edge: CanopyRunningMeanEdge | Unset
        if isinstance(_smoothing_edge, Unset):
            smoothing_edge = UNSET
        else:
            smoothing_edge = CanopyRunningMeanEdge(_smoothing_edge)

        canopy_profile_threshold = cls(
            method=method,
            threshold=threshold,
            relative_threshold_fraction=relative_threshold_fraction,
            smoothing_window=smoothing_window,
            smoothing_edge=smoothing_edge,
        )

        return canopy_profile_threshold
