from PyQt6.QtWidgets import QComboBox


class StitchingTechniqueComboBox(QComboBox):
    """ Contains a dropdown list of different stitching techniques """
    stitching_techniques: list[str]
    selected_technique: str
    parent: 'PreStitchingOptionsOverlay'

    def __init__(self, parent: 'PreStitchingOptionsOverlay' = None):
        super().__init__()
        self.parent = parent
        self.stitching_techniques = ["Parking"]
        self.selected_technique = self.stitching_techniques[0]
        self.addItems(self.stitching_techniques)

        self.activated.connect(self.update_currently_selected)

    def update_currently_selected(self):
        self.selected_technique = self.stitching_techniques[self.currentIndex()]
