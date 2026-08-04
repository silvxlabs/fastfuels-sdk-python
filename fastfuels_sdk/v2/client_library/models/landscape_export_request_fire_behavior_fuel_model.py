from enum import Enum


class LandscapeExportRequestFireBehaviorFuelModel(str, Enum):
    FBFM13 = "fbfm13"
    FBFM40 = "fbfm40"

    def __str__(self) -> str:
        return str(self.value)
