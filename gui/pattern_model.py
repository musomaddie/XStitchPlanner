import typing

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor

from gui.pattern_view import PatternView
from pattern_cells.pattern_cell import PatternCell


class PatternModel(QAbstractTableModel):
    """ A super class for all pattern models. Generically handles the pattern data for display

    Methods:
        __init__(data)
        data(index, role): displays the data
        rowCount(index): number of rows
        columnCount(index): number of columns
        add_display(display): connects the display used for this data so that it can be modified
            as necessary
    """
    _data: list[list[PatternCell]]
    show_colours: bool
    display: 'PatternView'

    def __init__(self, data: list[list[PatternCell]]):
        super().__init__()
        self._data = data
        self.show_colours = False
        self.display = None

    def add_display(self, display: 'PatternView') -> None:
        self.display = display

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data[0])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.BackgroundRole and self.show_colours:
            return QColor(f"#{self._data[index.row()][index.column()].hex_colour}")
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignHCenter + Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()].display_symbol

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)
