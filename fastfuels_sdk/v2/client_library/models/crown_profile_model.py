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

    def __str__(self) -> str:
        return str(self.value)
