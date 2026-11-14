from enum import Enum


class UniformBand(str, Enum):
    CURING = "curing"
    FUEL_DEPTH = "fuel_depth"
    FUEL_LOAD_100HR = "fuel_load.100hr"
    FUEL_LOAD_10HR = "fuel_load.10hr"
    FUEL_LOAD_1HR = "fuel_load.1hr"
    FUEL_LOAD_LIVE_HERB = "fuel_load.live_herb"
    FUEL_LOAD_LIVE_WOODY = "fuel_load.live_woody"
    FUEL_MOISTURE_100HR = "fuel_moisture.100hr"
    FUEL_MOISTURE_10HR = "fuel_moisture.10hr"
    FUEL_MOISTURE_1HR = "fuel_moisture.1hr"
    FUEL_MOISTURE_LIVE_HERB = "fuel_moisture.live_herb"
    FUEL_MOISTURE_LIVE_WOODY = "fuel_moisture.live_woody"

    @classmethod
    def _missing_(cls, value: object) -> "UniformBand | None":
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
