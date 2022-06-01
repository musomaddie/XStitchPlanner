from unittest.mock import MagicMock

from extractors.extractor import Extractor


def test_Init():
    pattern_name = "Testing"
    made_extractor = Extractor(MagicMock(), pattern_name)

    assert made_extractor.key_filename == f"{pattern_name}.key"
    assert made_extractor.pattern_filename == f"{pattern_name}.pat"
