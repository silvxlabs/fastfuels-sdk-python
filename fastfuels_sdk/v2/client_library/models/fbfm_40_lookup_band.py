from enum import Enum


class Fbfm40LookupBand(str, Enum):
    FUEL_DEPTH = "fuel_depth"
    FUEL_LOAD_100HR = "fuel_load.100hr"
    FUEL_LOAD_10HR = "fuel_load.10hr"
    FUEL_LOAD_1HR = "fuel_load.1hr"
    FUEL_LOAD_LIVE_HERB = "fuel_load.live_herb"
    FUEL_LOAD_LIVE_WOODY = "fuel_load.live_woody"
    SAVR_100HR = "savr.100hr"
    SAVR_10HR = "savr.10hr"
    SAVR_1HR = "savr.1hr"
    SAVR_LIVE_HERB = "savr.live_herb"
    SAVR_LIVE_WOODY = "savr.live_woody"

    def __str__(self) -> str:
        return str(self.value)
