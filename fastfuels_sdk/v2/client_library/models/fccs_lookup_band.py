from enum import Enum


class FccsLookupBand(str, Enum):
    DUFF_DEPTH = "duff_depth"
    FUEL_LOAD_1000HR_ROTTEN = "fuel_load.1000hr_rotten"
    FUEL_LOAD_1000HR_SOUND = "fuel_load.1000hr_sound"
    FUEL_LOAD_100HR = "fuel_load.100hr"
    FUEL_LOAD_10HR = "fuel_load.10hr"
    FUEL_LOAD_1HR = "fuel_load.1hr"
    FUEL_LOAD_DUFF = "fuel_load.duff"
    FUEL_LOAD_LITTER = "fuel_load.litter"
    FUEL_LOAD_LIVE_BRANCH = "fuel_load.live_branch"
    FUEL_LOAD_LIVE_FOLIAGE = "fuel_load.live_foliage"
    FUEL_LOAD_LIVE_HERB = "fuel_load.live_herb"
    FUEL_LOAD_LIVE_SHRUB = "fuel_load.live_shrub"

    @classmethod
    def _missing_(cls, value: object) -> "FccsLookupBand | None":
        """Parse a value this SDK version doesn't know as an ``UNKNOWN`` member
        that keeps the value, so new API values don't break older SDKs."""
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = "UNKNOWN"
        member._value_ = value
        return member

    def __str__(self) -> str:
        return str(self.value)
