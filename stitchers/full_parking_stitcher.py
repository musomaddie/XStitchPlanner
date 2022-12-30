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
                 starting_pattern: list[list[StitchingCell]],
                 starting_corner: StartingCorner,
                 config: dict = dict()):
        super().__init__(starting_pattern, starting_corner)
        self.max_rows_can_skip = config.get("max-rows-skip", 5)

    def _park_thread(self, dmc_symbol: str):
        for cell in PatternGenerator.iterate_over_limited_rows(self.generator, self.max_rows_can_skip):
            if cell.dmc_value == dmc_symbol:
                cell.parked = True
                return

    def stitch_next_colour(self):
        """ Overrides super method and stitches the next available colour. """
        # TODO: handle end of pattern sensibly
        to_stitch_cells = [cell for cell in self.generator.move_through_colour_in_rows()]
        to_stitch_cells[0].stitch(
            StartedFrom.FROM_PARKED_THREAD if to_stitch_cells[0].parked else StartedFrom.STARTED_NEW)
        for cell in to_stitch_cells[1:]:
            cell.stitch(StartedFrom.CONTINUED_FROM_ROW)

        self._park_thread(to_stitch_cells[0].dmc_value)

    def stitch_next_row(self):
        # TODO: see comments within parent class
        return
