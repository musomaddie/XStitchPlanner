from PyQt6.QtWidgets import QHeaderView, QTableView


class PatternView(QTableView):
    """ A super class for displaying the pattern in a table form.
    Does not contain a parent variable as this is the responsibility of its child classes.
    """
    model: 'PatternModel'

    def __init__(self, model: 'PatternModel'):
        super().__init__()
        self.model = model
        self.setModel(self.model)
        self.model.add_display(self)
        # Using ResizeMode.Fixed to control the size of the cells as using a more dynamic resize
        # caused the program to take a long time loading
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setMinimumSectionSize(20)
        self.horizontalHeader().setDefaultSectionSize(20)

        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setMinimumSectionSize(20)
        self.verticalHeader().setDefaultSectionSize(20)

        current_font = self.font()
        current_font.setPointSize(8)
        self.horizontalHeader().setFont(current_font)
        self.verticalHeader().setFont(current_font)
