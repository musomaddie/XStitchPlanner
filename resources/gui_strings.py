""" This is a file to store all the strings used in the GUI application.

Try and keep in alphabetical order

"""
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode


def apply_button() -> str:
    return "Apply!"


def cell_display(dim: str, value: int) -> str:
    return f"({dim}:) {value + 1}"


def cell_display_title() -> str:
    return "Currently selected cell: "


def limit_prompt(mode: LimiterMode) -> str:
    return f"{mode.value.title()}:"


def limiter_applied_label_none() -> str:
    return "None"


def limiter_applied_label_between(v1: int, v2: int) -> str:
    return f"Between {v1 + 1} and {v2 + 1}"


def limiter_applied_label_from_or_to(mode: LimiterMode, v: int) -> str:
    return f"{mode.value.title()}: {v + 1}"


def limiter_applied_already_exists(mode: LimiterMode, values: list[int]) -> str:
    return f"Modification with {mode} -> {' '.join([str(v) for v in values])} already exists"


def limiter_currently_applied_title() -> str:
    return "Limits Currently Applied:"


def limiter_from_desc(direction: LimiterDirection) -> str:
    if direction == LimiterDirection.COLUMN:
        return "Only shows the pattern right (inclusive) of the provided column value"
    return "Only shows the pattern below (inclusive) the provided row value"


def limiter_between_desc(direction: LimiterDirection) -> str:
    return f"Only shows the pattern between (inclusive) the provided {direction} values"


def limiter_remove_desc(direction: LimiterDirection) -> str:
    return f"Removes any currently applied {direction.value} limits"


def limiter_title(direction: LimiterDirection) -> str:
    return f"Limit patterns via {direction.value.lower()}s"


def limiter_to_desc(direction: LimiterDirection) -> str:
    if direction == LimiterDirection.COLUMN:
        return "Only shows the pattern left (inclusive) of the provided column value"
    return "Only shows the pattern above (inclusive) the provided row value"


def limiter_use_current_cell_desc(direction: LimiterDirection) -> str:
    return f"Use current {direction.value}"


def load_variant() -> str:
    return "Load This Variant"


def original_pattern(name: str) -> str:
    return f"{name} (Original)"


def pattern_selector_title() -> str:
    return "Select the pattern to view"


def pattern_selector_select() -> str:
    return "Select this pattern"


def program_title() -> str:
    return "Stitch Please!"


def start_stitching_title() -> str:
    return "Stitch This!"
