from enum import Enum


class CrownProfileModel(str, Enum):
    BETA = "beta"
    PURVES = "purves"

    def __str__(self) -> str:
        return str(self.value)
