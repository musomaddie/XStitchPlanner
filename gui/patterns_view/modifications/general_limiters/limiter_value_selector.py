from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget)

import resources.gui_strings as s
from gui.patterns_view.modifications.general_limiters.limiter_direction import \
    LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import \
    LimiterMode


def create_value_widget(
        direction: LimiterDirection, mode: LimiterMode) -> QWidget:
    if mode == LimiterMode.NO_SELECTOR:
        return QWidget()

    def create_line_edit():
        line_edit = QLineEdit()
        line_edit.setValidator(QIntValidator())
        return line_edit

    def create_button(line_edit: QLineEdit):
        button = QPushButton(s.limiter_use_current_cell_desc(direction))
        # TODO: update this to work correctly
        button.clicked.connect(lambda: line_edit.setText("100"))
        return button

    def create_input_filler():
        line_edit = create_line_edit()
        v_layout = QHBoxLayout()
        v_layout.addWidget(line_edit)
        v_layout.addWidget(create_button(line_edit))
        v_layout_widget = QWidget()
        v_layout_widget.setLayout(v_layout)
        return v_layout_widget

    # Prompt
    layout = QVBoxLayout()
    layout.addWidget(QLabel(s.limit_prompt(mode)))
    layout.addWidget(create_input_filler())
    if mode == LimiterMode.BETWEEN:
        layout.addWidget(QLabel("&"))
        layout.addWidget(create_input_filler())

    w = QWidget()
    w.setLayout(layout)
    return w


class LimiterValueSelector(QVBoxLayout):
    """
    Responsible for the actual content of the pattern general_limiters.
    """
    selector_mode: LimiterMode
    selector_direction: LimiterDirection
    apply_button: QPushButton
    explanation: QLabel
    value_widget: QWidget

    def __init__(
            self,
            selector_direction: LimiterDirection,
            selector_mode: LimiterMode):
        super().__init__()
        self.selector_direction = selector_direction
        self.selector_mode = selector_mode

        self.apply_button = QPushButton(s.apply_button())
        self.explanation = QLabel(self.display_explanation())
        self.explanation.setWordWrap(True)
        self.value_widget = create_value_widget(
            self.selector_direction, self.selector_mode)

        self.addWidget(self.explanation)
        self.addWidget(self.value_widget)
        self.addWidget(self.apply_button)

    def display_explanation(self):
        if self.selector_mode == LimiterMode.NO_SELECTOR:
            return s.limiter_remove_desc(self.selector_direction)
        elif self.selector_mode == LimiterMode.FROM:
            return s.limiter_from_desc(self.selector_direction)
        elif self.selector_mode == LimiterMode.TO:
            return s.limiter_to_desc(self.selector_direction)
        elif self.selector_mode == LimiterMode.BETWEEN:
            return s.limiter_between_desc(self.selector_direction.value)

        raise ValueError(f"{self.selector_direction} with "
                         f"{self.selector_mode} is not recognised")
