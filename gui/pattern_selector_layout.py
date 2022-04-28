from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

def create_pattern_selector_layout():
    vbox = QVBoxLayout()
    label = QLabel("Hello World this is vbox")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    vbox.addWidget(label)

    return vbox
