from extractors.extractor_mode import ExtractorMode


def test_from_string():
    assert ExtractorMode.FONT == ExtractorMode.from_string("FONT")
    assert ExtractorMode.SHAPE == ExtractorMode.from_string("SHAPE")
    assert ExtractorMode.UNKNOWN == ExtractorMode.from_string("ahhhhhh")


def test_from_string_case_insensitive():
    assert ExtractorMode.FONT == ExtractorMode.from_string("fOnT")
