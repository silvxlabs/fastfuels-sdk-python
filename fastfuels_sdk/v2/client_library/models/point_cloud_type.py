from enum import Enum


class PointCloudType(str, Enum):
    ALS = "als"
    TLS = "tls"

    def __str__(self) -> str:
        return str(self.value)
