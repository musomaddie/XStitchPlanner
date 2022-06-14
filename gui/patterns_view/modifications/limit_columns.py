from enum import Enum

from PyQt6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QStackedLayout, QVBoxLayout, QWidget)


class ColumnLimiterMode(Enum):
    NO_SELECTOR = "None"
    BETWEEN_COLUMNS = "Between Columns"
    FROM_COLUMN = "From Column"
    TO_COLUMN = "To Column"


class LimitColumnsDropDown(QComboBox):
    """ Contains the dropdown with the choice of which column limiter to use
    """
    parent: 'LimitColumnsLayout'
    value_selector: 'LimitColumnsValueSelector'
    options: list[ColumnLimiterMode]

    def __init__(
            self,
            value_selector: 'LimitColumnsValueSelector',
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


class LimitColumnsValueSelector(QStackedLayout):
    """ A layout to enter information depending on the selector mode chosen.
    NO_SELECTOR: (empty)
    BETWEEN_COLUMNS: | FROM xx (use_selection)   TO   xx  (us) |
    FROM_COLUMN:     | FROM xx (use_selection) |
    TO_COLUMN:       | TO xx (use_selection) |
    """
    parent: 'LimitColumnsLayout'
    selection_dictionary: dict[ColumnLimiterMode, QWidget]

    # TODO: not sure if these should be saved as class variables too
    # no_selector_layout: QWidget
    # between_columns_layout: QHBoxLayout
    # from_column_layout: QHBoxLayout
    # to_column_layout: QHBoxLayout

    def __init__(self, parent: 'LimitColumnsLayout' = None):
        super().__init__()
        self.parent = parent

        no_selector_layout_widget = QWidget()
        self.addWidget(no_selector_layout_widget)

        between_columns_layout = QHBoxLayout()
        between_columns_layout.addWidget(QLabel("between columns"))
        between_columns_layout_widget = QWidget()
        between_columns_layout_widget.setLayout(
            between_columns_layout)
        self.addWidget(between_columns_layout_widget)

        from_column_layout = QHBoxLayout()
        from_column_layout.addWidget(QLabel("from column"))
        from_column_layout_widget = QWidget()
        from_column_layout_widget.setLayout(from_column_layout)
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
    value_selector: LimitColumnsValueSelector

    def __init__(self, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel("Limit pattern via columns")
        self.value_selector = LimitColumnsValueSelector()
        self.mode_selector_dd = LimitColumnsDropDown(self.value_selector,
                                                     self)
        self.addWidget(self.title)
        self.addWidget(self.mode_selector_dd)
        value_selector_layout_widget = QWidget()
        value_selector_layout_widget.setLayout(self.value_selector)
        self.addWidget(value_selector_layout_widget)
