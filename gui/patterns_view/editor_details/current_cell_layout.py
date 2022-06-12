from PyQt6.QtWidgets import QHBoxLayout, QLabel


class CurrentCellLayout(QHBoxLayout):
    """ Contains the information for the current cell
    +-------------------------------------------------------------------+
    |         title            |      row        |      col             |
    +-------------------------------------------------------------------+

    Methods:
        update_displays()   updates the numbers being displayed
    """
    # TODO: handle selected range somehow nicely
    parent: 'PatternTitleBar'
    title: QLabel
    row_display: QLabel
    col_display: QLabel
    row_value: int
    col_value: int

    def __init__(self, parent: 'PatternTitleBar' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel("Currently selected cell: ")
        self.row_value = 0
        self.col_value = 0

        # TODO: make this look pretty!
        self.row_display = QLabel(f"(row:) {self.row_value}")
        self.col_display = QLabel(f"(col:) {self.col_value}")

        self.addWidget(self.title)
        self.addWidget(self.row_display)
        self.addWidget(self.col_display)

    def _update_displays(self):
        self.row_display.setText(f"(row:) {self.row_value}")
        self.col_display.setText(f"(col:) {self.col_value}")

    def update_values(self, row: int, col: int) -> None:
        self.row_value = row
        self.col_value = col
        self._update_displays()
