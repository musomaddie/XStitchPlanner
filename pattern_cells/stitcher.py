from abc import ABC, abstractmethod

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.StitchedResult import StitchedResult
from stitchers.pattern_generator import PatternGenerator
from stitchers.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, StartingCorner, TOP_LEFT, TOP_RIGHT


class Stitcher(ABC):
    """
    All the details of the stitching process are handled within this class. It is up to the caller to interact with the
    stitched pattern to extract information.
    TODO: could make a helper method to return the most recent changes??
    """
    _height_idx: int
    _width_idx: int
    generator: PatternGenerator
    highlight_latest_stitched: bool
    latest_stitched: list[StitchingCell]
    height: int
    starting_corner: StartingCorner
    stitched_pattern: list[list[StitchingCell]]
    width: int

    def __init__(self,
                 original_pattern: list[list[PatternCell]],
                 starting_corner: StartingCorner,
                 config: dict):
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
        self.highlight_latest_stitched = config.get("highlight_latest_stitched", True)
        self.latest_stitched = []
        self.mark_starting_stitch()

    @staticmethod
    def update_modified_idx(
            top_left_index: list[int, int], bottom_right_index: list[int, int], current_cell: StitchingCell) -> None:
        """ Updates the saved indices that wrap what has currently been modified. Modifies the list in place."""
        top_left_index[0] = min(top_left_index[0], current_cell.index[0])
        top_left_index[1] = min(top_left_index[1], current_cell.index[1])
        bottom_right_index[0] = max(bottom_right_index[0], current_cell.index[0])
        bottom_right_index[1] = max(bottom_right_index[1], current_cell.index[1])

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
    def stitch_next_colour(self) -> StitchedResult:
        """ Stitches the next colour. The exact details of this depend on the stitching method."""
        pass
