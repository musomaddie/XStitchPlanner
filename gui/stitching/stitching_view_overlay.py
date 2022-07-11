from PyQt6.QtWidgets import QStackedWidget, QWidget

from gui.stitching.prepare.prepare_stitching_view_overlay import PrepareStitchingViewOverlay


class StitchingViewOverlay(QStackedWidget):
    prepare_layout: PrepareStitchingViewOverlay
    parent: 'StitchingOverlay'

    def __init__(self, model: 'PrepareStitchingDisplayModel', parent: 'StitchingOverlay' = None):
        super().__init__()
        self.parent = parent

        self.prepare_layout = PrepareStitchingViewOverlay(model, self)
        prepare_layout_layout_widget = QWidget()
        prepare_layout_layout_widget.setLayout(self.prepare_layout)
        self.addWidget(prepare_layout_layout_widget)
