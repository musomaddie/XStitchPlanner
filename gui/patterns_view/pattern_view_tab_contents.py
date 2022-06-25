from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.pattern_view_toolbar import PatternViewToolBar
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay
from pattern_cell import PatternCell


class PatternViewTabContents(QVBoxLayout):
    parent: 'PatternViewTabList'
    toolbar: PatternViewToolBar
    display_overlay: PatternDisplayOverlay

    def __init__(
            self,
            pattern_name: str,
            model: 'PatternDisplayModel',
            current_mod: list['Modification'],
            parent: 'PatternViewTabList' = None):
        super().__init__()
        self.parent = parent
        self.display_overlay = PatternDisplayOverlay(pattern_name, model, current_mod, self)
        self.toolbar = PatternViewToolBar(model, self.display_overlay)

        self.addWidget(self.toolbar)
        display_overlay_layout_widget = QWidget()
        display_overlay_layout_widget.setLayout(self.display_overlay)
        self.addWidget(display_overlay_layout_widget)

    def create_new_pattern_tab(
            self,
            pattern_name: str,
            new_model: list[list[PatternCell]],
            modifications: list['Modification']) -> None:
        self.parent.create_new_tab(pattern_name, new_model, modifications)
