from enum import Enum


class TreeMapVersion(str, Enum):
    VALUE_0 = "2014"
    VALUE_1 = "2016"
    VALUE_2 = "2020"
    VALUE_3 = "2022"

    def __str__(self) -> str:
        return str(self.value)
