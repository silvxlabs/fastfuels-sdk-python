from enum import Enum


class LandfireDisturbanceVersion(str, Enum):
    VALUE_0 = "2025"

    def __str__(self) -> str:
        return str(self.value)
