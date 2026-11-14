from enum import Enum


class FuelMoistureMonth(str, Enum):
    APRIL = "April"
    AUGUST = "August"
    DECEMBER = "December"
    FEBRUARY = "February"
    JANUARY = "January"
    JULY = "July"
    JUNE = "June"
    MARCH = "March"
    MAY = "May"
    NOVEMBER = "November"
    OCTOBER = "October"
    SEPTEMBER = "September"

    @classmethod
    def _missing_(cls, value: object) -> "FuelMoistureMonth | None":
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
