from enum import Enum


class ComposeComparisonOperator(str, Enum):
    EQ = "eq"
    GE = "ge"
    GT = "gt"
    IN = "in"
    LE = "le"
    LT = "lt"
    NE = "ne"

    def __str__(self) -> str:
        return str(self.value)
