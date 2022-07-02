from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_overlay import LimiterOverlay
from gui.patterns_view.modifications.load_overlay import LoadOverlay
from gui.patterns_view.modifications.save_button import SaveButton
from pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_direction import LimiterDirection


class StitchingOptMenuOverview(QVBoxLayout):
    # TODO: allow very basic pattern changes (i.e. on harry potter allow
    #  assigning of colours to replace the "and the ....." text
    """ Menu containing buttons that interaction with the pattern

    TODO: make undo / back button
   +---------------+
   |    LOAD       |
   +---------------+
   |    LIMIT BY   |
   |    COLUMNS    |
   +---------------+
   |    LIMIT BY   |
   |    ROWS       |
   +---------------+
   |   SAVE        |
   +---------------+
    """
    parent: 'PatternDisplayOverlay'
    load_overlay: LoadOverlay
    column_overlay: LimiterOverlay
    row_overlay: LimiterOverlay
    save_button: SaveButton

    def __init__(
            self,
            pattern_name: str,
            current_cell_layout: 'CurrentCellLayout',
            model: 'PatternDisplayModel',
            current_mods: dict[LimiterDirection, list['Modification']],
            parent: 'PatternDisplayOverlay' = None):
        super().__init__()
        self.parent = parent

        self.load_overlay = LoadOverlay(pattern_name, self)
        load_overlay_layout_widget = QWidget()
        load_overlay_layout_widget.setLayout(self.load_overlay)
        self.addWidget(load_overlay_layout_widget)

        self.column_overlay = LimiterOverlay(
            current_cell_layout,
            LimiterDirection.COLUMN,
            current_mods[LimiterDirection.COLUMN],
            model,
            self)
        column_overlay_layout_widget = QWidget()
        column_overlay_layout_widget.setLayout(self.column_overlay)
        self.addWidget(column_overlay_layout_widget)

        self.row_overlay = LimiterOverlay(
            current_cell_layout,
            LimiterDirection.ROW,
            current_mods[LimiterDirection.ROW],
            model,
            self)
        row_overlay_layout_widget = QWidget()
        row_overlay_layout_widget.setLayout(self.row_overlay)
        self.addWidget(row_overlay_layout_widget)

        save_button = SaveButton(
            pattern_name, model,
            {LimiterDirection.COLUMN: self.column_overlay.get_all_modifiers(),
             LimiterDirection.ROW: self.row_overlay.get_all_modifiers()}, self)
        self.addWidget(save_button)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modifications: dict[LimiterDirection, list['Modification']]) -> None:
        """ Creates and displays a new tab with the current pattern modifications """
        self.parent.create_new_pattern_tab(new_model, modifications)

    def create_new_pattern_variant_tab(self, new_model_data: list[list[PatternCell]]) -> None:
        """ Creates and displays a new tab with the selected pattern variant """
        self.parent.create_new_pattern_variant_tab(
            new_model_data,
            {LimiterDirection.ROW: self.get_modifiers_for_direction(LimiterDirection.ROW),
             LimiterDirection.COLUMN: self.get_modifiers_for_direction(LimiterDirection.COLUMN)})

    def get_modifiers_for_direction(self, direction: LimiterDirection) -> list['Modification']:
        """ Fetches all the current modifications for the given direction"""
        if direction == LimiterDirection.COLUMN:
            return self.column_overlay.get_all_modifiers()
        return self.row_overlay.get_all_modifiers()
