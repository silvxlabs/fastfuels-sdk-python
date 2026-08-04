from enum import Enum


class InventoryExportFormat(str, Enum):
    CSV = "csv"
    GEOJSON = "geojson"
    GEOPACKAGE = "geopackage"
    PARQUET = "parquet"

    def __str__(self) -> str:
        return str(self.value)
