from enum import Enum


class LandfireTopographyVersion(str, Enum):
    VALUE_0 = "2020"

    def __str__(self) -> str:
        return str(self.value)
