""" This is a file to store all the strings used in the GUI application. """


def apply_button():
    return "Apply!"


def cell_display(dim: str, value: int) -> str:
    return f"({dim}:) {value + 1}"


def cell_display_title():
    return "Currently selected cell: "


def pattern_selector_title():
    return "Select the pattern to view"


def pattern_selector_select():
    return "Select this pattern"


def program_title():
    return "Stitch Please!"


def remove_column_limit_desc():
    return "Removes any currently applied column limits"
