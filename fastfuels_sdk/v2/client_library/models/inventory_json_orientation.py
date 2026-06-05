from enum import Enum


class InventoryJsonOrientation(str, Enum):
    RECORDS = "records"
    SPLIT = "split"

    def __str__(self) -> str:
        return str(self.value)
