from PyQt6.QtWidgets import QHeaderView, QTableView

from gui.pattern_display_model import PatternDisplayModel


class PatternDisplayView(QTableView):
    """ Responsible for actually displaying the pattern in a table form.

    Parameters:
        parent (PatternDisplayOverlay)
        model  (PatternDisplayModel)     the model managing this table

    Methods:
        __init__(pattern_name)  PatternDisplayGridView
    """
    pattern_name: str
    model: 'PatternDisplayModel'
    parent: 'PatternEditorView'

    def __init__(
            self,
            pattern_name: str,
            model: PatternDisplayModel,
            parent: 'PatternEditorView' = None):
        super().__init__()

        self.parent = parent
        self.model = model
        self.pattern_name = pattern_name

        self.setModel(self.model)

        # Using ResizeMode.Fixed to control the size of the cells as using a
        # more dynamic resize caused the program to take a long time loading
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setDefaultSectionSize(10)
        self.verticalHeader().setDefaultSectionSize(10)

        # Setting the font size of the header row
        current_font = self.font()
        current_font.setPointSize(8)
        self.horizontalHeader().setFont(current_font)

        # Handling interactions with the table
        # self.cellClicked.connect(self.on_cell_click)

    # def on_cell_click(self, row, column):
    #     print(row, column)
