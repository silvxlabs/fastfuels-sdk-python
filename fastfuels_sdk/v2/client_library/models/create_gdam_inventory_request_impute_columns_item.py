from enum import Enum


class CreateGdamInventoryRequestImputeColumnsItem(str, Enum):
    CROWN_RATIO = "crown_ratio"
    DBH = "dbh"
    FIA_SPECIES_CODE = "fia_species_code"

    def __str__(self) -> str:
        return str(self.value)
