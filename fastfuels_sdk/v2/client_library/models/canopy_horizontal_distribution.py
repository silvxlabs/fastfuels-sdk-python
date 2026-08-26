from enum import Enum


class CanopyHorizontalDistribution(str, Enum):
    CROWN_PROJECTED = "crown_projected"
    STEM = "stem"

    def __str__(self) -> str:
        return str(self.value)
