""" This is a file to store all the strings used in the GUI application.

Try and keep in alphabetical order

"""


def apply_button() -> str:
    return "Apply!"


def cell_display(dim: str, value: int) -> str:
    return f"({dim}:) {value + 1}"


def cell_display_title() -> str:
    return "Currently selected cell: "


def limit_column_from_desc() -> str:
    return "Only shows the pattern right (inclusive) of the provided column " \
           "number"


def limit_column_from_prompt() -> str:
    return "From: "


def limit_column_remove_desc() -> str:
    return "Removes any currently applied column limits"


def limit_column_to_desc() -> str:
    return "Only shows the pattern left (inclusive) of the provided column " \
           "number"


def limit_column_to_prompt() -> str:
    return "To: "


def limit_use_current_cell_desc(dim: str) -> str:
    return f"Use current {dim}"


def pattern_selector_title() -> str:
    return "Select the pattern to view"


def pattern_selector_select() -> str:
    return "Select this pattern"


def program_title() -> str:
    return "Stitch Please!"
