"""Helpers that only tests need.

`all_boards` enumerates every arrangement, which is (n^2)! and therefore usable
up to 3x3 and no further. `expected_degree` recomputes the degree from the board
geometry alone, independently of `neighbors`, so the two can disagree.
"""
from itertools import permutations

from oedipus.core.board import DIRECTIONS, Board, board_from


def all_boards(size: int) -> list[Board]:
    return [board_from(list(p), size) for p in permutations(range(size * size))]


def expected_degree(r: int, c: int, size: int) -> int:
    return sum(0 <= r + dr < size and 0 <= c + dc < size for dr, dc in DIRECTIONS)
