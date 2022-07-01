from os import listdir
from os.path import isfile

from PyQt6.QtWidgets import QPushButton, QVBoxLayout

import resources.gui_strings as s


class LoadOverlay(QVBoxLayout):
    """
    Handles the overall layout for loading a previously saved configuration. Initially everything is
    compressed into one button which when clicked expands out the layout. (I HOPE)
    +---------------+
    |   LOAD        |
    +---------------+
    """
    parent: 'StitchingOptMenuOverview'
    original_pattern_name: str
    load_show_options: QPushButton

    # TODO: it makes more sense for this to be a dropdown

    def __init__(self, pattern_name: str, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        # TODO: don't show if no pattern modifiers saved!
        self.parent = parent
        self.original_pattern_name = pattern_name

        self.load_show_options = QPushButton(s.load_variants_show_desc())
        self.addWidget(self.load_show_options)

    def list_all_variants(self) -> dict[str, str]:
        """
        Finds and returns all the different saved variants for this pattern.

        Returns:
            dict[str, str]: a dictionary with the display string mapped to the actual pattern name.
        """
        return {self.make_label_text(fn): fn for fn in self.find_all_variants_filenames()}

    @staticmethod
    def make_label_text(variant_filename: str) -> str:
        """ Generates the user readable text describing the given variant

        Args:
            variant_filename: the full filename of the variant to make user readable

        Returns:
            a string which will be used for displaying this variant
        """

        def helper(direction_str, direction, add_bool_start=True, add_bool_capitalise_dir=True):
            resulting_str = "" if add_bool_start else ","
            for mod in direction:
                if mod == "":
                    continue
                mode, value = mod.split("[")
                mode_str = (mode.title()
                            if resulting_str == "" and add_bool_capitalise_dir
                            else f" {mode}")
                if mode == "between":
                    v1, v2 = value.split("_")
                    resulting_str += f"{mode_str} {direction_str}s {v1} and {v2}"
                else:
                    resulting_str += f"{mode_str} {direction_str} {value}"
            return resulting_str

        values = variant_filename.split("-")
        row_idx, col_idx = 2, 4
        row_str = helper("row", values[row_idx].split("]"))
        col_str = helper(
            "column",
            values[col_idx].split("]"),
            add_bool_start=row_str == "" or values[col_idx] == "",
            add_bool_capitalise_dir=row_str == ""
        )
        return f"{row_str}{col_str}"

    def find_all_variants_filenames(self) -> list[str]:
        """ Finds all the variants of this pattern

        Returns:
            a list of strings where every string is the .pat file with the variant
        """
        all_files = [f for f in listdir("patterns/") if isfile()]
        return [f.split(".")[0] for f in all_files
                if f.startswith(self.original_pattern_name) and f.endswith(".pat")
                and f != f"{self.original_pattern_name}.pat"
                and f != f"{self.original_pattern_name}--row--col--variant.pat"]
