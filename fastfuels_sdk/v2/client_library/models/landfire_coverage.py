from enum import Enum


class LandfireCoverage(str, Enum):
    FULL = "full"
    NONE = "none"
    PARTIAL = "partial"
    UNPUBLISHED = "unpublished"

    def __str__(self) -> str:
        return str(self.value)
