from enum import IntEnum


class ThreeDepResolution(IntEnum):
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_10 = 10
    VALUE_30 = 30

    @classmethod
    def _missing_(cls, value: object) -> "ThreeDepResolution | None":
        """Parse a value this SDK version doesn't know as an ``UNKNOWN`` member
        that keeps the value, so new API values don't break older SDKs."""
        if not isinstance(value, int) or isinstance(value, bool):
            return None
        member = int.__new__(cls, value)
        member._name_ = "UNKNOWN"
        member._value_ = value
        return member

    def __str__(self) -> str:
        return str(self.value)
