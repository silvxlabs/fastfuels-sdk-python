from enum import Enum


class LandfireSeason(str, Enum):
    ES = "ES"
    FA = "FA"
    SP = "SP"
    SU = "SU"

    def __str__(self) -> str:
        return str(self.value)
