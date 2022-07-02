import copy

from pattern_cells.starting_corner import HorizontalDirection, StartingCorner, VerticalDirection
from pattern_cells.stitched_cell import StitchedCell
from pattern_cells.stitching_cell import StitchingCell


class FullParking:
    """ Handles the typical parking technique for the given pattern. This parking technique means
    stitching every cell in the row before moving on to the next one.

    For example stitching the row: A B B A C would be stitched in the following order (assuming
    starting on the left): C A A B B (with either Danish or English method)

    Parameters: (description)
        original_pattern: the starting pattern
        stitched_pattern: the stitched pattern
        starting_corner: the corner to start stitching
        num_skippable_columns: the number of vertical columns that are appropriate to skip while
            still carrying the thread. (i.e. if this is 1 than any gap larger than one column will
            not be carried - the thread will be cut and then started again).
        next_row_to_stitch: the next row to be stitched, None if the entire passed pattern has been
            stitched

    Methods:
        __init__()
    """
    original_pattern: list[list[StitchingCell]]
    stitched_pattern: list[list[StitchedCell]]
    starting_corner: StartingCorner
    num_skippable_columns: int
    next_row_to_stitch: list[StitchingCell]

    def __init__(
            self,
            starting_pattern: list[list[StitchingCell]],
            starting_corner: StartingCorner,
            config: dict = {}):
        self.original_pattern = starting_pattern
        self.stitched_pattern = []
        self.starting_corner = starting_corner
        self.num_skippable_columns = config.get("skippable-columns", 0)
        self.next_row_to_stitch = self.get_next_stitchable_row()

    def get_next_stitchable_row(self) -> list[StitchingCell]:
        num_stitched = len(self.stitched_pattern)
        num_to_stitch = len(self.original_pattern)
        if num_stitched == num_to_stitch:
            return None
        if self.starting_corner.vertical == VerticalDirection.TOP:
            return self.original_pattern[num_stitched]
        return self.original_pattern[num_to_stitch - 1 - num_stitched]

    @staticmethod
    def stitch_this_colour(
            current_colour_cell: StitchingCell,
            remaining_row: list[StitchingCell],
            num_stitched_currently: int) -> tuple[list[StitchedCell], int]:
        """ Finds all the occurrences of the given colour in the current row

        Args:
            num_stitched_currently:
            current_colour_cell: the current cell we're searching for
            remaining_row: the remaining cells in the row (NOT inclusive of the current_colour_cell)
            num_stitched_currently: how many cells have been currently stitched from this row
            
        Returns:
            list[StitchedCell]: the list of all cells of this colour found in this row.
            int: how many cells have been stitched after this colour
        """
        # Should never happen but just a sanity check
        if current_colour_cell.stitched:
            return ([], num_stitched_currently)
        found_colours = [
            StitchedCell.create_from_stitching_cell(current_colour_cell, num_stitched_currently)]
        num_stitched_currently += 1
        current_colour_cell.stitched = True
        for cell in remaining_row:
            if current_colour_cell == cell:
                found_colours.append(
                    StitchedCell.create_when_found_in_row(cell, num_stitched_currently))
                num_stitched_currently += 1
                cell.stitched = True
        return found_colours, num_stitched_currently

    def stitch_next_row(self):
        """ Stitches the next row to stitch if it exists """
        if self.next_row_to_stitch is None:
            return
        current_row = (copy.deepcopy(self.next_row_to_stitch)
                       if self.starting_corner.horizontal == HorizontalDirection.LEFT
                       else list(reversed(copy.deepcopy(self.next_row_to_stitch))))
        # Work through the row
        stitched_row = []
        num_stitched = 0
        while len(current_row) > 0:
            this_cell = current_row.pop(0)
            if this_cell.stitched:
                continue
            colours, num_stitched = FullParking.stitch_this_colour(
                this_cell, current_row, num_stitched)
            stitched_row.append(colours)
            # TODO: handle parking in the future rows
            # TODO: handle moving to next row
        return stitched_row
