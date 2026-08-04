from enum import IntEnum


class ThreeDepResolution(IntEnum):
    VALUE_1 = 1
    VALUE_10 = 10
    VALUE_30 = 30

    def __str__(self) -> str:
        return str(self.value)
