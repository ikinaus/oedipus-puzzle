
"""Inversion parity: which states are reachable from which.

The graph of all (n^2)! arrangements is not connected. It splits into exactly
two components of equal size, and no sequence of moves crosses between them.
The invariant that tells them apart is

    P(board) = (inversions + (n - 1) * row_of_blank) mod 2

For odd n the second term vanishes and plain inversion parity suffices; for
even n, as in the 15-puzzle, the blank's row is part of the answer.
"""
import random

from oedipus.core.board import BLANK, Board, board_from, find_blank


def inversions(board: Board) -> int:
    """Number of inversions"""
    tiles = [v for row in board for v in row if v != BLANK]
    invs = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return invs


def parity_class(board: Board) -> int:
    n = len(board)
    row, _ = find_blank(board)
    inv = inversions(board)

    return (inv + (n - 1)*row) % 2


def reachable(a: Board, b: Board) -> bool:
    return parity_class(a) == parity_class(b)


def random_board(n: int) -> Board:
    flat = list(range(n * n))
    random.shuffle(flat)
    return board_from(flat, n)
