from enum import Enum


class ResamplingMethod(str, Enum):
    AVERAGE = "average"
    BILINEAR = "bilinear"
    CUBIC = "cubic"
    CUBIC_SPLINE = "cubic_spline"
    FIRST_QUARTILE = "first_quartile"
    LANCZOS = "lanczos"
    MAX = "max"
    MEDIAN = "median"
    MIN = "min"
    MODE = "mode"
    NEAREST = "nearest"
    ROOT_MEAN_SQUARE = "root_mean_square"
    SUM = "sum"
    THIRD_QUARTILE = "third_quartile"

    def __str__(self) -> str:
        return str(self.value)
