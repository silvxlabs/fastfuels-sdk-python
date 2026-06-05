from enum import Enum


class NonBurnableFuelModel(str, Enum):
    NB1 = "NB1"
    NB2 = "NB2"
    NB3 = "NB3"
    NB8 = "NB8"
    NB9 = "NB9"

    def __str__(self) -> str:
        return str(self.value)
