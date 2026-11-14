from enum import Enum


class Fbfm13LookupBand(str, Enum):
    FUEL_DEPTH = "fuel_depth"
    FUEL_LOAD_100HR = "fuel_load.100hr"
    FUEL_LOAD_10HR = "fuel_load.10hr"
    FUEL_LOAD_1HR = "fuel_load.1hr"
    FUEL_LOAD_LIVE_FOLIAGE = "fuel_load.live_foliage"
    SAVR_100HR = "savr.100hr"
    SAVR_10HR = "savr.10hr"
    SAVR_1HR = "savr.1hr"
    SAVR_LIVE_FOLIAGE = "savr.live_foliage"

    @classmethod
    def _missing_(cls, value: object) -> "Fbfm13LookupBand | None":
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
