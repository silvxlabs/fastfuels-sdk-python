from enum import Enum


class LandfireFbfm13Version(str, Enum):
    VALUE_0 = "2023"
    VALUE_1 = "2024"

    def __str__(self) -> str:
        return str(self.value)
