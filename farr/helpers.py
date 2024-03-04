# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import re
from typing import Callable, Sequence, Any, List, Tuple


def partition_a_sequence(
    sequence: Sequence[Any],
    fn: Callable[[Any], bool],
) -> Tuple[List[Any], List[Any]]:
    """Partitions a sequence into two parts based on the condition."""
    return (
        [i for i in sequence if fn(i)],
        [i for i in sequence if not fn(i)],
    )


def normalize_identifier(identifier: str) -> str:
    """Makes an identifier understandable to Python."""
    return (
        '_'.join(
            filter(
                lambda x: x,
                re.split(r'([\!\?]+)', identifier),
            )
        )
        .replace('!', 'e')
        .replace('?', 'q')
    )
