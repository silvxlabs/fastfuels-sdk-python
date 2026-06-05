from enum import Enum


class BiomassComponent(str, Enum):
    BRANCHWOOD = "branchwood"
    FINE = "fine"
    FOLIAGE = "foliage"

    def __str__(self) -> str:
        return str(self.value)
