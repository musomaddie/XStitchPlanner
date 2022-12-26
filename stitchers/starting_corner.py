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
    # TODO: move to a better file?? - the color seems dependent on the parking approach.
    vertical_dir: VerticalDirection
    horizontal_dir: HorizontalDirection
    pattern: list[list['StitchingCell']]
    current_x: int
    current_y: int

    def __init__(self, starting_corner: StartingCorner, stitching_pattern: list[list['StitchingCell']]):
        self.horizontal_dir = starting_corner.horizontal
        self.vertical_dir = starting_corner.vertical
        self.pattern = stitching_pattern
        self.current_x = self._horizontal_idx_start()
        self.current_y = 0 if self.vertical_dir == VerticalDirection.TOP else len(self.pattern) - 1

    def move_through_row(self):
        """ Iterates through the entire row (all cells). Sets up the indices to iterate through the next row. """
        # TODO: should I handle stitched cells being part of this? (I don't want to return them if so)
        for value in self._row_generator():
            yield value
        if not self._within_bounds():
            raise StopIteration
        self._update_y()

    def move_through_colour_in_rows(self):
        """ Move through the next colour (but only up to a rows worth) """
        current_colour = self._find_current_colour()
        if current_colour is None:
            self._update_y()
            if not self._within_bounds():
                raise StopIteration
            current_colour = self._find_current_colour()
        for cell in self._row_generator():
            if not cell.stitched and cell.dmc_value == current_colour.dmc_value:
                yield cell

    def _within_bounds(self):
        return 0 <= self.current_y < len(self.pattern)

    def _find_current_colour(self):
        """ Finds the first colour in this row that hasn't been stitched. """
        for cell in self._row_generator():
            if not cell.stitched:
                return cell
        return None

    def _row_generator(self):
        """ A generator function that goes through the entire row."""
        # if self.horizontal_dir == HorizontalDirection.LEFT
        if self.horizontal_dir == HorizontalDirection.LEFT:
            while self.current_x < len(self.pattern[self.current_y]):
                yield self.pattern[self.current_y][self.current_x]
                self.current_x += 1
        else:
            while self.current_x >= 0:
                yield self.pattern[self.current_y][self.current_x]
                self.current_x -= 1
        self.current_x = self._horizontal_idx_start()

    def _update_y(self):
        if self.vertical_dir == VerticalDirection.TOP:
            self.current_y += 1
        else:
            self.current_y -= 1

    def _horizontal_idx_start(self):
        return 0 if self.horizontal_dir == HorizontalDirection.LEFT else len(self.pattern[0]) - 1


TOP_LEFT = StartingCorner("top left", VerticalDirection.TOP, HorizontalDirection.LEFT)
TOP_RIGHT = StartingCorner("top right", VerticalDirection.TOP, HorizontalDirection.RIGHT)
BOTTOM_LEFT = StartingCorner("bottom left", VerticalDirection.BOTTOM, HorizontalDirection.LEFT)
BOTTOM_RIGHT = StartingCorner("bottom right", VerticalDirection.BOTTOM, HorizontalDirection.RIGHT)
