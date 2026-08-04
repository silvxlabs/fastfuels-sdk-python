from enum import Enum


class BiomassUnit(str, Enum):
    KG = "kg"

    def __str__(self) -> str:
        return str(self.value)
