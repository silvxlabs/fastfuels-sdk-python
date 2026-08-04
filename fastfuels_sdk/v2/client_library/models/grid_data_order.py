from enum import Enum


class GridDataOrder(str, Enum):
    C = "C"
    F = "F"

    def __str__(self) -> str:
        return str(self.value)
