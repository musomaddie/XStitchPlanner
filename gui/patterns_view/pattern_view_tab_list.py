from PyQt6.QtWidgets import QTabWidget, QWidget

import resources.gui_strings as s
from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.modifications.general_limiters.limiter_currently_applied import Modification
from gui.patterns_view.pattern_view_tab_contents import PatternViewTabContents
from pattern_cells.pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode


class PatternViewTabList(QTabWidget):
    parent: 'ViewHierarchy'
    pattern_name: str
    original_layout: PatternViewTabContents
    tab_list: list[PatternViewTabContents]  # Doesn't contain original layout
    tab_counts: dict[str, int]

    def __init__(
            self,
            pattern_name: str,
            pattern_model: 'PatternDisplayModel',
            parent: 'ViewHierarchy' = None):
        super().__init__()

        # TODO: If I save the pattern_name here then I won't need to take it in for creating the
        #  next tab

        self.parent = parent
        self.pattern_name = pattern_name
        self.original_layout = PatternViewTabContents(
            pattern_name, pattern_model,
            {direction: [Modification(LimiterMode.NO_SELECTOR, [])]
             for direction in list(LimiterDirection)}, self)
        self.tab_list = []
        self.tab_counts = {"modifications": 0, "variants": 0}

        og_layout_widget = QWidget()
        og_layout_widget.setLayout(self.original_layout)
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.addTab(og_layout_widget, s.original_pattern(pattern_name))

    def load_stitch_view(self, model: 'PatternDisplayModel') -> None:
        """ Loads the stitch view: echoes call all the way to view hierarchy """
        self.parent.load_stitch_view(self.pattern_name, model)

    def create_new_tab_with_modifications(
            self,
            pattern_model_data: list[list[PatternCell]],
            modifications: dict[LimiterDirection, list['Modification']]) -> None:
        """ Creates and displays a new tab containing the passed modifications """
        pattern_model = PatternDisplayModel(pattern_model_data)
        new_layout = PatternViewTabContents(self.pattern_name, pattern_model, modifications, self)
        self.tab_list.append(new_layout)
        self.tab_counts["modifications"] += 1

        new_layout_widget = QWidget()
        new_layout_widget.setLayout(new_layout)
        self.addTab(new_layout_widget, f"{self.pattern_name} ({self.tab_counts['modifications']})")
        self.setCurrentIndex(len(self.tab_list))

    def create_new_tab_with_variant(
            self,
            new_model_data: list[list[PatternCell]],
            modifications: dict[LimiterDirection, list['Modification']]) -> None:
        """ Creates and displays a new tab containing the variant whose data has been passed """
        new_pattern_model = PatternDisplayModel(new_model_data)
        new_layout = PatternViewTabContents(
            self.pattern_name, new_pattern_model, modifications, self)
        self.tab_list.append(new_layout)
        self.tab_counts["variants"] += 1

        new_layout_widget = QWidget()
        new_layout_widget.setLayout(new_layout)
        self.addTab(
            new_layout_widget,
            f"{self.pattern_name} variant #{self.tab_counts['variants']}")
        self.setCurrentIndex(len(self.tab_list))
