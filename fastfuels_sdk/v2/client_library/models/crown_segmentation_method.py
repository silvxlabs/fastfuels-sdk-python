from enum import Enum


class CrownSegmentationMethod(str, Enum):
    DALPONTE2016 = "dalponte2016"

    def __str__(self) -> str:
        return str(self.value)
