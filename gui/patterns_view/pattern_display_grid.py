from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QTableView, QHeaderView


class PatternDisplayGridModel(QAbstractTableModel):
    """ Handles the pattern data for display

    Parameters:
        data    list[list[str]]     the pattern data

    Methods:
        __init__(data)  PatternDisplayGridModel

    Static Methods:
        load_from_pattern_file(pattern_name)    PatternDisplayGridModel
                loads a pattern display grid model from the .pat file with the
                given pattern name

    """

    def __init__(self, data):
        super().__init__()
        self.data = data

    def data(self, index, role):
        # TODO: does it get stuck here???
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self.data)

    def columnCount(self, index):
        return len(self.data[0])

    @staticmethod
    def load_from_pattern_file(pattern_name):
        """ Returns a PatternDisplayGridModel containing a data loaded from the
        .pat file of the given pattern.

        Args:
            pattern_name    str     the name of the pattern to load

        Returns:
            PatternDisplayGridModel     with the given pattern loaded as data

        Raises:
            FileNotFoundError   if the given pattern does not have a
                                    corresponding file name. This should never
                                    be reached as it MUST have a .pat file to be
                                    selected from the pattern selector
        """

        with open(f"patterns/{pattern_name}.pat") as f:
            return PatternDisplayGridModel(
                [[letter for letter in row.rstrip()]
                 for row in f.readlines()]
            )


class PatternDisplayGridView(QTableView):
    """ Responsible for actually displaying the pattern in a table form.

    Parameters:
        parent  PatternDisplayOverlay
        model   PatternDisplayGridModel     the model managing this table

    Methods:
        __init__(pattern_name)  PatternDisplayGridView
    """

    def __init__(self, pattern_name, parent=None):
        super().__init__()

        self.parent = parent
        self.model = PatternDisplayGridModel.load_from_pattern_file(
            pattern_name)

        self.setModel(self.model)

        # Using ResizeMode.Fixed to control the size of the cells as using a
        # more dynamic resize caused the program to take a long time loading
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setDefaultSectionSize(10)
        self.verticalHeader().setDefaultSectionSize(10)
