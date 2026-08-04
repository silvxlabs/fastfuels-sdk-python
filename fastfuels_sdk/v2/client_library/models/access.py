from enum import Enum


class Access(str, Enum):
    APPLICATION = "application"
    PERSONAL = "personal"

    def __str__(self) -> str:
        return str(self.value)
