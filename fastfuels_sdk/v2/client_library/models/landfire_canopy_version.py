from enum import Enum


class LandfireCanopyVersion(str, Enum):
    VALUE_0 = "2024"

    def __str__(self) -> str:
        return str(self.value)
