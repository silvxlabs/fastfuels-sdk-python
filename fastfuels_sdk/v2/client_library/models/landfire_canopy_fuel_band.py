from enum import Enum


class LandfireCanopyFuelBand(str, Enum):
    CBD = "cbd"
    CBH = "cbh"
    CC = "cc"
    CHM = "chm"

    def __str__(self) -> str:
        return str(self.value)
