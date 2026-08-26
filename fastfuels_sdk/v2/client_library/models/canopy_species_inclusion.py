from enum import Enum


class CanopySpeciesInclusion(str, Enum):
    ALL_SPECIES = "all_species"
    FUELCALC_DEFAULT = "fuelcalc_default"

    def __str__(self) -> str:
        return str(self.value)
