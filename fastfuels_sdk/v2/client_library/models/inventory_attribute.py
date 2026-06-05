from enum import Enum


class InventoryAttribute(str, Enum):
    CROWN_RATIO = "crown_ratio"
    DBH = "dbh"
    FIA_SPECIES_CODE = "fia_species_code"
    HEIGHT = "height"

    def __str__(self) -> str:
        return str(self.value)
