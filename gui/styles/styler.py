# """ This is how I'm doing tokens now. (?) """
# SPECIAL_KEYS = {}
import json
import logging
from abc import ABC, abstractmethod
from enum import Enum, auto

from PyQt6.QtCore import QSize

MINIMUM_TOUCH_TARGET_SIZE_PX = 48
MINIMUM_TOUCH_TARGET_SIZE = QSize(MINIMUM_TOUCH_TARGET_SIZE_PX, MINIMUM_TOUCH_TARGET_SIZE_PX)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class ProcessState(Enum):
    UNGENERATED = auto()
    GENERATED = auto()


class StyleGenerator(ABC):

    def __init__(self):
        self.state = ProcessState.UNGENERATED
        self.generated_style = ""

    @abstractmethod
    def _generate_style(self):
        pass

    def get_style(self):
        if self.state == ProcessState.UNGENERATED:
            self._generate_style()
        return self.generated_style


class TokenGenerator(StyleGenerator):
    """ Handles the lookup for token values passed.

    Accepts the following token types:
        - colour
        - shape
        - size
    """
    _tokens = json.load(open("gui/styles/tokens/theme.json"))

    def _generate_style(self):
        token_parts = self.token_name.split("-")
        if token_parts[1] == "colour":
            self.generated_style = self._tokens["schemes"]["light"][token_parts[2]]
        elif token_parts[1] == "shape":
            self.generated_style = ValueGenerator(self._tokens["shapes"][token_parts[2]]).get_style()
        elif token_parts[1] == "size":
            self.generated_style = ValueGenerator(self._tokens["sizes"][token_parts[2]]).get_style()
        else:
            raise NotImplementedError(f"The token generator does not yet support {token_parts[2]}.")
        self.state = ProcessState.GENERATED

    def __init__(self, token_name: str):
        super().__init__()
        self.token_name = token_name


class ValueGenerator(StyleGenerator):
    """ Wraps a value given after the colon, e.g. 40.

    Handles the following value types:
        - string
        - string (token)
        - int
        - list
    """

    def __init__(self, value: str | int | list):
        super().__init__()
        self.value = value

    def _generate_style(self):
        if type(self.value) == str:
            self.generated_style = (
                TokenGenerator(self.value).get_style()
                if self.value.startswith("token")
                else self.value)
        elif type(self.value) == int:
            self.generated_style = "0%" if self.value == 0 else f"{self.value}px"
        elif type(self.value) == list:
            self.generated_style = " ".join(
                [ValueGenerator(value).get_style() for value in self.value])
        else:
            raise NotImplementedError(f"Value of type {type(self.value)} is not supported")
        self.state = ProcessState.GENERATED


class LayoutTypeGenerator(StyleGenerator):
    """ Wraps a style on a single line (e.g. font-size: 40).

    Handles the following list of possible special cases:
        - border-radius
        - height
        - width
    """

    def _generate_style(self):
        if self.layout_type == "border-radius":
            if type(self.layout_value) != str or not self.layout_value.startswith("token"):
                value_style = ValueGenerator(self.layout_value).get_style()
                self.generated_style = f"border-radius: {value_style};"
            else:
                values = TokenGenerator(self.layout_value).get_style().split(" ")
                if len(values) == 4:
                    ident_list = ["top-left", "top-right", "bottom-right", "bottom-left"]
                    for (value, ident) in zip(values, ident_list):
                        if value != "0%":
                            self.generated_style += f"border-{ident}-radius: {value};"
                else:
                    self.generated_style = f"border-radius: {values[0]};"
        elif self.layout_type == "height" or self.layout_type == "width":
            self._set_dimension(ValueGenerator(self.layout_value).get_style())
        else:
            value_style = ValueGenerator(self.layout_value)
            self.generated_style = f"{self.layout_type}: {value_style.get_style()};"
        self.state = ProcessState.GENERATED

    def _set_dimension(self, given_value: str):
        self.generated_style = f"min-{self.layout_type}: {given_value}; max-{self.layout_type}: {given_value};"

    def __init__(self, layout_type: str, layout_value: str | list | int):
        super().__init__()
        self.layout_type = layout_type
        self.layout_value = layout_value


class SelectorGenerator(StyleGenerator):
    """ Wraps an entire style selector (e.g. h1 { ... } ).

    Handles the following special cases:
        - additionally_generate: also load the styles of the listed layout components.

    """

    def _generate_style(self):
        if self.selector_name == "additionally_generate":
            self.generated_style = "\n".join([Styler(component).get_style() for component in self.values])
        else:
            self.generated_style = f"{self.selector_name} {{"
            for value in self.values:
                self.generated_style += LayoutTypeGenerator(value, self.values[value]).get_style()
            self.generated_style += "}"
        self.state = ProcessState.GENERATED
        logging.debug(f"\tgenerated style for {self.selector_name} as - {self.generated_style}")

    def __init__(self, selector_name: str, values: dict | list):
        super().__init__()
        self.selector_name = selector_name
        self.values = values


class Styler(StyleGenerator):
    """ Handles styling an entire file, given the component_name (filename). """

    def _generate_style(self):
        self.generated_style = "\n".join(
            [SelectorGenerator(key, value).get_style() for key, value in self.provided_styles_json.items()])
        self.state = ProcessState.GENERATED

    def __init__(self, component_name: str):
        super().__init__()
        self.component_name = component_name
        self.provided_styles_json = json.load(open(f"gui/styles/stylesheets/{self.component_name}.json"))
