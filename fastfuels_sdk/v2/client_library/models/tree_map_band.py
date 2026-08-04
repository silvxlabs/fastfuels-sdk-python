from enum import Enum


class TreeMapBand(str, Enum):
    PLT_CN = "plt_cn"
    TM_ID = "tm_id"

    def __str__(self) -> str:
        return str(self.value)
