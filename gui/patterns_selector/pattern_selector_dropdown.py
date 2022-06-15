from os import listdir
from os.path import isfile, join

from PyQt6.QtWidgets import QComboBox


class PatternSelectorDropDownWidget(QComboBox):
    """ Responsible for the dropdown box containing a choice of patterns.

    Parameters:
        pattern_names(list[str]):   a list containing all the possible pattern
                                        names
        selected_pattern(str):  currently selected pattern

    Methods:
        __init__(): initialises a new dropdown box and populates it
        activated(int): updates the currently selected whenever the box is
            updated
    """

    def __init__(self):
        super().__init__()
        self.pattern_names = find_all_patterns()
        self.addItems(self.pattern_names)
        self.selected_pattern = self.pattern_names[0]  # default to first name
        self.activated.connect(self.update_currently_selected)

    def update_currently_selected(self):
        self.selected_pattern = self.pattern_names[self.currentIndex()]


def find_all_patterns():
    """ Finds all the patterns that have both a .key file and a .pat file and
    returns the pattern name

    Returns
        list [str]      a list where each item is a different pattern name.
    """
    all_pattern_related_files = [
        f for f in listdir("patterns/") if isfile(join("patterns/", f))]

    key_files = [
        f.split(".")[0] for f in all_pattern_related_files
        if f.endswith(".key")]
    pat_files = [
        f.split(".")[0] for f in all_pattern_related_files
        if f.endswith(".pat")]

    return sorted(
        [file_name for file_name in key_files if file_name in pat_files])
