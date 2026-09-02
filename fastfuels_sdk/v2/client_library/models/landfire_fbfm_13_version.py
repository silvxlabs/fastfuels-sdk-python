from enum import Enum


class LandfireFbfm13Version(str, Enum):
    VALUE_0 = "2023"
    VALUE_1 = "2024"
    VALUE_2 = "2025"

    def __str__(self) -> str:
        return str(self.value)
