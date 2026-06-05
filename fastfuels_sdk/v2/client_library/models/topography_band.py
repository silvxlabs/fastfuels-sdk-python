from enum import Enum


class TopographyBand(str, Enum):
    ASPECT = "aspect"
    ELEVATION = "elevation"
    SLOPE = "slope"

    def __str__(self) -> str:
        return str(self.value)
