"""Tests for v2 calibration builders."""

import pytest

from fastfuels_sdk.v2.calibrations import duet_calibration
from fastfuels_sdk.v2.client_library.models import (
    DuetConstantCalibrationTarget,
    DuetMaxMinCalibrationTarget,
    DuetMeanSdCalibrationTarget,
)


def test_duet_calibration_builds_each_target_method():
    calibration = duet_calibration(
        fuel_load={
            "grass": {"mean": 0.5, "sd": 0.25},
            "litter": {"max": 5.0},
        },
        fuel_depth={"all": {"value": 0.3}},
    )

    assert isinstance(calibration.fuel_load.grass, DuetMeanSdCalibrationTarget)
    assert isinstance(calibration.fuel_load.litter, DuetMaxMinCalibrationTarget)
    assert calibration.fuel_load.litter.min_ == 0.0
    assert isinstance(calibration.fuel_depth.all_, DuetConstantCalibrationTarget)
    assert calibration.to_dict() == {
        "fuel_load": {
            "grass": {"method": "meansd", "mean": 0.5, "sd": 0.25},
            "litter": {"method": "maxmin", "max": 5.0, "min": 0.0},
        },
        "fuel_depth": {
            "all": {"method": "constant", "value": 0.3},
        },
    }


def test_duet_calibration_accepts_explicit_method():
    calibration = duet_calibration(
        fuel_moisture={
            "grass": {"method": "constant", "value": 12},
        }
    )

    assert calibration.fuel_moisture.grass.value == 12


def test_duet_calibration_requires_a_parameter():
    with pytest.raises(ValueError, match="at least one"):
        duet_calibration()


def test_duet_calibration_all_is_exclusive():
    with pytest.raises(ValueError, match="cannot be combined"):
        duet_calibration(
            fuel_load={
                "all": {"value": 1},
                "grass": {"value": 1},
            }
        )


def test_duet_calibration_litter_is_exclusive_of_components():
    with pytest.raises(ValueError, match="litter"):
        duet_calibration(
            fuel_load={
                "litter": {"value": 1},
                "coniferous": {"value": 1},
            }
        )


@pytest.mark.parametrize(
    "target,match",
    [
        ({"method": "unknown", "value": 1}, "Unknown calibration method"),
        ({"mean": 1}, "missing required fields"),
        ({"max": 1, "min": 2}, "greater than or equal"),
        ({"value": -1}, "nonnegative"),
        ({"value": 1, "max": 2}, "not used"),
    ],
)
def test_duet_calibration_rejects_invalid_targets(target, match):
    with pytest.raises(ValueError, match=match):
        duet_calibration(fuel_load={"grass": target})
