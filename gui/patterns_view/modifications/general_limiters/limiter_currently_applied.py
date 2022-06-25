from PyQt6.QtWidgets import QLabel, QVBoxLayout

import resources.gui_strings as s
from pattern_cell import PatternCell
from pattern_modifiers.limiters.limit_applier import LimitApplier
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode


# TODO: move to own class!
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
    # TODO: add undo
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
    applier: LimitApplier

    def __init__(
            self,
            model: 'PatternDisplayModel',
            direction: LimiterDirection,
            current_mod: Modification,
            parent: 'LimiterOverlay' = None):
        super().__init__()
        self.parent = parent
        self.direction = direction
        self.addWidget(QLabel(s.limiter_currently_applied_title()))

        # If the current_mod is None we need to set up for the no selector
        self.applier = LimitApplier(direction, model._data, current_mod)
        self.current_mods = {current_mod: QLabel(current_mod.generate_label_str())}
        self.addWidget(self.current_mods[current_mod])

    def add_modification(self, mode: LimiterMode, values: list[int]):
        """ Adds a label representing the given mode to the dictionary. """
        # TODO: sanity check for blank --> if no selector passed when already blank it just
        #  crashes which is sad :(
        this_mod = Modification(mode, values)
        if this_mod in self.current_mods:
            # TODO: not sure what the best way forward here is --> probs just ignore?? but print
            #  warning?
            raise ValueError(s.limiter_applied_already_exists(mode, values))

        new_model = self.applier.apply_limit(this_mod)

        # TODO: only call this when desired
        self.create_new_pattern_tab(new_model, this_mod)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modification: Modification) -> None:
        self.parent.create_new_pattern_tab(new_model, modification)

        # TODO: improve this
        #   1) Automatically switch to new tab (DONE)
        #   2) Move the applied limits to this tab instead of the current one: will need to be
        #   separate). (DONE)
        #   3) (next commit): don't assign another tab after first one unless asked and make sure
        #   it's all the modifiers being passed not just the next one.
