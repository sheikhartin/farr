# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import pytest

from farr.lexer import FarrRegexLexer


@pytest.fixture(scope='session')
def farr_regex_lexer_fixture() -> FarrRegexLexer:
    """Returns an instance of `FarrRegexLexer`."""
    return FarrRegexLexer()
