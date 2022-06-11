from PyQt6.QtWidgets import QVBoxLayout

from gui.patterns_view.modifications.limit_columns import LimitColumnsLayout


class StitchingOptMenuOverview(QVBoxLayout):
    """ Menu containing buttons that interaction with the pattern

   +---------------+
   |    LIMIT BY   |
   |    COLUMNS    |
   +---------------+
   |               |
   |               |
   |               |
   +---------------+

    Parameters:
        parent (PatternDisplayOverlay)
        columnn_control (LimitColumnsLayout) layout responsible for limiting
            by columns
    """
    parent: 'PatternDisplayOverlay'
    column_control: LimitColumnsLayout

    def __init__(self, parent: 'PatternDisplayOverlay' = None):
        super().__init__()
        self.parent = parent

        # self.column_control = LimitColumnsLayout()
        # column_control_layout_widget = QWidget()
        # column_control_layout_widget.setLayout(self.column_control)
        # self.addWidget(column_control_layout_widget)
