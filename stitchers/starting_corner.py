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


class PatternGenerator:
    vertical_dir: VerticalDirection
    horizontal_dir: HorizontalDirection
    pattern: list[list['StitchingCell']]
    current_x: int
    current_y: int

    def __init__(self, starting_corner: StartingCorner, stitching_pattern: list[list['StitchingCell']]):
        self.horizontal_dir = starting_corner.horizontal
        self.vertical_dir = starting_corner.vertical
        self.pattern = stitching_pattern
        self.current_x = 0 if self.horizontal_dir == HorizontalDirection.LEFT else len(self.pattern[0]) - 1
        self.current_y = 0 if self.vertical_dir == VerticalDirection.TOP else len(self.pattern) - 1

    # Create slightly different generates based on the need(?) This will iterate through the current row - and move to
    # the next
    def move_through_row(self):
        if self.horizontal_dir == HorizontalDirection.LEFT:
            while self.current_x < len(self.pattern[self.current_y]):
                yield self.pattern[self.current_y][self.current_x]
                self.current_x += 1
            self.current_x = 0
        else:
            while self.current_x >= 0:
                yield self.pattern[self.current_y][self.current_x]
                self.current_x -= 1
            self.current_x = len(self.pattern[0]) - 1
        if self.vertical_dir == VerticalDirection.TOP:
            self.current_y += 1
        else:
            self.current_y -= 1


TOP_LEFT = StartingCorner("top left", VerticalDirection.TOP, HorizontalDirection.LEFT)
TOP_RIGHT = StartingCorner("top right", VerticalDirection.TOP, HorizontalDirection.RIGHT)
BOTTOM_LEFT = StartingCorner("bottom left", VerticalDirection.BOTTOM, HorizontalDirection.LEFT)
BOTTOM_RIGHT = StartingCorner("bottom right", VerticalDirection.BOTTOM, HorizontalDirection.RIGHT)
