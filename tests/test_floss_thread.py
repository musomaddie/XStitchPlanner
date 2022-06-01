from floss_thread import Thread


# This is a pretty boring test but its probably still worth having.

def test_FlossThread_init():
    dmc_value = "310"
    identifier = "@"
    symbol = "@"
    name = "Black"
    hex_colour = "000000"

    created_thread = Thread(dmc_value, identifier, symbol, name, hex_colour)

    assert created_thread is not None

    assert created_thread.dmc_value == dmc_value
    assert created_thread.identifier == identifier
    assert created_thread.symbol == symbol
    assert created_thread.name == name
    assert created_thread.hex_colour == hex_colour
