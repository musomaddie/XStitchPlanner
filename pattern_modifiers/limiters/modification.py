import resources.gui_strings as s
from pattern_modifiers.limiters.limiter_mode import LimiterMode


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
