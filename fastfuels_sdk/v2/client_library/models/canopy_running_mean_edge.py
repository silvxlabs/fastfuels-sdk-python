from enum import Enum


class CanopyRunningMeanEdge(str, Enum):
    FIXED_DEPTH = "fixed_depth"
    GROUND_CLAMPED = "ground_clamped"
    TRUNCATED = "truncated"

    def __str__(self) -> str:
        return str(self.value)
