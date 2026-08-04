from enum import Enum


class QuicfireExportRequestMoistMerge(str, Enum):
    MAX = "max"
    WEIGHTED_AVG = "weighted_avg"

    def __str__(self) -> str:
        return str(self.value)
