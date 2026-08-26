from enum import Enum


class CanopyBiomassEquations(str, Enum):
    BROWN_1978 = "brown_1978"
    JENKINS = "jenkins"
    NSVB = "nsvb"

    def __str__(self) -> str:
        return str(self.value)
