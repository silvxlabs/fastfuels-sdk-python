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

    def __str__(self) -> str:
        return str(self.value)
