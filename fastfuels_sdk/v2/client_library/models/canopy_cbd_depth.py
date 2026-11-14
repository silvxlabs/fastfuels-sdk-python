from enum import Enum


class CanopyCbdDepth(str, Enum):
    BIOMASS_PERCENTILE = "biomass_percentile"
    CANOPY_DEPTH = "canopy_depth"
    HEIGHT_PERCENTILE = "height_percentile"
    MEAN_CROWN_LENGTH = "mean_crown_length"

    @classmethod
    def _missing_(cls, value: object) -> "CanopyCbdDepth | None":
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
