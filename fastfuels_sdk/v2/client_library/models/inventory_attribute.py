from enum import Enum


class InventoryAttribute(str, Enum):
    CROWN_BASE_HEIGHT = "crown_base_height"
    DBH = "dbh"
    FIA_SPECIES_CODE = "fia_species_code"
    HEIGHT = "height"
    TREE_ID = "tree_id"

    @classmethod
    def _missing_(cls, value: object) -> "InventoryAttribute | None":
        """Parse a value this SDK version doesn't know as an ``UNKNOWN`` member
        that keeps the value, so new API values don't break older SDKs."""
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = "UNKNOWN"
        member._value_ = value
        return member

    def __str__(self) -> str:
        return str(self.value)
