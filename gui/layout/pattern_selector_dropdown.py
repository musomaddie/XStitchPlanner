from PyQt6.QtWidgets import QComboBox
from os import listdir
from os.path import isfile, join

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
        self.findViablePatterns()

    def findViablePatterns(self, directory="patterns/"):
        """ Finds all viable patterns in the given directory and assigns it to
        patternNames.

        Parameters:
            directory   str     the directory of where to look for patterns.
                                [default: 'patterns/']
        """
        fileList = [f for f in listdir(directory)
                    if isfile(join(directory, f))]
        print(fileList)
        return []
        # file_list = [f for f in listdir("patterns/") if isfile(join(
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))
