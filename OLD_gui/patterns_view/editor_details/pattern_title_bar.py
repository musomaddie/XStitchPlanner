from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from gui.patterns_view.editor_details.current_cell_layout import CurrentCellLayout


class PatternTitleBar(QHBoxLayout):
    """ Responsible for containing all the information that is required in the pattern editor
    title bar
   +-------------------------------------------------------------------+
   |   PATTERN-TITLE                 |       CURRENTLY_SELECTED_CELL   |
   +-------------------------------------------------------------------+
    """
    parent: 'PatternEditorView'
    model: 'PatternDisplayModel'
    title: QLabel
    current_cell: CurrentCellLayout

    def __init__(
            self,
            title: str,
            model: 'PatternDisplayModel',
            parent: 'PatternEditorView' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel(title)
        self.model = model

        self.addWidget(self.title)

        self.current_cell = CurrentCellLayout(self)
        current_cell_layout_widget = QWidget()
        current_cell_layout_widget.setLayout(self.current_cell)
        self.addWidget(current_cell_layout_widget)

    def get_current_cell_layout(self):
        return self.current_cell
