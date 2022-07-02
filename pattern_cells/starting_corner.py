from enum import Enum


class HorizontalDirection(Enum):
    LEFT = "left"
    RIGHT = "right"


class VerticalDirection(Enum):
    TOP = "top"
    BOTTOM = "bottom"


class StartingCorner:
    description: str
    vertical: VerticalDirection
    horizontal: HorizontalDirection

    def __init__(self, desc, v, h):
        self.description = desc
        self.vertical = v
        self.horizontal = h


TOP_LEFT = StartingCorner("top left", VerticalDirection.TOP, HorizontalDirection.LEFT)
TOP_RIGHT = StartingCorner("top right", VerticalDirection.TOP, HorizontalDirection.RIGHT)
BOTTOM_LEFT = StartingCorner("bottom left", VerticalDirection.BOTTOM, HorizontalDirection.LEFT)
BOTTOM_RIGHT = StartingCorner("bottom right", VerticalDirection.BOTTOM, HorizontalDirection.RIGHT)
