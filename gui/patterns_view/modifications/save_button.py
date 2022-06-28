from PyQt6.QtWidgets import QPushButton


class SaveButton(QPushButton):

    parent: 'StitchingOptMenuOverview'

    def __init__(self, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()

        self.parent = parent
        self.setText("Save these modifications")
