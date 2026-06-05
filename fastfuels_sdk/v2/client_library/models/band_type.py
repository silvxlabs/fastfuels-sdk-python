from enum import Enum


class BandType(str, Enum):
    CATEGORICAL = "categorical"
    CONTINUOUS = "continuous"

    def __str__(self) -> str:
        return str(self.value)
