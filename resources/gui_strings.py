""" This is a file to store all the strings used in the GUI application.

Try and keep in alphabetical order

"""
from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import LimiterMode


def apply_button() -> str:
    return "Apply!"


def cell_display(dim: str, value: int) -> str:
    return f"({dim}:) {value + 1}"


def cell_display_title() -> str:
    return "Currently selected cell: "


def limit_prompt(mode: LimiterMode) -> str:
    return f"{mode.value.title()}:"


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


def pattern_selector_title() -> str:
    return "Select the pattern to view"


def pattern_selector_select() -> str:
    return "Select this pattern"


def program_title() -> str:
    return "Stitch Please!"
