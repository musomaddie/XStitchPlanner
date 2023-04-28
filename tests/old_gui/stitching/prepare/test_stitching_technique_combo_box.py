from unittest.mock import patch

from gui.stitching.prepare.stitching_technique_combo_box import StitchingTechniqueComboBox

FILE_LOC = "old_gui.stitching.prepare.stitching_technique_combo_box"


@patch(f"{FILE_LOC}.StitchingTechniqueComboBox.addItems")
def test_init(add_items_mock):
    combo_box = StitchingTechniqueComboBox()

    add_items_mock.assert_called_once_with(["Parking"])

    assert combo_box.stitching_techniques == ["Parking"]
