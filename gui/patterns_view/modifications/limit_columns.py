from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedLayout,
    QVBoxLayout,
    QWidget)

import resources.gui_strings as s


# TODO: consider splitting this into separate files??


class ColumnLimiterMode(Enum):
    NO_SELECTOR = "None"
    BETWEEN_COLUMNS = "Between Columns"
    FROM_COLUMN = "From Column"
    TO_COLUMN = "To Column"


class LimitColumnsDropDown(QComboBox):
    """ Contains the dropdown with the choice of which column limiter to use
    """
    parent: 'LimitColumnsLayout'
    value_selector: 'LimitColumnsValueSelectorOverlay'
    options: list[ColumnLimiterMode]

    def __init__(
            self,
            value_selector: 'LimitColumnsValueSelectorOverlay',
            parent: 'LimitColumnsLayout' = None):
        super().__init__()
        self.parent = parent
        self.value_selector = value_selector
        self.options = list(ColumnLimiterMode)
        self.addItems([opt.value for opt in self.options])
        self.activated.connect(self.update_currently_selected)

    def update_currently_selected(self):
        self.value_selector.change_selected(
            self.options[self.currentIndex()])


class LimitColumnsValueSelector(QVBoxLayout):
    """ Contains the layout for this mode --> magic
    The apply button here pushes the call to the applied layout (above) (TODO)
    which will handle the implementation logic the applied layout then calls a
    method on its parent which echos the call back until there are tabs
    added to the editor view
    """
    overlay: 'LimitColumnsValueSelectorOverlay'
    selector_mode: ColumnLimiterMode
    apply_button: QPushButton
    explanation: QLabel
    from_value_layout_widget: QWidget

    def __init__(
            self, selector_mode: ColumnLimiterMode,
            overlay: 'LimitColumnsValueSelectorOverlay' = None):
        super().__init__()
        self.selector_mode = selector_mode
        self.overlay = overlay

        self.apply_button = QPushButton(s.apply_button())
        self.explanation = QLabel(self.display_explanation())
        self.explanation.setWordWrap(True)

        # TODO: make this dynamically resize based on window size!
        self._create_from_value_layout()

        self.addWidget(self.explanation)
        if self.selector_mode == ColumnLimiterMode.FROM_COLUMN:
            self.addWidget(self.from_value_layout_widget)
        self.addWidget(self.apply_button)

    def display_explanation(self):
        if self.selector_mode == ColumnLimiterMode.NO_SELECTOR:
            return s.remove_column_limit_desc()
        if self.selector_mode == ColumnLimiterMode.FROM_COLUMN:
            return s.from_column_limit_desc()

    @staticmethod
    def _make_value_prompt(dim: str) -> QLabel:
        fv_prompt = QLabel(s.from_column_prompt() if dim == "column" else "")
        fv_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return fv_prompt

    @staticmethod
    def _make_value_line_edit() -> QLineEdit:
        le = QLineEdit()
        le.setValidator(QIntValidator())
        return le

    @staticmethod
    def _make_value_button(dim: str, le: QLineEdit) -> QPushButton:
        but = QPushButton(s.use_selected_desc(dim))
        but.clicked.connect(lambda: le.setText("100"))
        return but

    # TODO: move these out of the class completely when refactoring to new file
    @staticmethod
    def _make_value_input(dim: str) -> QWidget:
        i_lay = QHBoxLayout()
        le = LimitColumnsValueSelector._make_value_line_edit()
        i_lay.addWidget(le)
        i_lay.addWidget(LimitColumnsValueSelector._make_value_button(dim, le))
        i_wid = QWidget()
        i_wid.setLayout(i_lay)
        return i_wid

    def _create_from_value_layout(self):
        fv_layout = QVBoxLayout()
        fv_layout.addWidget(LimitColumnsValueSelector._make_value_prompt(
            "column"))
        fv_layout.addWidget(LimitColumnsValueSelector._make_value_input(
            "column"))

        self.from_value_layout_widget = QWidget()
        self.from_value_layout_widget.setLayout(fv_layout)


class LimitColumnsValueSelectorOverlay(QStackedLayout):
    """ A layout to enter information depending on the selector mode chosen.
    NO_SELECTOR: (empty)
    BETWEEN_COLUMNS: | FROM xx (use_selection)   TO   xx  (us) |
    FROM_COLUMN:     | FROM xx (use_selection) |
    TO_COLUMN:       | TO xx (use_selection) |
    """
    parent: 'LimitColumnsLayout'
    selection_dictionary: dict[ColumnLimiterMode, QWidget]

    # between_columns_layout: QHBoxLayout
    # from_column_layout: QHBoxLayout
    # to_column_layout: QHBoxLayout

    def __init__(self, parent: 'LimitColumnsLayout' = None):
        super().__init__()
        self.parent = parent

        no_selector_layout_widget = QWidget()
        no_selector_layout_widget.setLayout(
            LimitColumnsValueSelector(ColumnLimiterMode.NO_SELECTOR, self))
        self.addWidget(no_selector_layout_widget)

        between_columns_layout = QHBoxLayout()
        between_columns_layout.addWidget(QLabel("between columns"))
        between_columns_layout_widget = QWidget()
        between_columns_layout_widget.setLayout(
            between_columns_layout)
        self.addWidget(between_columns_layout_widget)

        from_column_layout_widget = QWidget()
        from_column_layout_widget.setLayout(
            LimitColumnsValueSelector(ColumnLimiterMode.FROM_COLUMN, self))
        self.addWidget(from_column_layout_widget)

        to_column_layout = QHBoxLayout()
        to_column_layout.addWidget(QLabel("to column"))
        to_column_layout_widget = QWidget()
        to_column_layout_widget.setLayout(to_column_layout)
        self.addWidget(to_column_layout_widget)

        self.selection_dictionary = {
            ColumnLimiterMode.NO_SELECTOR: no_selector_layout_widget,
            ColumnLimiterMode.BETWEEN_COLUMNS: between_columns_layout_widget,
            ColumnLimiterMode.FROM_COLUMN: from_column_layout_widget,
            ColumnLimiterMode.TO_COLUMN: to_column_layout_widget
        }

    def change_selected(self, mode: ColumnLimiterMode) -> None:
        self.setCurrentWidget(self.selection_dictionary[mode])


class LimitColumnsLayout(QVBoxLayout):
    """ Layout containing the necessary elements to limit the pattern display by
    columns
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
    mode_selector_dd: LimitColumnsDropDown
    value_selector: LimitColumnsValueSelectorOverlay

    def __init__(self, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel("Limit pattern via columns")
        self.value_selector = LimitColumnsValueSelectorOverlay()
        self.mode_selector_dd = LimitColumnsDropDown(self.value_selector,
                                                     self)
        self.addWidget(self.title)
        self.addWidget(self.mode_selector_dd)
        value_selector_layout_widget = QWidget()
        value_selector_layout_widget.setLayout(self.value_selector)
        self.addWidget(value_selector_layout_widget)
