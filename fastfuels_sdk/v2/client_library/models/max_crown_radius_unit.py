from enum import Enum


class MaxCrownRadiusUnit(str, Enum):
    M = "m"

    def __str__(self) -> str:
        return str(self.value)
