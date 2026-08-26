from enum import Enum


class InventoryCanopyBand(str, Enum):
    CBD = "cbd"
    CBH = "cbh"
    CC = "cc"
    CFL = "cfl"
    CHM = "chm"

    def __str__(self) -> str:
        return str(self.value)
