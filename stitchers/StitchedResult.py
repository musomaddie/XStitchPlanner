from dataclasses import dataclass

from pattern_cells.stitching_cell import StitchingCell


@dataclass
class StitchedResult:
    """ Contains all useful information for what was just stitched. """
    display_symbol: str
    dmc_value: str
    # Together the top_left_index and bottom_right_index cover all the cells that were modified by creating this stitch.
    # This includes any cells that are no longer the latest stitched, and any cells where the thread has been parked.
    top_left_index: list[int, int]
    bottom_right_index: list[int, int]
    cells_stitched: list[StitchingCell]
