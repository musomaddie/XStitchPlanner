from os import listdir
from os.path import isfile, join

from PyQt6.QtWidgets import QComboBox


class PatternSelectorChoice(QComboBox):
    """ Responsible for the drop down box containing a choice of patterns.

    Parameters:
        patternNames    list[str]       the name of all possible pattern
                                        options, ordered alphabetically

    Methods:
        __init__(self):                         initialises a new drop down box
                                                and populates it
        findViablePatterns(self, directory)     updates the patternNames to
                                                match all viable patterns
                                                within the given directory
    """

    def __init__(self):
        """ Initialises a new pattern selector choice instance and finds all
        viable patterns in the `patterns/` directory.
        """
        super().__init__()
        self.patternNames = []


def find_all_patterns():
    """ Finds all the patterns that have both a .key file and a .pat file and
    returns the pattern name
    """
    all_pattern_related_files = [
        f for f in listdir("patterns/") if isfile(join("patterns/", f))]

    key_files = [
        f.split(".")[0] for f in all_pattern_related_files if ".key" in f]
    pat_files = [
        f.split(".")[0] for f in all_pattern_related_files if ".pat" in f]

    return [file_name for file_name in key_files if file_name in pat_files]
