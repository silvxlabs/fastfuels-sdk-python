from enum import Enum


class PointProcess(str, Enum):
    INHOMOGENEOUS_POISSON = "inhomogeneous_poisson"

    def __str__(self) -> str:
        return str(self.value)
