from enum import Enum


class BiomassEquations(str, Enum):
    JENKINS = "jenkins"
    NSVB = "nsvb"

    def __str__(self) -> str:
        return str(self.value)
