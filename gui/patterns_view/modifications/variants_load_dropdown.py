from os import listdir
from os.path import isfile, join

from PyQt6.QtWidgets import QComboBox

from pattern_cells.pattern_cell import PatternCell
from utils import load_from_pattern_file


class VariantsLoadDropDown(QComboBox):
    """ Responsible for the dropdown box containing the list of variants that can be loaded for
    the given pattern.

    Methods:
        __init__()
        list_all_variants(): creates a dictionary of user-readable variant description to variant
            filename
        find_all_variants_filename(): loads all the variant filenames

    Static Methods:
        make_label_text(variant_filename): makes a user-readable variant description from the
            variant filename
    """
    parent: 'LoadOverlay'
    original_pattern_name: str
    all_variants: dict[str, str]

    def __init__(self, pattern_name: str, parent: 'LoadOverlay' = None):
        super().__init__()
        self.parent = parent
        self.original_pattern_name = pattern_name
        self.all_variants = self.list_all_variants()
        self.addItems([desc for desc in self.all_variants.keys()])

    def get_pattern_model_from_selected_variant(self) -> list[list[PatternCell]]:
        """ Returns the pattern model that's found in the file of the selected variant """
        return load_from_pattern_file(
            self.original_pattern_name, self.all_variants[self.currentText()])

    def list_all_variants(self) -> dict[str, str]:
        """
        Finds and returns all the different saved variants for this pattern.

        Returns:
            dict[str, str]: a dictionary with the display string mapped to the actual pattern name.
        """
        return {self.make_label_text(fn): fn
                for fn in self.find_all_variants_filenames()
                if fn != f"{self.original_pattern_name}-row--col--variant"}

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
        all_files = [f for f in listdir("patterns/") if isfile(join("patterns/", f))]
        return [f.split(".")[0] for f in all_files
                if f.startswith(self.original_pattern_name) and f.endswith(".pat")
                and f != f"{self.original_pattern_name}.pat"
                and f != f"{self.original_pattern_name}--row--col--variant.pat"]
