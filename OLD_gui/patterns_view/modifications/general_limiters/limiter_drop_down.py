from PyQt6.QtWidgets import QComboBox

from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.limiter_type import LimiterType


class LimiterDropDown(QComboBox):
    """ Contains the dropdown with the choice of which column limiter to use
    """
    parent: 'LimiterOverlay'
    limiter_direction: LimiterType
    value_selector_stack: 'LimiterSelectorStack'

    def __init__(
            self,
            limiter_direction: LimiterType,
            value_selector_stack: 'LimiterSelectorStack',
            parent: 'LimiterOverlay' = None):
        super().__init__()
        self.parent = parent
        self.options = list(LimiterMode)
        self.value_selector_stack = value_selector_stack

        self.addItems(
            [f"{opt.value} {limiter_direction.value}s".title()
             if opt == LimiterMode.BETWEEN or opt == LimiterMode.NO_SELECTOR
             else f"{opt.value.title()} {limiter_direction.value}".title()
             for opt in self.options])
        self.activated.connect(self.update_currently_selected)

    def update_currently_selected(self):
        self.value_selector_stack.change_selected(
            self.options[self.currentIndex()])
