from enum import Enum


class NonBurnableFuelModel(str, Enum):
    NB1 = "NB1"
    NB2 = "NB2"
    NB3 = "NB3"
    NB8 = "NB8"
    NB9 = "NB9"

    @classmethod
    def _missing_(cls, value: object) -> "NonBurnableFuelModel | None":
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
