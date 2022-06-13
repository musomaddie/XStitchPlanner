from enum import Enum

from PyQt6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QStackedLayout,
                             QVBoxLayout,
                             QWidget)


class ColumnLimiterMode(Enum):
    NO_SELECTOR = "None"
    BETWEEN_COLUMNS = "Between Columns"
    FROM_COLUMN = "From Column"
    TO_COLUMN = "To Column"


class LimitColumnsDropDown(QComboBox):
    """ Contains the dropdown with the choice of which column limiter to use
    """
    options: list[ColumnLimiterMode]
    selected_mode: ColumnLimiterMode

    def __init__(self):
        super().__init__()
        self.options = list(ColumnLimiterMode)
        self.addItems([opt.value for opt in self.options])
        self.selected_mode = self.options[0]
        # self.activated.connect(self.update_currently_selected)


class LimitColumnsValueSelector(QStackedLayout):
    """ A layout to enter information depending on the selector mode chosen.
    NO_SELECTOR: (empty)
    BETWEEN_COLUMNS: | FROM xx (use_selection)   TO   xx  (us) |
    FROM_COLUMN:     | FROM xx (use_selection) |
    TO_COLUMN:       | TO xx (use_selection) |
    """
    parent: 'LimitColumnsLayout'
    no_selector_layout: QWidget
    between_columns_layout: QHBoxLayout
    from_column_layout: QHBoxLayout
    to_column_layout: QHBoxLayout

    def __init__(self, parent: 'LimitColumnsLayout' = None):
        super().__init__()
        self.parent = parent

        self.no_selector_layout = QWidget()
        self.addWidget(self.no_selector_layout)

        self.between_columns_layout = QHBoxLayout()
        self.between_columns_layout.addWidget(QLabel("between columns"))
        self.between_columns_layout_widget = QWidget()
        self.between_columns_layout_widget.setLayout(
            self.between_columns_layout)
        self.addWidget(self.between_columns_layout_widget)

        self.from_column_layout = QHBoxLayout()
        self.from_column_layout.addWidget(QLabel("from column"))
        self.from_column_layout_widget = QWidget()
        self.from_column_layout_widget.setLayout(self.from_column_layout)
        self.addWidget(self.from_column_layout_widget)

        self.to_column_layout = QHBoxLayout()
        self.to_column_layout.addWidget(QLabel("to column"))
        self.to_column_layout_widget = QWidget()
        self.to_column_layout_widget.setLayout(self.to_column_layout)
        self.addWidget(self.to_column_layout_widget)


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
    value_selector: LimitColumnsValueSelector

    def __init__(self, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel("Limit pattern via columns")
        self.mode_selector_dd = LimitColumnsDropDown()
        self.addWidget(self.title)
        self.addWidget(self.mode_selector_dd)
        self.value_selector = LimitColumnsValueSelector()
        value_selector_layout_widget = QWidget()
        value_selector_layout_widget.setLayout(self.value_selector)
        self.addWidget(value_selector_layout_widget)
