from enum import Enum


class Distribution(str, Enum):
    HOMOGENEOUS = "homogeneous"
    RANDOM_CLUSTERS = "random_clusters"
    UNIFORM_RANDOM = "uniform_random"

    def __str__(self) -> str:
        return str(self.value)
