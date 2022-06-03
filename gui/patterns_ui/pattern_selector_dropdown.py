from os import listdir
from os.path import isfile, join

from PyQt6.QtWidgets import QComboBox


class PatternSelectorDropDownLayout(QComboBox):
    """ Responsible for the drop down box containing a choice of patterns.

    Methods:
        __init__(self):                         initialises a new drop down box
                                                and populates it
    """

    def __init__(self):
        """ Initialises a new pattern selector dropdown instance containing all
        the viable file names.
        """
        super().__init__()
        self.addItems(find_all_patterns())


def find_all_patterns():
    """ Finds all the patterns that have both a .key file and a .pat file and
    returns the pattern name

    Returns
        list [str]      a list where each item is a different pattern name.
    """
    all_pattern_related_files = [
        f for f in listdir("patterns/") if isfile(join("patterns/", f))]

    key_files = [
        f.split(".")[0] for f in all_pattern_related_files if ".key" in f]
    pat_files = [
        f.split(".")[0] for f in all_pattern_related_files if ".pat" in f]

    return sorted([file_name for file_name in key_files if file_name in pat_files])
