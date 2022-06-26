from PyQt6.QtWidgets import QLabel, QVBoxLayout

import resources.gui_strings as s
from pattern_cell import PatternCell
from pattern_modifiers.limiters.limit_applier import LimitApplier
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode


# TODO: move to own class!
class Modification:
    """ A custom class to store the identifier for each modifications.
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

    def __repr__(self):
        return f"{self.mode.value.upper()} ({', '.join([str(v) for v in self.values])})"

    def generate_label_str(self):
        # TODO: be nice to see these values reflected from the original pattern size (or not at
        #  all tbh).
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
            current_mods: list[Modification],
            parent: 'LimiterOverlay' = None):
        super().__init__()
        self.parent = parent
        self.direction = direction
        self.addWidget(QLabel(s.limiter_currently_applied_title()))

        self.applier = LimitApplier(direction, model._data, current_mods)
        self.current_mods = {current_mod: QLabel(current_mod.generate_label_str())
                             for current_mod in current_mods}
        [self.addWidget(self.current_mods[current_mod]) for current_mod in current_mods]

    def get_all_modifiers(self) -> list[Modification]:
        return list(self.current_mods.keys())

    def add_modification(self, mode: LimiterMode, values: list[int]):
        """ Adds a label representing the given mode to the dictionary. """
        # TODO: sanity check for blank --> if no selector passed when already blank it just
        #  crashes which is sad :(
        this_mod = Modification(mode, values)
        if this_mod in self.current_mods:
            # TODO: not sure what the best way forward here is --> probs just ignore?? but print
            #  warning?
            raise ValueError(s.limiter_applied_already_exists(mode, values))

        mod_list = []
        if (len(self.current_mods) == 1
                and LimiterMode.NO_SELECTOR in [v.mode for v in self.current_mods.keys()]):
            mod_list.append(this_mod)
        else:
            [mod_list.append(m) for m in self.current_mods.keys()]
            mod_list.append(this_mod)

        new_model = self.applier.apply_limit(this_mod)

        self.create_new_pattern_tab(new_model, mod_list)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modifications: list[Modification]) -> None:
        self.parent.create_new_pattern_tab(new_model, modifications)

        # TODO: improve this
        #   don't assign another tab after first one unless asked
