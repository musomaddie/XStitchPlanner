from PyQt6.QtWidgets import QLabel, QVBoxLayout

import resources.gui_strings as s
from gui.patterns_view.modifications.general_limiters.limiter_direction import \
    LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_drop_down import \
    LimiterDropDown
from gui.patterns_view.modifications.general_limiters.limiter_mode import \
    LimiterMode
from gui.patterns_view.modifications.general_limiters.limiter_selector_stack \
    import \
    LimiterSelectorStack


class LimiterOverlay(QVBoxLayout):
    """ A layout containing the necessary elements to limit the pattern
    display by
   +---------------+
   |     title     |
   +---------------+
   |   currently   |
   |    applied    |
   +---------------+
   | mode selector |
   +---------------+
   |    options    |
   +---------------+
    """
    parent: 'StitchingOptMenuOverview'
    title: QLabel
    mode: LimiterMode
    direction: LimiterDirection
    mode_selector_dropdown: LimiterDropDown
    value_selector_stack: LimiterSelectorStack

    def __init__(
            self,
            direction: LimiterDirection,
            parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent
        self.direction = direction

        self.value_selector_stack = LimiterSelectorStack(self.direction)
        self.title = QLabel(s.limiter_title(self.direction))
        self.mode_selector_dropdown = LimiterDropDown(
            self.direction, self.value_selector_stack)

        self.addWidget(self.title)
        self.addWidget(self.mode_selector_dropdown)
        self.addWidget(self.value_selector_stack)
