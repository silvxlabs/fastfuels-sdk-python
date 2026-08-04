from enum import Enum


class InventoryTreatmentMethod(str, Enum):
    FROM_ABOVE = "from_above"
    FROM_BELOW = "from_below"
    PROPORTIONAL = "proportional"

    def __str__(self) -> str:
        return str(self.value)
