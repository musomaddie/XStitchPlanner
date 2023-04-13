from enum import Enum


class LimiterType(Enum):
    ROW = "row"
    COLUMN = "column"
    RECTANGLE = "rectangle"
