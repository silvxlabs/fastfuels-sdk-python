from enum import Enum


class GridDataArrayFormat(str, Enum):
    DENSE = "dense"
    SPARSE = "sparse"

    def __str__(self) -> str:
        return str(self.value)
