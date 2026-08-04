from enum import Enum


class ComposeOperator(str, Enum):
    ADD = "add"
    AVERAGE = "average"
    DIVIDE = "divide"
    MAX = "max"
    MIN = "min"
    MULTIPLY = "multiply"
    SUBTRACT = "subtract"

    def __str__(self) -> str:
        return str(self.value)
