from enum import Enum


class UserMeResponseKind(str, Enum):
    APPLICATION = "application"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
