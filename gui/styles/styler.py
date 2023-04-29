# """ This is how I'm doing tokens now. (?) """
# SPECIAL_KEYS = {}
import json

TOKENS = json.load(open("gui/styles/tokens/theme.json"))

TOKENS_LOOKUP = {
    "colour": lambda colour_name: TOKENS["schemes"]["light"][colour_name]
}


def _get_value(given_value: str | int) -> str:
    """ Given a value returns it formatted for use within CSS styling. 

    Args:
        given_value (str | int): handles any conversions that must happen to the given value (e.g. replacing the
        token value with the actual value, and adding px to ints).

    Returns:
        str: qss string
    """
    if type(given_value) == str:
        if given_value.startswith("token"):
            return _process_token(given_value)
        return given_value
    if type(given_value) == int:
        return f"{given_value}px"


def _process_block(block_name: str, block_contents: dict) -> str:
    """ Processes a particular style block.

    Args:
        block_name: the name of the block (will be the qss selector).
        block_contents: the values the block should contain.

    Returns:
        str: the qss string for the given block
    """
    block_str = f"{block_name} {{"
    for style in block_contents:
        block_str += f"{style}: {_get_value(block_contents[style])};"
    block_str += "}"

    return block_str


def _process_token(given_token_name: str) -> str:
    """ Replaces the given token with an actual(!) value. The given token name must be in the following form:
        token-type-value
        "token" identifies this as a token we should look up, "type" tells us the type of this token (and thus
        directs us through the theme file) and value is the actual value of this token and should match the
        corresponding value within theme.json.

    Args:
        given_token_name: the name of the token to look up and must be in token-type-value form described above.

        Should be able to be split into (at least) 3 parts using
        the dash (-). The three parts are as follows: token-type-identifier. The tok

    Returns:
        str: the actual value of the token
    """
    token_parts = given_token_name.split("-")
    return TOKENS_LOOKUP[token_parts[1]](token_parts[2])


def generate_style_sheet(component_name: str) -> str:
    """ Given a component name, returns the corresponding style sheet as a string.

    Args:
        component_name (object): the name of the stylesheet to load. Should correspond to a file name within
        gui/styles/stylesheets/

    Returns:
        str: the corresponding style sheet in qss syntax.
    """
    provided_styles = json.load(open(f"gui/styles/stylesheets/{component_name}.json"))
    output_styles_str = ""
    for identifier in provided_styles:
        output_styles_str += _process_block(identifier, provided_styles[identifier])

    return output_styles_str
