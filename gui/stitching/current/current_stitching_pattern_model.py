import typing

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QColor

from gui.pattern_model import PatternModel
from pattern_cells.stitcher import Stitcher
from pattern_cells.stitching_cell import StitchingCell


class CurrentStitchingPatternModel(PatternModel):
    _data: list[list[StitchingCell]]
    stitcher: Stitcher

    def __init__(self, stitcher: Stitcher):
        super().__init__(stitcher.stitched_pattern)
        self.stitcher = stitcher

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        def _get_cell():
            return self._data[index.row()][index.column()]

        # Special colouring for this pattern model
        if role == Qt.ItemDataRole.BackgroundRole:
            # Colour it the main colour
            # TODO: fade colours that aren't the latest stitched.
            if _get_cell().stitched:
                return QColor(f"#{_get_cell().hex_colour}")
            # Colour any parked thread a lighter colour.
            if _get_cell().to_start_with or _get_cell().parked:
                return QColor(f"#88{_get_cell().hex_colour}")

        # Handle the remaining things
        return super().data(index, role)
