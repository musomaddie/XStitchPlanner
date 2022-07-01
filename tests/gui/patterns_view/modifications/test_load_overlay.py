from unittest.mock import call, patch

import pytest

from gui.patterns_view.modifications.load_overlay import LoadOverlay

FILE_LOC = "gui.patterns_view.modifications.load_overlay"


@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
def test_init(add_widget_mock, button_mock):
    overlay = LoadOverlay("testing")

    button_mock.assert_called_once_with("Show Saved Variants")
    add_widget_mock.assert_called_once_with(button_mock.return_value)

    assert overlay.load_show_options == button_mock.return_value


@pytest.mark.parametrize(
    ("all_files", "expected_files"),
    [(["testing.pat",
       "testing--row--col--variant.pat",
       "testing-row-from[5]-col--variant.pat",
       "testing-row--col-between[2_3]-variant.pat",
       "testing-row-from[5]to[12]-col-from[3]to[5].pat"],
      ["testing-row-from[5]-col--variant",
       "testing-row--col-between[2_3]-variant",
       "testing-row-from[5]to[12]-col-from[3]to[5]"]),
     (["testing.pat"], []),
     (["testing.pat", "testing-not-a-pat-file"], []),
     (["testing.pat", "testing-row-from[5]-col--variant.pat"],
      ["testing-row-from[5]-col--variant"])]
)
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
@patch(f"{FILE_LOC}.listdir")
@patch(f"{FILE_LOC}.isfile")
def test_find_all_variants(
        isfile_mock, listdir_mock, add_widget_mock, button_mock, all_files, expected_files):
    isfile_mock.return_value = True
    listdir_mock.return_value = all_files
    load_overlay = LoadOverlay("testing")
    assert load_overlay.find_all_variants_filenames() == expected_files


@pytest.mark.parametrize(
    ("variant_filename", "expected"),
    [("testing-row-from[5]-col--variant", "From row 5"),
     ("testing-row--col-from[5]-variant", "From column 5"),
     ("testing-row-from[3]to[10]-col--variant", "From row 3 to row 10"),
     ("testing-row--col-between[1_12]-variant", "Between columns 1 and 12"),
     ("testing-row-between[2_22]-col--variant", "Between rows 2 and 22"),
     ("testing-row-from[6]-col-to[3]-variant", "From row 6, to column 3")]
)
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
def test_make_label_text(add_widget_mock, button_mock, variant_filename, expected):
    load_overlay = LoadOverlay("testing")
    assert load_overlay.make_label_text(variant_filename) == expected


@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
@patch(f"{FILE_LOC}.LoadOverlay.make_label_text")
@patch(f"{FILE_LOC}.LoadOverlay.find_all_variants_filenames")
def test_list_all_variants(
        find_all_vars_fn_mock, make_label_text_mock, add_widget_mock, button_mock):
    # Adding return values, so I can check the dict at the end
    make_label_text_mock.side_effect = ["1", "2"]
    find_all_vars_fn_mock.return_value = ["testing-row-from[5]-col--variant",
                                          "testing-row--col-from[5]-variant"]

    load_overlay = LoadOverlay("testing")
    resulting_dict = load_overlay.list_all_variants()
    make_label_text_mock.assert_has_calls(
        [call("testing-row-from[5]-col--variant"),
         call("testing-row--col-from[5]-variant")])
    find_all_vars_fn_mock.assert_called_once()

    print(resulting_dict)
    assert len(resulting_dict) == 2
    assert "1" in resulting_dict
    assert "2" in resulting_dict
