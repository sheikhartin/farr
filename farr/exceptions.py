# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

from dataclasses import dataclass, field
from typing import Optional, Any


class BreakError(Exception):
    """Exception to break the loop."""


class ContinueError(Exception):
    """Exception to ignore the current iteration of the loop."""


@dataclass
class ReturnError(Exception):
    """Exception to throw a possible value."""

    expression: Optional[Any] = field(kw_only=True)


@dataclass
class InterpretError(Exception):
    """Exception to keep the error and the node that caused it cleaner."""

    error: BaseException = field(kw_only=True)
    origin: str = field(kw_only=True)
