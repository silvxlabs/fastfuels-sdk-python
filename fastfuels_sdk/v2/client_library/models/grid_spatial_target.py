from enum import Enum


class GridSpatialTarget(str, Enum):
    CELL = "cell"
    CENTROID = "centroid"

    def __str__(self) -> str:
        return str(self.value)
