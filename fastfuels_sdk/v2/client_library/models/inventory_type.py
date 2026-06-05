from enum import Enum


class InventoryType(str, Enum):
    TREE = "tree"

    def __str__(self) -> str:
        return str(self.value)
