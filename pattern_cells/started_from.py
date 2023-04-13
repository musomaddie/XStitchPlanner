from enum import Enum, auto


class StartedFrom(Enum):
    NOT_STARTED = auto()
    FROM_PARKED_THREAD = auto()
    STARTED_NEW = auto()
    CONTINUED_FROM_ROW = auto()
