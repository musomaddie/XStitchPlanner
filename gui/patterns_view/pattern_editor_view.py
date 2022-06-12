from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.editor_details.pattern_display_view import \
    PatternDisplayView
from gui.patterns_view.editor_details.pattern_title_bar import PatternTitleBar


class PatternEditorView(QVBoxLayout):
    """ A class containing the pattern editor view
    +-------------------------------------------------------------------+
    |                          PATTERN_TITLE_BAR                        |
    +-------------------------------------------------------------------+
    |                                                                   |
    |                              TABLE_VIEW                           |
    |                                                                   |
    +-------------------------------------------------------------------+
    """
    parent: 'PatternDisplayOverlay'
    model: 'PatternDisplayModel'
    title_bar: PatternTitleBar
    table_view: 'PatternDisplayView'

    def __init__(
            self,
            title: str,
            model: 'PatternDisplayModel',
            parent: 'PatternDisplayOverlay' = None):
        super().__init__()
        self.parent = parent
        self.model = model

        self.title_bar = PatternTitleBar(title, model, self)
        title_bar_layout_widget = QWidget()
        title_bar_layout_widget.setLayout(self.title_bar)
        self.addWidget(title_bar_layout_widget)

        self.table_view = PatternDisplayView(model,
                                             self.title_bar.current_cell,
                                             self)
        self.addWidget(self.table_view)
