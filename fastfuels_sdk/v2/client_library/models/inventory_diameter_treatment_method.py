from enum import Enum


class InventoryDiameterTreatmentMethod(str, Enum):
    FROM_ABOVE = "from_above"
    FROM_BELOW = "from_below"

    def __str__(self) -> str:
        return str(self.value)
