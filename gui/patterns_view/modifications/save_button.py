from PyQt6.QtWidgets import QPushButton

from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.modification import Modification
from utils import save_pattern


class SaveButton(QPushButton):

    parent: 'StitchingOptMenuOverview'
    applied_modifications: dict[LimiterDirection, list[Modification]]
    pattern_name: str
    model: 'PatternModel'

    def __init__(
            self,
            pattern_name,
            model,
            applied_modifications: dict[LimiterDirection, list[Modification]],
            parent: 'StitchingOptMenuOverview' = None):
        super().__init__()

        self.parent = parent
        self.pattern_name = pattern_name
        self.applied_modifications = applied_modifications
        self.model = model
        self.setText("Save these modifications")

    def _make_filename(self):
        row_mods_string = ""
        for mod in self.applied_modifications[LimiterDirection.ROW]:
            if mod.mode != LimiterMode.NO_SELECTOR:
                row_mods_string += f"{mod.mode.value}[{'_'.join(str(v) for v in mod.values)}]"
        col_mods_string = ""
        for mod in self.applied_modifications[LimiterDirection.COLUMN]:
            if mod.mode != LimiterMode.NO_SELECTOR:
                col_mods_string += f"{mod.mode.value}[{'_'.join(str(v) for v in mod.values)}]"

        return f"{self.pattern_name}-row-{row_mods_string}-col-{col_mods_string}-variant"

    def save_pattern_variant(self):
        """
        Saves this pattern to a file with a name from the modifiers. Then when it's loaded it
        can use the file name to get the relevant extractors. Symbols used should not differ
        from the original pattern.
        """
        save_pattern(self._make_filename(), self.model._data)
