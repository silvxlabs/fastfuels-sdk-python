from enum import Enum


class CanopyCrownWidthEquations(str, Enum):
    CROOKSTON_STAGE = "crookston_stage"
    PURVES = "purves"

    def __str__(self) -> str:
        return str(self.value)
