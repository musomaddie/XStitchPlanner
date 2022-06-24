from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.pattern_view_toolbar import PatternViewToolBar
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay


class PatternViewTabContents(QVBoxLayout):
    parent: 'PatternViewTabList'
    toolbar: PatternViewToolBar
    display_overlay: PatternDisplayOverlay

    def __init__(
            self,
            pattern_name: str,
            model: 'PatternDisplayModel',
            parent: 'PatternViewTabList' = None):
        super().__init__()
        self.parent = parent
        self.display_overlay = PatternDisplayOverlay(pattern_name, model, self)
        self.toolbar = PatternViewToolBar(model, self.display_overlay)

        self.addWidget(self.toolbar)
        display_overlay_layout_widget = QWidget()
        display_overlay_layout_widget.setLayout(self.display_overlay)
        self.addWidget(display_overlay_layout_widget)
