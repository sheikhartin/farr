# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import re
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass(frozen=True)
class Token:
    name: str
    pattern: str
    ignore: Optional[bool] = field(default=False, kw_only=True)


@dataclass(frozen=True)
class GroupedTokens:
    pattern: str
    tokens: List[Token]


@dataclass(frozen=True)
class TokenState:
    row: int = field(kw_only=True)
    column: int = field(kw_only=True)
    name: str = field(kw_only=True)
    value: str = field(kw_only=True)


class RegexLexer:
    """A base class for building a lexer using regular expressions.

    Attributes:
        tokens: The language tokens.
        _separator: A pattern that separates parts of the code.
        _row: The current row position in the source code.
        _column: And the column position.
    """

    tokens: List[GroupedTokens]

    def __init__(self) -> None:
        # Patching the separator tokens pattern
        self._separator = re.compile(
            '|'.join(
                f'({grouped_tokens.pattern})' for grouped_tokens in self.tokens
            )
        )
        self._row = self._column = -1

    def _match_token(self, chunk: str) -> Token:
        """Checks whether the token is valid or not."""
        for grouped_tokens in self.tokens:
            if re.fullmatch(grouped_tokens.pattern, chunk):
                for token in grouped_tokens.tokens:
                    if re.fullmatch(token.pattern, chunk):
                        return token
        raise ValueError(
            'A strange thing was found! '
            f'Line {self._row}, column {self._column}'
        )

    def _update_position(self, chunk: str) -> None:
        """Updates the pointer position after passing the current chunk."""
        for char in chunk:
            if char in '\r\n':  # TODO: Check for different operating systems
                self._row += 1
                self._column = 1
            else:
                self._column += 1
        return None

    def tokenize(self, code: str) -> List[TokenState]:
        """Tokenizes the code and then labels them."""
        self._row = self._column = 1
        result = []

        for chunk in filter(lambda x: x, self._separator.split(code)):
            if not (token := self._match_token(chunk)).ignore:
                result.append(
                    TokenState(
                        row=self._row,
                        column=self._column,
                        name=token.name,
                        value=chunk,
                    )
                )
            self._update_position(chunk)
        return result
