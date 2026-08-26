from enum import Enum


class LeafluxBand(str, Enum):
    IRRADIANCE_CANOPY_RELATIVE = "irradiance.canopy.relative"
    IRRADIANCE_SURFACE_RELATIVE = "irradiance.surface.relative"

    def __str__(self) -> str:
        return str(self.value)
