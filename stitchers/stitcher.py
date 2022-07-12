from abc import ABC, abstractmethod

from pattern_cells.stitched_cell import StitchedCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.starting_corner import StartingCorner


class Stitcher(ABC):
    original_pattern: list[list[StitchingCell]]
    stitched_pattern: list[list[StitchedCell]]
    starting_corner: StartingCorner

    def __init__(
            self, starting_pattern: list[list[StitchingCell]], starting_corner: StartingCorner):
        self.original_pattern = starting_pattern
        self.stitched_pattern = []
        self.starting_corner = starting_corner

    @abstractmethod
    def stitch_next_row(self) -> list[StitchedCell]:
        """ Stitches the entire next row if it exists. 

        Returns:
            list[StitchedCell]: the stitched row
        """
        pass

    @abstractmethod
    def stitch_next_colour(
            self, num_stitched_currently: int) -> tuple[list[StitchedCell], int]:
        """
        Stitches the next colour if it exists.

        Args:
            num_stitched_currently: how many cells have been currently stitched from this row

        Returns:
            list[StitchedCell]: the list of all cells of this colour found in this row
            int: how many cells have been stitched after this colour has been stitched
        """
        pass

    @abstractmethod
    def stitch_entire_pattern(self) -> [list[list[StitchedCell]]]:
        """
        Stitches this entire pattern and returns the stitched version.

        Returns:
            the stitched pattern
        """
        pass
