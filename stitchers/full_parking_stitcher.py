from pattern_cells.pattern_cell import PatternCell
from pattern_cells.started_from import StartedFrom
from pattern_cells.stitcher import Stitcher
from pattern_cells.stitching_cell import StitchingCell
from stitchers.pattern_generator import PatternGenerator
from stitchers.starting_corner import StartingCorner


class FullParkingStitcher(Stitcher):
    """ Handles the typical parking technique for the given pattern. This parking technique means
    stitching every cell in the row before moving on to the next one.

    For example stitching the row: A B B A C would be stitched in the following order (assuming
    starting on the left): A A B B C (with either Danish or English method)
    """

    def __init__(self,
                 starting_pattern: list[list[PatternCell]],
                 starting_corner: StartingCorner,
                 config: dict = {}):
        super().__init__(starting_pattern, starting_corner, config)
        self.max_rows_can_skip = config.get("max-rows-skip", 5)
        self.highlight_latest_stitched = config.get("highlight_latest_stitched", True)
        self.latest_stitched = []

    def _park_thread(self, dmc_symbol: str) -> StitchingCell:
        for cell in PatternGenerator.iterate_over_limited_rows(self.generator, self.max_rows_can_skip):
            if cell.dmc_value == dmc_symbol:
                cell.parked = True
                return cell
        return None

    def stitch_next_colour(self):
        """ Overrides super method and stitches the next available colour. """
        # TODO: handle end of pattern sensibly
        # TODO: take advantage of python lists being pass by reference here so it's not quite as ugly.
        top_left_index = [self._height_idx, self._width_idx]
        bottom_right_index = [0, 0]

        if self.highlight_latest_stitched:
            for cell in self.latest_stitched:
                cell.latest_stitched = False
                Stitcher.update_modified_idx(top_left_index, bottom_right_index, cell)

        to_stitch_cells = [cell for cell in self.generator.move_through_colour_in_rows()]

        to_stitch_cells[0].stitch(
            StartedFrom.FROM_PARKED_THREAD if to_stitch_cells[0].parked else StartedFrom.STARTED_NEW)
        Stitcher.update_modified_idx(top_left_index, bottom_right_index, to_stitch_cells[0])

        for cell in to_stitch_cells[1:]:
            cell.stitch(StartedFrom.CONTINUED_FROM_ROW)
            Stitcher.update_modified_idx(top_left_index, bottom_right_index, cell)

        if self.highlight_latest_stitched:
            self.latest_stitched = to_stitch_cells

        parked_cell = self._park_thread(to_stitch_cells[0].dmc_value)
        if parked_cell:
            Stitcher.update_modified_idx(top_left_index, bottom_right_index, parked_cell)

        # TODO: test these return values!!
        return top_left_index, bottom_right_index

    def stitch_next_row(self):
        # TODO: see comments within parent class
        return
