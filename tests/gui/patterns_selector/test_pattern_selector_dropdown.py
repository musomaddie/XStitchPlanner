from unittest.mock import patch

import pytest

from gui.patterns_selector.pattern_selector_dropdown import find_all_patterns, \
    PatternSelectorDropDownWidget


@pytest.mark.parametrize(
    ("pat_files", "key_files", "expected_pattern_names"),
    ((["first_file.pat", "second_file.pat"],
      ["first_file.key", "second_file.key"],
      ["first_file", "second_file"]),
     (["first_file.pat", "second_file.pat"],
      ["first_file.key"], ["first_file"]),
     (
             ["first_file.pat"], ["first_file.key", "second_file.key"],
             ["first_file"]),
     (["first_file.pat"], ["second_file.key"], [])
     ))
@patch("gui.patterns_selector.pattern_selector_dropdown.listdir")
@patch("gui.patterns_selector.pattern_selector_dropdown.isfile")
def test_find_all_patterns(isfile_mock, listdir_mock,
                           pat_files, key_files, expected_pattern_names):
    isfile_mock.return_value = True
    listdir_mock.return_value = pat_files + key_files
    result = find_all_patterns()

    assert len(result) == len(expected_pattern_names)
    for expected in expected_pattern_names:
        assert expected in result


@patch("gui.patterns_selector.pattern_selector_dropdown.listdir")
@patch("gui.patterns_selector.pattern_selector_dropdown.isfile")
def test_find_all_patterns_sorted(isfile_mock, listdir_mock):
    isfile_mock.return_value = True
    listdir_mock.return_value = [
        "b.pat", "c.pat", "d.pat", "e.pat", "a.pat",
        "b.key", "c.key", "d.key", "e.key", "a.key"]
    expected_names = ["a", "b", "c", "d", "e"]
    result = find_all_patterns()

    assert len(result) == len(expected_names)
    for actual, expected in zip(result, expected_names):
        assert actual == expected


# Patching the find_all_patterns_method to make my life easier as it's
# already been tested
@patch("gui.patterns_selector.pattern_selector_dropdown.find_all_patterns")
def test_pattern_selector_dropdown_layout_init(finder_mock, qtbot):
    finder_mock.return_value = ["a", "b", "c", "d"]
    test_widget = PatternSelectorDropDownWidget()
    qtbot.addWidget(test_widget)

    assert test_widget.pattern_names == ["a", "b", "c", "d"]
    assert test_widget.selected_pattern == "a"


@patch("gui.patterns_selector.pattern_selector_dropdown.find_all_patterns")
def test_pattern_selector_dropdown_layout_on_click(finder_mock, qtbot):
    finder_mock.return_value = ["a", "b", "c", "d"]
    test_widget = PatternSelectorDropDownWidget()
    qtbot.addWidget(test_widget)

    qtbot.keyClicks(test_widget, "b")
    assert test_widget.selected_pattern == "b"
