from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.patterns_view.modifications.general_limiters.limiter_overlay import LimiterOverlay
from gui.patterns_view.modifications.load_overlay import LoadOverlay
from gui.patterns_view.modifications.save_button import SaveButton
from pattern_cells.pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_type import LimiterType


class StitchingOptMenuOverview(QVBoxLayout):
    # TODO: allow very basic pattern changes (i.e. on harry potter allow
    #  assigning of colours to replace the "and the ....." text
    """ Menu containing buttons that interaction with the pattern

    TODO: make undo / back button
   +---------------+
   |   STITCH      |
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
    stitch_button: QPushButton
    model: 'PatternDisplayModel'
    load_overlay: LoadOverlay
    column_overlay: LimiterOverlay
    row_overlay: LimiterOverlay
    save_button: SaveButton

    def __init__(
            self,
            pattern_name: str,
            current_cell_layout: 'CurrentCellLayout',
            model: 'PatternDisplayModel',
            current_mods: dict[LimiterType, list['Modification']],
            parent: 'PatternDisplayOverlay' = None):
        super().__init__()
        self.parent = parent
        self.model = model

        self.stitch_button = QPushButton(s.start_stitching_title())
        self.stitch_button.pressed.connect(self.load_stitch_view)
        self.addWidget(self.stitch_button)

        self.load_overlay = LoadOverlay(pattern_name, self)
        load_overlay_layout_widget = QWidget()
        load_overlay_layout_widget.setLayout(self.load_overlay)
        self.addWidget(load_overlay_layout_widget)

        self.column_overlay = LimiterOverlay(
            current_cell_layout,
            LimiterType.COLUMN,
            current_mods[LimiterType.COLUMN],
            model,
            self)
        column_overlay_layout_widget = QWidget()
        column_overlay_layout_widget.setLayout(self.column_overlay)
        self.addWidget(column_overlay_layout_widget)

        self.row_overlay = LimiterOverlay(
            current_cell_layout,
            LimiterType.ROW,
            current_mods[LimiterType.ROW],
            model,
            self)
        row_overlay_layout_widget = QWidget()
        row_overlay_layout_widget.setLayout(self.row_overlay)
        self.addWidget(row_overlay_layout_widget)

        self.save_button = SaveButton(
            pattern_name, model,
            {LimiterType.COLUMN: self.column_overlay.get_all_modifiers(),
             LimiterType.ROW: self.row_overlay.get_all_modifiers()}, self)
        self.addWidget(self.save_button)

    def load_stitch_view(self):
        """ Loads the view for stitching this pattern. """
        self.parent.load_stitch_view(self.model)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modifications: dict[LimiterType, list['Modification']]) -> None:
        """ Creates and displays a new tab with the current pattern modifications """
        self.parent.create_new_pattern_tab(new_model, modifications)

    def create_new_pattern_variant_tab(self, new_model_data: list[list[PatternCell]]) -> None:
        """ Creates and displays a new tab with the selected pattern variant """
        self.parent.create_new_pattern_variant_tab(
            new_model_data,
            {LimiterType.ROW: self.get_modifiers_for_direction(LimiterType.ROW),
             LimiterType.COLUMN: self.get_modifiers_for_direction(LimiterType.COLUMN)})

    def get_modifiers_for_direction(self, direction: LimiterType) -> list['Modification']:
        """ Fetches all the current modifications for the given direction"""
        if direction == LimiterType.COLUMN:
            return self.column_overlay.get_all_modifiers()
        return self.row_overlay.get_all_modifiers()
