from enum import Enum


class InventoryUploadFormat(str, Enum):
    CSV = "csv"
    GEOJSON = "geojson"
    GEOPACKAGE = "geopackage"

    def __str__(self) -> str:
        return str(self.value)
