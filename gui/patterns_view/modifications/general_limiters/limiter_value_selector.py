from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import LimiterMode


class ValueWidget(QWidget):
    direction = LimiterDirection
    mode = LimiterMode
    current_cell_layout: 'CurrentCellLayout'
    prompt: QLabel
    supplied_values: list[QLineEdit]  # this is the only one I probably really need
    set_current_value_buttons: list[QPushButton]

    def __init__(
            self,
            current_cell_layout: 'CurrentCellLayout',
            direction: LimiterDirection,
            mode: LimiterMode):
        super().__init__()
        self.current_cell_layout = current_cell_layout
        self.direction = direction
        self.mode = mode
        self.supplied_values = []
        self.set_current_value_buttons = []

        if mode == LimiterMode.NO_SELECTOR:
            return

        self.prompt = QLabel(s.limit_prompt(self.mode))
        layout = QVBoxLayout()
        layout.addWidget(self.prompt)
        layout.addWidget(self.create_input_filler())
        if mode == LimiterMode.BETWEEN:
            layout.addWidget(QLabel("&"))
            layout.addWidget(self.create_input_filler())

        self.setLayout(layout)

    def create_line_edit(self) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setValidator(QIntValidator())
        self.supplied_values.append(line_edit)
        return line_edit

    def create_button(self, line_edit: QLineEdit):
        button = QPushButton(s.limiter_use_current_cell_desc(self.direction))
        button.clicked.connect(lambda: line_edit.setText(
            str(self.current_cell_layout.get_current_value(self.direction) + 1)))
        self.set_current_value_buttons.append(button)
        return button

    def create_input_filler(self) -> QHBoxLayout:
        le = self.create_line_edit()
        h_layout = QHBoxLayout()
        h_layout.addWidget(le)
        h_layout.addWidget(self.create_button(le))
        h_layout_wid = QWidget()
        h_layout_wid.setLayout(h_layout)
        return h_layout_wid


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
            current_cell_layout: 'CurrentCellLayout',
            selector_direction: LimiterDirection,
            selector_mode: LimiterMode):
        super().__init__()
        self.selector_direction = selector_direction
        self.selector_mode = selector_mode

        self.apply_button = QPushButton(s.apply_button())
        self.explanation = QLabel(self.display_explanation())
        self.explanation.setWordWrap(True)
        self.value_widget = ValueWidget(
            current_cell_layout, self.selector_direction, self.selector_mode)

        self.addWidget(self.explanation)
        self.addWidget(self.value_widget)
        self.addWidget(self.apply_button)

    # def apply_data(self):
    #     # I need to get the data from the value widget which is going to be a pain in the butt
    # # unless I make it it's own class

    def display_explanation(self):
        if self.selector_mode == LimiterMode.NO_SELECTOR:
            return s.limiter_remove_desc(self.selector_direction)
        elif self.selector_mode == LimiterMode.FROM:
            return s.limiter_from_desc(self.selector_direction)
        elif self.selector_mode == LimiterMode.TO:
            return s.limiter_to_desc(self.selector_direction)
        elif self.selector_mode == LimiterMode.BETWEEN:
            return s.limiter_between_desc(self.selector_direction.value)

        raise ValueError(f"{self.selector_direction} with {self.selector_mode} is not recognised")
