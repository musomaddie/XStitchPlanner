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

    def __eq__(self, other: 'StartingCorner'):
        return self.vertical == other.vertical and self.horizontal == other.horizontal

    def __repr__(self):
        return self.description


TOP_LEFT = StartingCorner("top left", VerticalDirection.TOP, HorizontalDirection.LEFT)
TOP_RIGHT = StartingCorner("top right", VerticalDirection.TOP, HorizontalDirection.RIGHT)
BOTTOM_LEFT = StartingCorner("bottom left", VerticalDirection.BOTTOM, HorizontalDirection.LEFT)
BOTTOM_RIGHT = StartingCorner("bottom right", VerticalDirection.BOTTOM, HorizontalDirection.RIGHT)


def find_starting_corner(vertical_dir: VerticalDirection, horizontal_dir: HorizontalDirection):
    if vertical_dir == VerticalDirection.TOP:
        if horizontal_dir == HorizontalDirection.LEFT:
            return TOP_LEFT
        return TOP_RIGHT
    if horizontal_dir == HorizontalDirection.LEFT:
        return BOTTOM_LEFT
    return BOTTOM_RIGHT
