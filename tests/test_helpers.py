# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

from typing import Callable, Sequence, Any, List, Tuple

import pytest

from farr.helpers import partition_a_sequence, normalize_identifier


@pytest.mark.parametrize(
    ('sequence', 'fn', 'expected'),
    [
        ([1, 3, 2, 4], lambda x: x % 2 == 0, ([2, 4], [1, 3])),
        (
            ['A', 66, 'C', 68],
            lambda x: isinstance(x, str),
            (['A', 'C'], [66, 68]),
        ),
    ],
)
def test_partition_a_sequence(
    sequence: Sequence[Any],
    fn: Callable[[Any], bool],
    expected: Tuple[List[Any], List[Any]],
) -> None:
    """Tests the result of partitioning a sequence based on a condition."""
    assert partition_a_sequence(sequence, fn) == expected


@pytest.mark.parametrize(
    ('identifier', 'expected'),
    [('fullname', 'fullname'), ('me?', 'me_q'), ('ok?!', 'ok_qe')],
)
def test_normalize_identifier(identifier: str, expected: str) -> None:
    """Tests the normalized output of an identifier."""
    assert normalize_identifier(identifier) == expected
