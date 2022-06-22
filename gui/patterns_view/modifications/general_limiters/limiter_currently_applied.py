from PyQt6.QtWidgets import QLabel, QVBoxLayout

import resources.gui_strings as s
from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import LimiterMode


class Modification:
    """ A custom class to store the identifier for each modification.
    Methods:
         __init__(mode, values)
         __hash__() -> hash: required for dictionary
         __eq__(other) -> bool: required for dictionary
         generate_label_str() -> str: returns the string that is used to represent this mod
    """
    mode: LimiterMode
    values: list[int]  # Sorted

    def __init__(self, mode: LimiterMode, values: list[int]):
        self.mode = mode
        self.values = sorted(values)
        # Not worrying about error checking for correct values as the way this is created we know
        # the value list must be the correct size unless something has gone terribly wrong

    def __hash__(self):
        return hash((self.mode, "".join([str(v) for v in self.values])))

    def __eq__(self, other: 'Modification') -> bool:
        return self.mode == other.mode and self.values == other.values

    def generate_label_str(self):
        if self.mode == LimiterMode.NO_SELECTOR:
            return s.limiter_applied_label_none()
        if self.mode == LimiterMode.BETWEEN:
            return s.limiter_applied_label_between(self.values[0], self.values[1])
        return s.limiter_applied_label_from_or_to(self.mode, self.values[0])


class LimiterCurrentlyApplied(QVBoxLayout):
    """
    A layout containing the list of all currently applied limits for THIS limiter. When it's
    first created the limiter is none
    +---------------+
    |   cur applied |
    +---------------+
    |      app 1    |
    |      app 2    |
    |      ...      |
    +---------------+
    """
    parent: 'LimiterOverlay'
    direction: LimiterDirection
    current_mods: dict[Modification: QLabel]

    def __init__(
            self,
            direction: LimiterDirection,
            parent: 'LimiterOverlay' = None):
        super().__init__()
        self.parent = parent
        self.direction = direction
        mod = Modification(LimiterMode.NO_SELECTOR, [])
        self.current_mods = {mod: QLabel(mod.generate_label_str())}

        self.addWidget(QLabel(s.limiter_currently_applied_title()))
        self.addWidget(self.current_mods[mod])

    def add_modification(self, mode: LimiterMode, values: list[int]):
        """ Adds a label representing the given mode to the dictionary. """
        this_mod = Modification(mode, values)
        if this_mod in self.current_mods:
            # TODO: not sure what the best way forward here is --> probs just ignore?? but print
            #  warning?
            raise ValueError(s.limiter_applied_already_exists(mode, values))

        self.current_mods[this_mod] = QLabel(this_mod.generate_label_str())
        self.addWidget(self.current_mods[this_mod])
