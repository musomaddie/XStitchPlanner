from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_overlay import LimiterOverlay
from pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_direction import LimiterDirection


class StitchingOptMenuOverview(QVBoxLayout):
    # TODO: allow very basic pattern changes (i.e. on harry potter allow
    #  assigning of colours to replace the "and the ....." text
    """ Menu containing buttons that interaction with the pattern

    TODO: make undo / back button
   +---------------+
   |    LIMIT BY   |
   |    COLUMNS    |
   +---------------+
   |               |
   |               |
   |               |
   +---------------+
    """
    parent: 'PatternDisplayOverlay'
    column_overlay: LimiterOverlay

    # TODO: I think this will actually need to be a stacked layout (or have one SOMEWHERE) to
    #  control when everything is visible. Or maybe tabs??

    def __init__(
            self,
            current_cell_layout: 'CurrentCellLayout',
            model: 'PatternDisplayModel',
            current_mods: list['Modification'],
            parent):
        super().__init__()
        self.parent = parent

        self.column_overlay = LimiterOverlay(
            current_cell_layout, LimiterDirection.COLUMN, current_mods, model, self)
        column_overlay_layout_widget = QWidget()
        column_overlay_layout_widget.setLayout(self.column_overlay)
        self.addWidget(column_overlay_layout_widget)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modifications: list['Modification']) -> None:
        self.parent.create_new_pattern_tab(new_model, modifications)
