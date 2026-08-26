from enum import Enum


class CanopyVerticalDistribution(str, Enum):
    REINHARDT_2006 = "reinhardt_2006"
    UNIFORM = "uniform"

    def __str__(self) -> str:
        return str(self.value)
