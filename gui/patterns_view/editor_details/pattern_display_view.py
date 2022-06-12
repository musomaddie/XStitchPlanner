from PyQt6.QtWidgets import QHeaderView, QTableView

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.editor_details.current_cell_layout import \
    CurrentCellLayout


class PatternDisplayView(QTableView):
    """ Responsible for actually displaying the pattern in a table form.

    Parameters:
        parent (PatternDisplayOverlay)
        model  (PatternDisplayModel)     the model managing this table
    """
    model: 'PatternDisplayModel'
    parent: 'PatternEditorView'

    def __init__(
            self,
            model: PatternDisplayModel,
            current_cell_layout: CurrentCellLayout,
            parent: 'PatternEditorView' = None):
        super().__init__()

        self.parent = parent
        self.model = model

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
        self.verticalHeader().setFont(current_font)

        self.clicked.connect(current_cell_layout.update_values)
