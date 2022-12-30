import typing

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QColor

from gui.pattern_model import PatternModel
from pattern_cells.stitching_cell import StitchingCell
from stitchers.old_stitcher import OLD_Stitcher


class CurrentStitchingPatternModel(PatternModel):
    _data: list[list[StitchingCell]]
    stitcher: OLD_Stitcher

    def __init__(self, stitcher: OLD_Stitcher):
        super().__init__(stitcher.original_pattern)
        self.stitcher = stitcher

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        # Special colouring for this pattern model
        if role == Qt.ItemDataRole.BackgroundRole:
            if self._data[index.row()][index.column()].to_start_with:
                return QColor(f"#{self._data[index.row()][index.column()].hex_colour}")

        # Handle the remaining things
        return super().data(index, role)
