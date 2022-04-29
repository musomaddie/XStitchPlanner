from extract_key import extract_key_from_pdf
from extractors.extractor_mode import ExtractorMode

import pytest

def test_ExtractKeyFromPdf_InvalidKey():
    with pytest.raises(ValueError):
        extract_key_from_pdf("Testing",
                             ExtractorMode.UNKNOWN)
