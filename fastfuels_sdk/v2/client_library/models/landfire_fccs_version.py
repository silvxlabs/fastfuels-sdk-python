from enum import Enum


class LandfireFccsVersion(str, Enum):
    VALUE_0 = "2023"
    VALUE_1 = "2025"

    def __str__(self) -> str:
        return str(self.value)
