from enum import Enum


class InventorySortField(str, Enum):
    CREATED_ON = "created_on"
    MODIFIED_ON = "modified_on"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
