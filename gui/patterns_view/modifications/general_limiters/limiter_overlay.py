from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.patterns_view.modifications.general_limiters.limiter_currently_applied import \
    LimiterCurrentlyApplied
from gui.patterns_view.modifications.general_limiters.limiter_drop_down import LimiterDropDown
from gui.patterns_view.modifications.general_limiters.limiter_selector_stack import \
    LimiterSelectorStack
from pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_direction import LimiterDirection


class LimiterOverlay(QVBoxLayout):
    """ A layout containing the necessary elements to limit the pattern display by

    # TODO: make overall list of currently applied in the stitching menu opt in addition to here
    so that all the changes can be viewed as one.
   +---------------+
   |     title     |
   +---------------+
   |   currently   |
   |    applied    |
   +---------------+
   | mode selector |
   +---------------+
   | value selector|
   |     stack     |
   +---------------+
    """
    parent: 'StitchingOptMenuOverview'
    direction: LimiterDirection
    title: QLabel
    currently_applied: LimiterCurrentlyApplied
    mode_selector_dropdown: LimiterDropDown
    value_selector_stack: LimiterSelectorStack

    def __init__(
            self,
            current_cell_layout: 'CurrentCellLayout',
            direction: LimiterDirection,
            current_mods: list['Modification'],
            model: 'PatternDisplayModel',
            parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent
        self.direction = direction
        self.current_cell_layout = current_cell_layout

        self.title = QLabel(s.limiter_title(self.direction))
        self.currently_applied = LimiterCurrentlyApplied(model, direction, current_mods, self)
        self.value_selector_stack = LimiterSelectorStack(
            self.currently_applied, current_cell_layout, self.direction)
        self.mode_selector_dropdown = LimiterDropDown(self.direction, self.value_selector_stack)

        self.addWidget(self.title)
        currently_applied_layout_widget = QWidget()
        currently_applied_layout_widget.setLayout(self.currently_applied)
        self.addWidget(currently_applied_layout_widget)
        self.addWidget(self.mode_selector_dropdown)
        self.addWidget(self.value_selector_stack)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modifications: list['Modification']) -> None:
        self.parent.create_new_pattern_tab(new_model, modifications)
