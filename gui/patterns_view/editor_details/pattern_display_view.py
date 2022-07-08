from gui.pattern_display_model import PatternDisplayModel
from gui.pattern_view import PatternView
from gui.patterns_view.editor_details.current_cell_layout import CurrentCellLayout


class PatternDisplayView(PatternView):
    """ Responsible for actually displaying the pattern in a table form. """
    model: PatternDisplayModel
    parent: 'PatternEditorView'

    def __init__(
            self,
            model: PatternDisplayModel,
            current_cell_layout: CurrentCellLayout,
            parent: 'PatternEditorView' = None):
        super().__init__(model)
        self.parent = parent
        self.clicked.connect(current_cell_layout.update_values)
