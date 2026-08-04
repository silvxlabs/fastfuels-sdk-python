from enum import Enum


class Operator(str, Enum):
    EQ = "eq"
    GE = "ge"
    GT = "gt"
    LE = "le"
    LT = "lt"
    NE = "ne"

    def __str__(self) -> str:
        return str(self.value)
