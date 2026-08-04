"""Calibration builders for generated v2 request models."""

from collections.abc import Mapping
from numbers import Real

from fastfuels_sdk.v2.client_library.models import (
    DuetCalibration,
    DuetConstantCalibrationTarget,
    DuetMaxMinCalibrationTarget,
    DuetMeanSdCalibrationTarget,
    DuetParameterCalibration,
)
from fastfuels_sdk.v2.client_library.types import UNSET

__all__ = ["duet_calibration"]

_DUET_FUEL_TYPES = {"grass", "coniferous", "deciduous", "litter", "all"}
_DUET_TARGET_TYPES = (
    DuetConstantCalibrationTarget,
    DuetMaxMinCalibrationTarget,
    DuetMeanSdCalibrationTarget,
)


def duet_calibration(
    *,
    fuel_load=None,
    fuel_depth=None,
    fuel_moisture=None,
) -> DuetCalibration:
    """Build calibration targets for a DUET surface-fuel grid.

    Each argument maps fuel types (``"grass"``, ``"coniferous"``,
    ``"deciduous"``, ``"litter"``, or ``"all"``) to a target. Target fields
    select the calibration method: ``value`` for constant, ``max`` and
    optional ``min`` for max-min, or ``mean`` and ``sd`` for mean-standard
    deviation. An explicit ``method`` field is also accepted.

    Parameters
    ----------
    fuel_load : mapping, optional
        Per-fuel-type load targets.
    fuel_depth : mapping, optional
        Per-fuel-type depth targets.
    fuel_moisture : mapping, optional
        Per-fuel-type moisture targets.

    Returns
    -------
    DuetCalibration
        Calibration for
        :func:`fastfuels_sdk.v2.grids.create_surface_fuel_grid_from_duet`.

    Raises
    ------
    TypeError
        If a parameter or target is not a mapping or generated target model.
    ValueError
        If no parameter is provided, a target is invalid, or mutually
        exclusive fuel types are combined.

    Examples
    --------
    >>> import fastfuels_sdk.v2 as ff
    >>> calibration = ff.duet_calibration(
    ...     fuel_load={
    ...         "grass": {"mean": 0.5, "sd": 0.25},
    ...         "litter": {"max": 5.0, "min": 0.0},
    ...     },
    ...     fuel_depth={
    ...         "grass": {"value": 0.3},
    ...         "litter": {"value": 0.06},
    ...     },
    ... )
    """
    parameters = {
        "fuel_load": fuel_load,
        "fuel_depth": fuel_depth,
        "fuel_moisture": fuel_moisture,
    }
    if not any(value is not None for value in parameters.values()):
        raise ValueError(
            "duet_calibration requires at least one of fuel_load, fuel_depth, "
            "or fuel_moisture."
        )

    return DuetCalibration(
        **{
            name: _duet_parameter(value, name) if value is not None else UNSET
            for name, value in parameters.items()
        }
    )


def _duet_parameter(value, parameter: str) -> DuetParameterCalibration:
    if isinstance(value, DuetParameterCalibration):
        value = value.to_dict()
    if not isinstance(value, Mapping):
        raise TypeError(f"{parameter} must be a mapping of fuel types to targets.")
    if not value:
        raise ValueError(f"{parameter} requires at least one fuel-type target.")

    unknown = set(value) - _DUET_FUEL_TYPES
    if unknown:
        raise ValueError(
            f"Unknown {parameter} fuel types: {sorted(unknown)}. Use one of "
            f"{sorted(_DUET_FUEL_TYPES)}."
        )
    if "all" in value and len(value) > 1:
        raise ValueError(
            f"{parameter} 'all' cannot be combined with per-fuel-type targets."
        )
    if "litter" in value and ({"coniferous", "deciduous"} & set(value)):
        raise ValueError(
            f"{parameter} 'litter' cannot be combined with 'coniferous' or "
            "'deciduous'."
        )

    targets = {
        name: _duet_target(target, f"{parameter}.{name}")
        for name, target in value.items()
    }
    if "all" in targets:
        targets["all_"] = targets.pop("all")
    return DuetParameterCalibration(**targets)


def _duet_target(value, path: str):
    if isinstance(value, _DUET_TARGET_TYPES):
        value = value.to_dict()
    if not isinstance(value, Mapping):
        raise TypeError(f"{path} must be a calibration-target mapping.")

    data = dict(value)
    method = data.pop("method", None)
    if method is None:
        method = _infer_duet_method(data, path)

    if method == "constant":
        _require_fields(data, path, required={"value"})
        return DuetConstantCalibrationTarget(value=_nonnegative(data["value"], path))
    if method == "maxmin":
        _require_fields(data, path, required={"max"}, optional={"min"})
        maximum = _nonnegative(data["max"], f"{path}.max")
        minimum = _nonnegative(data.get("min", 0.0), f"{path}.min")
        if maximum < minimum:
            raise ValueError(f"{path}.max must be greater than or equal to min.")
        return DuetMaxMinCalibrationTarget(max_=maximum, min_=minimum)
    if method == "meansd":
        _require_fields(data, path, required={"mean", "sd"})
        return DuetMeanSdCalibrationTarget(
            mean=_nonnegative(data["mean"], f"{path}.mean"),
            sd=_nonnegative(data["sd"], f"{path}.sd"),
        )
    raise ValueError(
        f"Unknown calibration method {method!r} for {path}. Use 'constant', "
        "'maxmin', or 'meansd'."
    )


def _infer_duet_method(data: Mapping, path: str) -> str:
    fields = set(data)
    if "value" in fields:
        return "constant"
    if fields & {"max", "min"}:
        return "maxmin"
    if fields & {"mean", "sd"}:
        return "meansd"
    raise ValueError(
        f"Cannot infer a calibration method for {path}; provide value, max, "
        "or mean and sd."
    )


def _require_fields(
    data: Mapping,
    path: str,
    *,
    required: set[str],
    optional: set[str] | None = None,
) -> None:
    optional = optional or set()
    missing = required - set(data)
    if missing:
        raise ValueError(f"{path} is missing required fields: {sorted(missing)}.")
    extra = set(data) - required - optional
    if extra:
        raise ValueError(f"{path} has fields not used by this method: {sorted(extra)}.")


def _nonnegative(value, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{path} must be a number.")
    if value < 0:
        raise ValueError(f"{path} must be nonnegative.")
    return float(value)
