from enum import Enum


class ColumnType(str, Enum):
    CATEGORICAL = "categorical"
    CONTINUOUS = "continuous"

    def __str__(self) -> str:
        return str(self.value)
