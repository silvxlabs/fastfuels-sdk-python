from enum import Enum


class TreeBand(str, Enum):
    BULK_DENSITY_BRANCHWOOD_DEAD = "bulk_density.branchwood.dead"
    BULK_DENSITY_BRANCHWOOD_LIVE = "bulk_density.branchwood.live"
    BULK_DENSITY_FINE_DEAD = "bulk_density.fine.dead"
    BULK_DENSITY_FINE_LIVE = "bulk_density.fine.live"
    BULK_DENSITY_FOLIAGE_DEAD = "bulk_density.foliage.dead"
    BULK_DENSITY_FOLIAGE_LIVE = "bulk_density.foliage.live"
    FUEL_MOISTURE_DEAD = "fuel_moisture.dead"
    FUEL_MOISTURE_LIVE = "fuel_moisture.live"
    SAVR_FOLIAGE = "savr.foliage"
    SPCD = "spcd"
    TREE_ID = "tree_id"
    VOLUME_FRACTION = "volume_fraction"

    def __str__(self) -> str:
        return str(self.value)
