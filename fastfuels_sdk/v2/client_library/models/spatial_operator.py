from enum import Enum


class SpatialOperator(str, Enum):
    INTERSECTS = "intersects"
    OUTSIDE = "outside"
    WITHIN = "within"

    def __str__(self) -> str:
        return str(self.value)
