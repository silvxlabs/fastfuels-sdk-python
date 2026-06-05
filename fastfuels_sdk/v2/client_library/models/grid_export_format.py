from enum import Enum


class GridExportFormat(str, Enum):
    GEOTIFF = "geotiff"
    NETCDF = "netcdf"
    ZARR = "zarr"

    def __str__(self) -> str:
        return str(self.value)
