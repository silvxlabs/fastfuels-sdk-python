from enum import Enum


class CanopyBranchwoodSizePartition(str, Enum):
    BROWN_PROPORTIONS = "brown_proportions"
    EQUATIONS = "equations"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
