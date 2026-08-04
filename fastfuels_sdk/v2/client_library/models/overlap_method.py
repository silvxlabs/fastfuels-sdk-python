from enum import Enum


class OverlapMethod(str, Enum):
    MAX = "max"
    MEAN = "mean"
    MIN = "min"

    def __str__(self) -> str:
        return str(self.value)
