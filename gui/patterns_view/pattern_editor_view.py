from PyQt6.QtWidgets import QGridLayout, QLabel

from gui.patterns_view.editor_details.pattern_display_view import \
    PatternDisplayView


class PatternEditorView(QGridLayout):
    """ A class containing the pattern editor view
    +-------------------------------------------------------------------+
    |   PATTERN-TITLE                 |       CURRENTLY_SELECTED_CELL   |
    +-------------------------------------------------------------------+
    |                                                                   |
    |                        TABLE_VIEW                                 |
    |                                                                   |
    +-------------------------------------------------------------------+
    """
    parent: 'PatternDisplayOverlay'
    title: QLabel
    model: 'PatternDisplayModel'
    current_cell_layout: 'CurrentCellLayout'
    table_view: 'PatternDisplayView'

    def __init__(
            self,
            title: str,
            model: 'PatternDisplayModel',
            parent: 'PatternDisplayOverlay' = None):
        super().__init__()
        self.parent = parent
        self.model = model

        self.title = QLabel(title)
        self.addWidget(self.title)

        self.table_view = PatternDisplayView(title, model, self)
        self.addWidget(self.table_view)
