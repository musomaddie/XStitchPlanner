from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QTableView


class PatternDisplayGridModel(QAbstractTableModel):
    """ Handles the pattern data for display

    Parameters:
        data    list[list[str]]     the pattern data

    Methods:
        __init__(data)  PatternDisplayGridModel

    Static Methods:
        load_pattern_from_file(pattern_name)    PatternDisplayGridModel
                loads a pattern display grid model from the .pat file with the
                given pattern name

    """

    def __init__(self, data):
        super().__init__()
        self.data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self.data)

    def columnCount(self, index):
        return len(self.data[0])


class PatternDisplayGridView(QTableView):
    pass
