from PyQt6.QtWidgets import QTabWidget, QWidget

import resources.gui_strings as s
from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.modifications.general_limiters.limiter_currently_applied import Modification
from gui.patterns_view.pattern_view_tab_contents import PatternViewTabContents
from pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode


class PatternViewTabList(QTabWidget):
    parent: 'ViewHierarchy'
    original_layout: PatternViewTabContents
    tab_list: list[PatternViewTabContents]  # Doesn't contain original layout

    def __init__(
            self,
            pattern_name: str,
            pattern_model: 'PatternDisplayModel',
            parent: 'ViewHierarchy' = None):
        super().__init__()

        # TODO: If I save the pattern_name here then I won't need to take it in for creating the
        #  next tab

        self.parent = parent
        self.original_layout = PatternViewTabContents(
            pattern_name, pattern_model,
            {direction: [Modification(LimiterMode.NO_SELECTOR, [])]
             for direction in list(LimiterDirection)}, self)
        self.tab_list = []

        og_layout_widget = QWidget()
        og_layout_widget.setLayout(self.original_layout)
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.addTab(og_layout_widget, s.original_pattern(pattern_name))

    def create_new_tab(
            self,
            pattern_name: str,
            pattern_model_data: list[list[PatternCell]],
            modifications: dict[LimiterDirection, list['Modification']]) -> None:
        pattern_model = PatternDisplayModel(pattern_model_data)
        new_layout = PatternViewTabContents(pattern_name, pattern_model, modifications, self)
        self.tab_list.append(new_layout)

        new_layout_widget = QWidget()
        new_layout_widget.setLayout(new_layout)
        self.addTab(new_layout_widget, f"{pattern_name} ({len(self.tab_list)})")
        self.setCurrentIndex(len(self.tab_list))
