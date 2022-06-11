from PyQt6.QtWidgets import QHBoxLayout, QLabel


class PatternTitleBar(QHBoxLayout):
    """ Responsible for containing all the information that is required in
    the pattern editor title bar
   +-------------------------------------------------------------------+
   |   PATTERN-TITLE                 |       CURRENTLY_SELECTED_CELL   |
   +-------------------------------------------------------------------+
    """
    parent: 'PatternEditorView'
    model: 'PatternDisplayModel'
    title: QLabel

    # current_cell_layout: CurrentCellLayout

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
