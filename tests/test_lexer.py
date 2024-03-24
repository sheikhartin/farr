# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import textwrap

import pytest

from farr.lexer import FarrRegexLexer
from farr.lexer.base import TokenState


def test_an_arithmetic_operation_tokenization(
    farr_regex_lexer_fixture: FarrRegexLexer,
) -> None:
    """Checks the output of three plus five."""
    assert farr_regex_lexer_fixture.tokenize('+ 3 5.;') == [
        TokenState(row=1, column=1, name='Add', value='+'),
        TokenState(row=1, column=3, name='Integer', value='3'),
        TokenState(row=1, column=5, name='Float', value='5.'),
        TokenState(row=1, column=7, name='Semicolon', value=';'),
    ]


def test_a_meaningless_code_tokenization(
    farr_regex_lexer_fixture: FarrRegexLexer,
) -> None:
    """Checks the generated tokens of a meaningless program."""
    assert (
        farr_regex_lexer_fixture.tokenize(
            textwrap.dedent(
                """
                let mylist = {-1, 0, .2, +1, 2., 3.0};
                for let i in mylist = {
                  break!;
                  println("Sorry, nothing from the list was printed!");
                }
                """
            )
        )
        == [
            TokenState(row=2, column=1, name='Variable', value='let'),
            TokenState(row=2, column=5, name='Identifier', value='mylist'),
            TokenState(row=2, column=12, name='Equal', value='='),
            TokenState(row=2, column=14, name='LeftBrace', value='{'),
            TokenState(row=2, column=15, name='Integer', value='-1'),
            TokenState(row=2, column=17, name='Comma', value=','),
            TokenState(row=2, column=19, name='Integer', value='0'),
            TokenState(row=2, column=20, name='Comma', value=','),
            TokenState(row=2, column=22, name='Float', value='.2'),
            TokenState(row=2, column=24, name='Comma', value=','),
            TokenState(row=2, column=26, name='Integer', value='+1'),
            TokenState(row=2, column=28, name='Comma', value=','),
            TokenState(row=2, column=30, name='Float', value='2.'),
            TokenState(row=2, column=32, name='Comma', value=','),
            TokenState(row=2, column=34, name='Float', value='3.0'),
            TokenState(row=2, column=37, name='RightBrace', value='}'),
            TokenState(row=2, column=38, name='Semicolon', value=';'),
            TokenState(row=3, column=1, name='For', value='for'),
            TokenState(row=3, column=5, name='Variable', value='let'),
            TokenState(row=3, column=9, name='Identifier', value='i'),
            TokenState(row=3, column=11, name='In', value='in'),
            TokenState(row=3, column=14, name='Identifier', value='mylist'),
            TokenState(row=3, column=21, name='Equal', value='='),
            TokenState(row=3, column=23, name='LeftBrace', value='{'),
            TokenState(row=4, column=3, name='Break', value='break!'),
            TokenState(row=4, column=9, name='Semicolon', value=';'),
            TokenState(row=5, column=3, name='Identifier', value='println'),
            TokenState(row=5, column=10, name='LeftParenthesis', value='('),
            TokenState(
                row=5,
                column=11,
                name='String',
                value='"Sorry, nothing from the list was printed!"',
            ),
            TokenState(row=5, column=54, name='RightParenthesis', value=')'),
            TokenState(row=5, column=55, name='Semicolon', value=';'),
            TokenState(row=6, column=1, name='RightBrace', value='}'),
        ]
    )


def test_tokenization_output_types(
    farr_regex_lexer_fixture: FarrRegexLexer,
) -> None:
    """Checks that the outputs have the same type."""
    assert all(
        map(
            lambda x: isinstance(x, TokenState),
            farr_regex_lexer_fixture.tokenize(
                textwrap.dedent(
                    """
                    fn add_one(let x) = {
                      return! + x 1;
                    }
                    """
                )
            ),
        )
    )


@pytest.mark.xfail(raises=ValueError)
def test_tokenization_value_error(
    farr_regex_lexer_fixture: FarrRegexLexer,
) -> None:
    """Checks for a `ValueError` during tokenization."""
    farr_regex_lexer_fixture.tokenize('var $text <- `Hi, there!`.')
