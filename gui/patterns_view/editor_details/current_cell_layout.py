from PyQt6.QtWidgets import QHBoxLayout, QLabel


class CurrentCellLayout(QHBoxLayout):
    """ Contains the information for the current cell
    +-------------------------------------------------------------------+
    |         title            |      row        |      col             |
    +-------------------------------------------------------------------+
    """
    # TODO: handle selected range somehow nicely
    parent: 'PatternEditorView'
    title: QLabel
    row_display: QLabel
    col_display: QLabel
    row_value: int
    col_value: int

    def __init__(self, parent: 'PatternEditorView' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel("Currently selected cell: ")
        self.row_value = 0
        self.col_value = 0

        self.row_display = QLabel(f"(row:) {self.row_value}")
        self.col_display = QLabel(f"(col): {self.col_value}")

        self.addWidget(self.title)
        self.addWidget(self.row_display)
        self.addWidget(self.col_display)
