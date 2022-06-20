from PyQt6.QtWidgets import QTabWidget, QWidget

import resources.gui_strings as s
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay


# TODO: add tests!!


class PatternViewTab(QTabWidget):
    parent: 'ViewHierarchy'
    original_layout: PatternDisplayOverlay

    def __init__(
            self,
            pattern_name: str,
            pattern_model: 'PatternDisplayModel',
            parent: 'ViewHierarchy' = None):
        super().__init__()

        self.parent = parent
        self.original_layout = PatternDisplayOverlay(pattern_name, pattern_model, self)
        og_layout_widget = QWidget()
        og_layout_widget.setLayout(self.original_layout)
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.addTab(og_layout_widget, s.original_pattern())
