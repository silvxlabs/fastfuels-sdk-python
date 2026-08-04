from enum import Enum


class LandfireFccsVersion(str, Enum):
    VALUE_0 = "2023"

    def __str__(self) -> str:
        return str(self.value)
