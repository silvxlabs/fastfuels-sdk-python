from enum import Enum


class Modifier(str, Enum):
    ADD = "add"
    DIVIDE = "divide"
    MULTIPLY = "multiply"
    REPLACE = "replace"
    SUBTRACT = "subtract"

    def __str__(self) -> str:
        return str(self.value)
