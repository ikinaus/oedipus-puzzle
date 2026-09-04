"""The puzzle state and its move graph.

A board is a tuple of tuples: immutable, hashable, and therefore usable as a
set member and a dict key. Both are required — breadth-first search keeps a set
of visited states and the tabular agents key their tables by state.

    ((1, 2, 3),          1 2 3
     (4, 5, 6),   ==     4 5 6
     (7, 8, 0))          7 8 .

An action moves the BLANK, not a tile. The action space always contains four
directions, while the legal actions depend on the blank position. The price is
inverted directions: moving the blank up means the tile above it slid down.

Nothing here is specific to 3x3 — the size is read from the board itself.
"""
from enum import IntEnum
from typing import Final

type Coord = tuple[int, int]
type Row = tuple[int, ...]
type Board = tuple[Row, ...]

BLANK: Final[int] = 0
DIRECTIONS: Final[tuple[Coord, ...]] = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)

class Action(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3    


def find_blank(board: Board) -> Coord:
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            if value == BLANK:
                return r, c
    raise ValueError("no blank cell on the board")


def swap(board: Board, a: Coord, b: Coord) -> Board:
    """A new board with two cells exchanged. The input is not modified."""
    (r1, c1), (r2, c2) = a, b
    rows: list[list[int]] = [list(row) for row in board]
    rows[r1][c1], rows[r2][c2] = rows[r2][c2], rows[r1][c1]
    return tuple(tuple(row) for row in rows)


def legal_actions(board: Board) -> tuple[Action, ...]:
    n = len(board)
    row, col = find_blank(board)
    result: list[Action] = []

    for action in Action:
        dr, dc = DIRECTIONS[action]
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < n and 0 <= new_col < n:
            result.append(action)

    return tuple(result)


def transition(board: Board, action: Action) -> Board:
    n = len(board)
    row, col = find_blank(board)
    dr, dc = DIRECTIONS[action]
    new_row = row + dr
    new_col = col + dc

    if not (0 <= new_row < n and 0 <= new_col < n):
            raise ValueError(
                f"action {action.name} is illegal for blank at {(row, col)}"
            )

    return swap(board, (row, col), (new_row, new_col))


def neighbors(board: Board) -> list[Board]:
    """Every board reachable in exactly one move."""
    return [transition(board, action) for action in legal_actions(board)]


def degree(board: Board) -> int:
    return len(neighbors(board))


def board_from(cells: list[int], size: int) -> Board:
    return tuple(tuple(cells[r * size:(r + 1) * size]) for r in range(size))


def goal(size: int) -> Board:
    """Tiles 1..size^2-1 in reading order, blank in the bottom-right corner."""
    return board_from(list(range(1, size * size)) + [BLANK], size)
