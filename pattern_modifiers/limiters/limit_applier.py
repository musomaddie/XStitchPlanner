"""
Does the actual work of applying the limit to the pattern
"""
import copy

from pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode


class LimitApplier:
    direction: LimiterDirection
    original_pattern: list[list[PatternCell]]
    pattern_current_state: list[list[PatternCell]]
    currently_applied: list['Modification']

    def __init__(
            self,
            direction: LimiterDirection,
            pattern: list[list[PatternCell]],
            original_mod: 'Modification'):
        self.direction = direction
        self.original_pattern = copy.deepcopy(pattern)
        self.pattern_current_state = copy.deepcopy(pattern)
        self.currently_applied = [original_mod]

    def apply_limit(self, modification: 'Modification') -> list[list[PatternCell]]:
        """ Applies the given modification to the pattern"""
        if modification.mode == LimiterMode.NO_SELECTOR:
            self.apply_no_selections(modification)
        elif modification.mode == LimiterMode.FROM:
            self.apply_from(modification)
        elif modification.mode == LimiterMode.TO:
            self.apply_to(modification)
        elif modification.mode == LimiterMode.BETWEEN:
            self.apply_between(modification)

        return copy.deepcopy(self.pattern_current_state)

    def apply_no_selections(self, modification: 'Modification') -> None:
        self.currently_applied = [modification]
        self.pattern_current_state = copy.deepcopy(self.original_pattern)

    def apply_from(self, modification: 'Modification') -> None:
        self._apply_between_helper(modification.values[0], len(self.pattern_current_state))
        self._update_cur_applied_helper(modification)

    def apply_to(self, modification: 'Modification') -> None:
        self._apply_between_helper(0, modification.values[0] + 1)
        self._update_cur_applied_helper(modification)

    def apply_between(self, modification: 'Modification') -> None:
        self._apply_between_helper(modification.values[0], modification.values[1] + 1)
        self._update_cur_applied_helper(modification)

    def _apply_between_helper(self, value_to: int, value_from: int) -> None:
        if self.direction == LimiterDirection.COLUMN:
            self.pattern_current_state = [row[value_to:value_from]
                                          for row in self.pattern_current_state]
        else:
            self.pattern_current_state = self.pattern_current_state[value_to:value_from]

    def _update_cur_applied_helper(self, m: 'Modification') -> None:
        # If the only item is that there's no values attached remove it
        if (len(self.currently_applied) == 1
                and self.currently_applied[0].mode == LimiterMode.NO_SELECTOR):
            self.currently_applied = []

        self.currently_applied.append(m)
