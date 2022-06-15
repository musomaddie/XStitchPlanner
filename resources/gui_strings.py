""" This is a file to store all the strings used in the GUI application.

Try and keep in alphabetical order

"""


def apply_button() -> str:
    return "Apply!"


def cell_display(dim: str, value: int) -> str:
    return f"({dim}:) {value + 1}"


def cell_display_title() -> str:
    return "Currently selected cell: "


def from_column_limit_desc() -> str:
    return "Only shows the pattern right (inclusive) of the provided column " \
           "number"


def from_column_prompt() -> str:
    return "From:"


def pattern_selector_title() -> str:
    return "Select the pattern to view"


def pattern_selector_select() -> str:
    return "Select this pattern"


def program_title() -> str:
    return "Stitch Please!"


def remove_column_limit_desc() -> str:
    return "Removes any currently applied column limits"


def use_selected_desc(dim: str) -> str:
    return f"Use current {dim}"
