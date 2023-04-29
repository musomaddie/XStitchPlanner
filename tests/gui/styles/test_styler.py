import string

from gui.styles.styler import generate_style_sheet, _process_block, _get_value, _process_token


# TODO: add testing util to conftest to test strings without whitespace!

def remove_whitespace(s1, s2):
    remove = string.whitespace
    return s1.replace(remove, ""), s2.replace(remove, "")


class TestGetValue:
    def test_int(self):
        assert _get_value(20) == "20px"

    def test_simple_str(self):
        assert _get_value("simple-string") == "simple-string"


class TestProcessBlock:
    def test_simple(self):
        result = _process_block("identifier-name", {"key 1": "value 1"})
        assert result == "identifier-name {key 1: value 1;}"


class TestProcessToken:
    def test_colour_token(self):
        assert _process_token("token-colour-primary") == "#6543D0"


def test_contents_example():
    result = generate_style_sheet("contents")
    result, expected = remove_whitespace(
        result, "#contents {background-color: #E0E2EC;}")
    assert result == expected
