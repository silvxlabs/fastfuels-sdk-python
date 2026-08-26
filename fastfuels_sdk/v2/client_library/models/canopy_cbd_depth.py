from enum import Enum


class CanopyCbdDepth(str, Enum):
    BIOMASS_PERCENTILE = "biomass_percentile"
    CANOPY_DEPTH = "canopy_depth"
    HEIGHT_PERCENTILE = "height_percentile"
    MEAN_CROWN_LENGTH = "mean_crown_length"

    def __str__(self) -> str:
        return str(self.value)
