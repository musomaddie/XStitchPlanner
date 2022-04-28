from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class PatternSelectorLayout(QVBoxLayout):

    def __init__(self):
        super().__init__()

        label = QLabel("Hello World this is vbox")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(label)
