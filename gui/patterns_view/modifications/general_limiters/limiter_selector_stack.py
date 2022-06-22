from PyQt6.QtWidgets import QStackedWidget, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_value_selector import \
    LimiterValueSelector
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode


class LimiterSelectorStack(QStackedWidget):
    """ The stacked widget that contains all the different column limits """

    parent: 'LimiterOverlay'
    limiter_direction: LimiterDirection
    selection_dictionary: dict[LimiterMode, QWidget]

    def __init__(
            self,
            current_cell_layout: 'reader',
            limiter_direction: LimiterDirection,
            parent: 'LimiterOverlay' = None):
        super().__init__()
        self.parent = parent
        self.current_cell_layout = current_cell_layout
        self.limiter_direction = limiter_direction

        no_selector_layout_widget = QWidget()
        no_selector_layout_widget.setLayout(
            LimiterValueSelector(
                current_cell_layout, self.limiter_direction, LimiterMode.NO_SELECTOR))
        self.addWidget(no_selector_layout_widget)

        between_layout_widget = QWidget()
        between_layout_widget.setLayout(
            LimiterValueSelector(
                current_cell_layout, self.limiter_direction, LimiterMode.BETWEEN))
        self.addWidget(between_layout_widget)

        from_layout_widget = QWidget()
        from_layout_widget.setLayout(
            LimiterValueSelector(
                current_cell_layout, self.limiter_direction, LimiterMode.FROM))
        self.addWidget(from_layout_widget)

        to_layout_widget = QWidget()
        to_layout_widget.setLayout(
            LimiterValueSelector(
                current_cell_layout, self.limiter_direction, LimiterMode.TO))
        self.addWidget(to_layout_widget)

        self.selection_dictionary = {
            LimiterMode.NO_SELECTOR: no_selector_layout_widget,
            LimiterMode.BETWEEN: between_layout_widget,
            LimiterMode.FROM: from_layout_widget,
            LimiterMode.TO: to_layout_widget
        }

    def change_selected(self, mode: LimiterMode) -> None:
        self.setCurrentWidget(self.selection_dictionary[mode])
