from enum import Enum


class InventoryCrownSpacingRank(str, Enum):
    DBH = "dbh"
    HEIGHT = "height"

    def __str__(self) -> str:
        return str(self.value)
