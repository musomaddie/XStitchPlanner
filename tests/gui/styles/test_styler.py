import json
import string
from pathlib import Path

import pytest

from gui.styles.styler import (ValueGenerator, TokenGenerator, ProcessState, LayoutTypeGenerator, SelectorGenerator,
    Styler)


# TODO: add testing util to conftest to test strings without whitespace!

def remove_whitespace(s1, s2):
    remove = string.whitespace
    return s1.replace(remove, ""), s2.replace(remove, "")


class TestValueGenerator:

    def test_string(self):
        gen = ValueGenerator("string")
        assert gen.get_style() == "string"
        assert gen.state == ProcessState.GENERATED

    def test_int_non_zero(self):
        gen = ValueGenerator(1)
        assert gen.get_style() == "1px"
        assert gen.state == ProcessState.GENERATED

    def test_int_zero(self):
        gen = ValueGenerator(0)
        assert gen.get_style() == "0%"
        assert gen.state == ProcessState.GENERATED

    def test_token(self):
        gen = ValueGenerator("token-colour-surface")
        assert gen.get_style() == "#FAF9FD"
        assert gen.state == ProcessState.GENERATED


class TestTokenGenerator:

    def test_colour(self):
        gen = TokenGenerator("token-colour-surface")
        assert gen.get_style() == "#FAF9FD"
        assert gen.state == ProcessState.GENERATED

    def test_shape(self):
        gen = TokenGenerator("token-shape-large")
        assert gen.get_style() == "16px"
        assert gen.state == ProcessState.GENERATED

    def test_size(self):
        gen = TokenGenerator("token-size-minimumTouch")
        assert gen.get_style() == "48px"
        assert gen.state == ProcessState.GENERATED


class TestLayoutTypeGenerator:

    def test_border_radius(self):
        gen = LayoutTypeGenerator("border-radius", "token-shape-largeEnd")
        assert gen.get_style() == "border-top-right-radius: 16px;border-bottom-right-radius: 16px;"
        assert gen.state == ProcessState.GENERATED

    def test_height(self):
        gen = LayoutTypeGenerator("height", 48)
        assert gen.get_style() == "min-height: 48px; max-height: 48px;"
        assert gen.state == ProcessState.GENERATED

    def test_width(self):
        gen = LayoutTypeGenerator("width", 48)
        assert gen.get_style() == "min-width: 48px; max-width: 48px;"
        assert gen.state == ProcessState.GENERATED

    def test_generic(self):
        gen = LayoutTypeGenerator("font-size", 12)
        assert gen.get_style() == "font-size: 12px;"
        assert gen.state == ProcessState.GENERATED


class TestSelectorGenerator:

    c_name = "testing-component"

    @pytest.fixture
    def fake_component_style_file(self, monkeypatch, tmp_path):
        Path(tmp_path / "gui" / "styles" / "stylesheets").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        with open("gui/styles/stylesheets/testing-component.json", "w") as f:
            json.dump({"h1": {"font-size": 48}}, f)

    def test_simple(self):
        gen = SelectorGenerator("QIcon", {"width": 40, "border": "3px solid red"})
        assert gen.get_style() == "QIcon {min-width: 40px; max-width: 40px;border: 3px solid red;}"
        assert gen.state == ProcessState.GENERATED

    def test_additionally_generate(self, fake_component_style_file):
        gen = SelectorGenerator("additionally_generate", ["testing-component"])
        assert gen.get_style() == "h1 {font-size: 48px;}"
        assert gen.state == ProcessState.GENERATED


class TestStyler:

    c_name = "testing-component"

    @pytest.fixture
    def fake_component_style_file(self, monkeypatch, tmp_path):
        Path(tmp_path / "gui" / "styles" / "stylesheets").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        with open("gui/styles/stylesheets/testing-component.json", "w") as f:
            json.dump({"h1": {"width": 40}, "h2": {"width": 20}}, f)

    @pytest.fixture
    def fake_component_style_second_file(self, monkeypatch, tmp_path):
        with open("gui/styles/stylesheets/another-component.json", "w") as f:
            json.dump({
                "h1": {"font-size": 48}, "additionally_generate": ["testing-component"]
            }, f)

    def test_simple(self, fake_component_style_file):
        gen = Styler(self.c_name)
        assert gen.get_style() == "h1 {min-width: 40px; max-width: 40px;}\nh2 {min-width: 20px; max-width: 20px;}"
        assert gen.state == ProcessState.GENERATED

    def test_with_additionally_generate(self, fake_component_style_file, fake_component_style_second_file):
        gen = Styler("another-component")
        assert gen.get_style() == \
               "h1 {font-size: 48px;}\nh1 {min-width: 40px; max-width: 40px;}\nh2 {min-width: 20px; max-width: 20px;}"
        assert gen.state == ProcessState.GENERATED
