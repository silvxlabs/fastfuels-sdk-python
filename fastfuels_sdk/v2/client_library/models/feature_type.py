from enum import Enum


class FeatureType(str, Enum):
    BUILDING = "building"
    CROWN = "crown"
    LAYERSET = "layerset"
    ROAD = "road"
    WATER = "water"

    def __str__(self) -> str:
        return str(self.value)
