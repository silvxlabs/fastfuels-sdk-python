from enum import Enum


class CrownProfileModel(str, Enum):
    BETA = "beta"
    CONE = "cone"
    CYLINDER = "cylinder"
    DUAL_ELLIPSOID = "dual_ellipsoid"
    DUAL_PARABOLOID = "dual_paraboloid"
    PURVES = "purves"
    SINGLE_ELLIPSOID = "single_ellipsoid"
    SINGLE_PARABOLOID = "single_paraboloid"

    @classmethod
    def _missing_(cls, value: object) -> "CrownProfileModel | None":
        """Parse a value this SDK version doesn't know as an ``UNKNOWN`` member
        that keeps the value, so new API values don't break older SDKs."""
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = "UNKNOWN"
        member._value_ = value
        return member

    def __str__(self) -> str:
        return str(self.value)
