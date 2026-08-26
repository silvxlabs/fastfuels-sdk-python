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

T = TypeVar("T", bound="CanopyCbdRunningMean")


@_attrs_define
class CanopyCbdRunningMean:
    """CBD as the maximum of a running mean of the vertical fuel profile.

    The effective-CBD convention used by FuelCalc, FFE-FVS, and NEXUS.
    Published window depths vary by implementation: 1.524 m (5 ft, the
    FuelCalc 1.7 User Guide; its Appendix D reads unsmoothed layers, i.e.
    `null`), 3.9624 m (13 ft, FFE-FVS), 4.572 m (15 ft, the original
    FuelCalc method in RMRS-P-41; early NEXUS used 4.5 m), and 3.0 m
    (Reinhardt et al. 2006; current NEXUS). The default 3.0 m follows
    Reinhardt et al. (2006).

        Attributes:
            method (Literal['maximum_running_mean'] | Unset):  Default: 'maximum_running_mean'.
            window (float | None | Unset): Running-mean window depth in meters, rounded internally to a whole number of
                profile layers. `null` disables smoothing, making CBD the maximum single-layer value. Default: 3.0.
            edge (CanopyRunningMeanEdge | Unset): What a running mean takes to lie past the ends of the profile.

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

    method: Literal["maximum_running_mean"] | Unset = "maximum_running_mean"
    window: float | None | Unset = 3.0
    edge: CanopyRunningMeanEdge | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        window: float | None | Unset
        if isinstance(self.window, Unset):
            window = UNSET
        else:
            window = self.window

        edge: str | Unset = UNSET
        if not isinstance(self.edge, Unset):
            edge = self.edge.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if window is not UNSET:
            field_dict["window"] = window
        if edge is not UNSET:
            field_dict["edge"] = edge

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = cast(Literal["maximum_running_mean"] | Unset, d.pop("method", UNSET))
        if method != "maximum_running_mean" and not isinstance(method, Unset):
            raise ValueError(
                f"method must match const 'maximum_running_mean', got '{method}'"
            )

        def _parse_window(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        window = _parse_window(d.pop("window", UNSET))

        _edge = d.pop("edge", UNSET)
        edge: CanopyRunningMeanEdge | Unset
        if isinstance(_edge, Unset):
            edge = UNSET
        else:
            edge = CanopyRunningMeanEdge(_edge)

        canopy_cbd_running_mean = cls(
            method=method,
            window=window,
            edge=edge,
        )

        return canopy_cbd_running_mean
