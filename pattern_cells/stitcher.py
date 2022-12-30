from abc import ABC, abstractmethod

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.pattern_generator import PatternGenerator
from stitchers.starting_corner import StartingCorner, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT


class Stitcher(ABC):
    """
    All the details of the stitching process are handled within this class. It is up to the caller to interact with the
    stitched pattern to extract information.
    TODO: could make a helper method to return the most recent changes??
    """
    width: int
    height: int
    stitched_pattern: list[list[StitchingCell]]
    starting_corner: StartingCorner
    generator: PatternGenerator

    def __init__(self, original_pattern: list[list[PatternCell]], starting_corner: StartingCorner):
        """ Creates a new Stitcher instance.

        Args:
            original_pattern: the pattern we want to stitch
            starting_corner: where we are beginning to stitch
        """
        self.height = len(original_pattern)
        self.width = len(original_pattern[0])
        self._height_idx = self.height - 1
        self._width_idx = self.width - 1
        self.stitched_pattern = [[StitchingCell(cell) for cell in row] for row in original_pattern]
        self.starting_corner = starting_corner
        self.generator = PatternGenerator(starting_corner, self.stitched_pattern)
        self.mark_starting_stitch()

    def mark_starting_stitch(self):
        if self.starting_corner == TOP_LEFT:
            self.stitched_pattern[0][0].to_start_with = True
            return
        if self.starting_corner == TOP_RIGHT:
            self.stitched_pattern[0][self._width_idx].to_start_with = True
            return
        if self.starting_corner == BOTTOM_LEFT:
            self.stitched_pattern[self._height_idx][0].to_start_with = True
            return
        if self.starting_corner == BOTTOM_RIGHT:
            self.stitched_pattern[self._height_idx][self._width_idx].to_start_with = True
            return
        raise NotImplementedError("Invalid starting corner")

    @abstractmethod
    def stitch_next_row(self):
        """ Stitches the entire next row if it exists, by marking the cells as stitched. """
        # TODO - I'm not convinced this will be useful (but I do have a "next row" button - but I'm not convinced
        #  that's useful either. Could control the granularity of the stitcher ??
        pass

    @abstractmethod
    def stitch_next_colour(self):
        """ Stitches the next colour. The exact details of this depend on the stitching method."""
        pass
