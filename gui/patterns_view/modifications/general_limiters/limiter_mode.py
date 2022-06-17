from enum import Enum


class LimiterMode(Enum):
    NO_SELECTOR = "no"
    BETWEEN = "between"
    FROM = "from"
    TO = "to"
