from enum import Enum


class LandfireFbfm13Version(str, Enum):
    VALUE_0 = "2023"
    VALUE_1 = "2024"
    VALUE_2 = "2025"

    @classmethod
    def _missing_(cls, value: object) -> "LandfireFbfm13Version | None":
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
