""" This is a file to store all the strings used throughout the program.
They are all being saved as a method so that I can use f strings easily.
"""
def extractor_load_success():
    return "Successfully loaded the extractor"

def extractor_error():
    return ("The extractor mode is unknown. It should either be 'font' or "
            "'shape'")

def key_load_success():
    return "Successfully loaded the key"

def page_number_error(string):
    return (f"'{string}' is not a valid page number as it is not a number. "
            "Please provide a valid number.")
