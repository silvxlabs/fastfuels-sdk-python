from enum import Enum


class CrownRadiusEstimator(str, Enum):
    AREA_EQUIVALENT = "area_equivalent"

    def __str__(self) -> str:
        return str(self.value)
