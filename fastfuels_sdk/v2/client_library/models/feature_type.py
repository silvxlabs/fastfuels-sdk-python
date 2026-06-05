from enum import Enum


class FeatureType(str, Enum):
    LAYERSET = "layerset"
    ROAD = "road"
    WATER = "water"

    def __str__(self) -> str:
        return str(self.value)
