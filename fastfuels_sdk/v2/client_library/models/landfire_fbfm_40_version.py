from enum import Enum


class LandfireFbfm40Version(str, Enum):
    VALUE_0 = "2019"
    VALUE_1 = "2020"
    VALUE_2 = "2022"
    VALUE_3 = "2023"
    VALUE_4 = "2024"
    VALUE_5 = "2025"

    def __str__(self) -> str:
        return str(self.value)
