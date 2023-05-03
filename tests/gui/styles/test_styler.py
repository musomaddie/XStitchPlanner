import string

from gui.styles.styler import (generate_style_sheet, _process_block, _get_value, _process_token,
    _calculate_border_radius, _set_dimension)


# TODO: add testing util to conftest to test strings without whitespace!

def remove_whitespace(s1, s2):
    remove = string.whitespace
    return s1.replace(remove, ""), s2.replace(remove, "")


class TestCalculateBorderRadius:
    def test_number(self):
        assert _calculate_border_radius(10) == "border-radius: 10px;"

    def test_string_with_tokens(self):
        assert (
                _calculate_border_radius("token-shape-largeEnd") ==
                "border-top-right-radius: 16px;border-bottom-right-radius: 16px;"
        )


class TestGetValue:
    def test_int(self):
        assert _get_value(20) == "20px"

    def test_simple_str(self):
        assert _get_value("simple-string") == "simple-string"

    def test_list(self):
        assert _get_value([1, 2, 3, "4"]) == "1px 2px 3px 4"


class TestProcessBlock:
    def test_simple(self):
        result = _process_block("identifier-name", {"key 1": "value 1"})
        assert result == "identifier-name {key 1: value 1;}"


class TestProcessToken:
    def test_colour_token(self):
        assert _process_token("token-colour-primary") == "#6543D0"

    def test_shape_token(self):
        assert _process_token("token-shape-large") == "16px"


class TestSetDimension:
    def test_set_dimension(self):
        assert _set_dimension("width", 20) == "min-width: 20; max-width: 20;"


def test_contents_example():
    result = generate_style_sheet("contents")
    result, expected = remove_whitespace(
        result, "#contents {background-color: #DAD9DD;}")
    assert result == expected
