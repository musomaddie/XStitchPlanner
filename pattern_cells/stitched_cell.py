from dataclasses import dataclass
from enum import Enum, auto

from pattern_cells.stitching_cell import StitchingCell


class StartedFrom(Enum):
    FROM_PARKED_THREAD = auto()
    STARTED_NEW = auto()
    CONTINUED_FROM_ROW = auto()


@dataclass
class StitchedCell(StitchingCell):
    started_from: StartedFrom
    nth_stitched: int

    @staticmethod
    def create_from_stitching_cell(cell: StitchingCell, num_stitched: int) -> 'StitchedCell':
        return StitchedCell(
            cell.display_symbol,
            cell.dmc_value,
            cell.index,
            cell.hex_colour,
            StartedFrom.FROM_PARKED_THREAD if cell.parked else StartedFrom.STARTED_NEW,
            num_stitched + 1)

    @staticmethod
    def create_when_found_in_row(cell: StitchingCell, num_stitched) -> 'StitchedCell':
        return StitchedCell(
            cell.display_symbol,
            cell.dmc_value,
            cell.index,
            cell.hex_colour,
            StartedFrom.CONTINUED_FROM_ROW,
            num_stitched + 1)

    def __repr__(self):
        return f"{self.display_symbol} [{self.nth_stitched}] (sed)"
