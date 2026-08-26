from enum import Enum


class RelativeElevation(str, Enum):
    ABOVE = "above"
    BELOW = "below"
    NEAR = "near"

    def __str__(self) -> str:
        return str(self.value)
