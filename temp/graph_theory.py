# %%
ring = {i: [(i - 1) % 12, (i + 1) % 12] for i in range(12)}
print(ring[2])

# %%
path = [3]

while path[-1] != 6:
    path.append(ring[path[-1]][1])

print(f"nods: {path} \nlength(number of edges): {len(path) - 1}")
# %%
from gettext import find

import numpy as np
from numpy._core.numeric import ndarray

board = np.array([[1, 2],
                  [3, 0]])
print(np.argwhere(board == 0)[0])
# %%
def neighbors2(board: np.ndarray) -> list[np.ndarray]:\

    ind_lst = np.argwhere(board == 0)[0]
    r, c = ind_lst[0], ind_lst[1]

    n1 = board.copy()
    n1[r, c] = board[(r+1)%2, c]
    n1[(r+1)%2, c] = 0

    n2 = board.copy()
    n2[r, c] = board[r, (c+1)%2]
    n2[r, (c+1)%2] = 0

    return [n1, n2]

print(board)
neighbors2(board)
# %%
from collections.abc import Callable, Hashable
from typing import Final

type Coord = tuple[int, int]
type Row = tuple[int, ...]
type Board = tuple[Row, ...]

BLANK: Final[int] = 0
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

def find_blank(board: Board) -> Coord:
    """Return row and col of blank[0] cell"""
    for r, row in enumerate(board):
        for c, v in enumerate(row):
            if v == 0:
                return r, c
    raise ValueError("There is NO blank cell on the board")

def swap(board: Board, a: Coord, b: Coord) -> Board:
    """New board after swap two cells"""
    (r1, c1), (r2, c2) = a, b
    rows = [list(row) for row in board]
    rows[r1][c1], rows[r2][c2] = rows[r2][c2], rows[r1][c1]

    return tuple(tuple(row) for row in rows)

def neighbors(board: Board) -> list[Board]:
    """Neighbors of current nod"""
    n = len(board)
    r, c = find_blank(board)
    result: list[Board] = []

    for dr, dc in DIRECTIONS:
        rr, cc = r + dr, c + dc
        if 0 <= rr < n and 0 <= cc < n:
            result.append(swap(board, (r, c), (rr, cc)))

    return result

def degree(board: Board) -> int:
    return len(neighbors(board))

def explore[V: Hashable](start: V, expand: Callable[[V], list[V]]) -> set[V]:
    """
    Universe function for all type of graphs.
    Return set of Nodes which could be reach from the taken one.
    """
    seen: set[V] = {start}
    stack: list[V] = [start]

    while stack:
        vertex = stack.pop()
        for nxt in expand(vertex):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)

    return seen
print(f"{'#'*60}\n{'#'*60}")

# %%
def board_from(cells: list[int], size: int) -> Board:
    return tuple(tuple(cells[r * size:(r + 1) * size]) for r in range(size))

def all_boards(size: int) -> list[Board]:
    from itertools import permutations
    return [board_from(list(p), size) for p in permutations(range(size * size))]

def expected_degree(r: int, c: int, size: int) -> int:
    return sum(0 <= r + dr < size and 0 <= c + dc < size for dr, dc in DIRECTIONS)

if __name__ == "__main__":
    EXPECTED_3X3 = {
        (0, 0): 2, (0, 1): 3, (0, 2): 2,
        (1, 0): 3, (1, 1): 4, (1, 2): 3,
        (2, 0): 2, (2, 1): 3, (2, 2): 2,
    }

    boards3 = all_boards(3)

    # degree depends only on the blank position
    for b in boards3:
        assert degree(b) == EXPECTED_3X3[find_blank(b)]

    # moves are reversible
    for b in boards3[:2000]:
        for nb in neighbors(b):
            assert b in neighbors(nb)

    # a move changes exactly two cells, one of them the blank
    for b in boards3[:2000]:
        r, c = find_blank(b)
        for nb in neighbors(b):
            diff = [(i, j) for i in range(3) for j in range(3) if b[i][j] != nb[i][j]]
            assert len(diff) == 2 and (r, c) in diff

    # swap does not mutate its input
    b = board_from([1, 2, 3, 4, 5, 6, 7, 8, 0], 3)
    before = b
    swap(b, (2, 2), (2, 1))
    assert b == before

    # handshake lemma on the full 2x2 graph
    ring = explore(board_from([1, 2, 3, 0], 2), neighbors)
    assert len(ring) == 12
    assert sum(degree(b) for b in ring) == 2 * 12

    # size independence
    assert degree(board_from(list(range(16)), 4)) == 2
    assert degree(board_from(list(range(25)), 5)) == 2

    print("all checks passed")

    print("\n3x3 degree by blank position")
    for r in range(3):
        print("   " + " ".join(str(EXPECTED_3X3[(r, c)]) for c in range(3)))

    total = sum(EXPECTED_3X3.values())
    print(f"\nsum of degrees over 9 cells : {total}")
    print(f"mean degree                 : {total}/9 = {total / 9:.4f}")

    n = 4
    for i in range(n * n):
        r, c = divmod(i, n)
        tiles = list(range(1, n * n))
        b = board_from(tiles[:i] + [BLANK] + tiles[i:], n)
        assert degree(b) == expected_degree(r, c, n)

    print("\n4x4 degree by blank position")
    for r in range(n):
        print("   " + " ".join(str(expected_degree(r, c, n)) for c in range(n)))

    total4 = sum(expected_degree(r, c, n) for r in range(n) for c in range(n))
    print(f"\nsum of degrees over {n * n} cells : {total4}")
    print(f"mean degree                  : {total4}/{n * n} = {total4 / (n * n):.4f}")

# %%
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

# %%
import random
from math import factorial


def random_board(n: int) -> Board:
    flat = list(range(n * n))
    random.shuffle(flat)
    return board_from(flat, n)

def goal(n: int) -> Board:
    return board_from(list(range(1, n * n)) + [BLANK], n)

# %%
# ---- tests ----

if __name__ == "__main__":
    random.seed(0)

    # invariant: no legal move changes the parity class, any board size
    for size in (2, 3, 4):
        sample = [random_board(size) for _ in range(500)]
        for b in sample:
            p = parity_class(b)
            assert all(parity_class(nb) == p for nb in neighbors(b))

    all_boards_3 = all_boards(3)  # 362 880 штук, считаем один раз

    # swapping tiles 1 and 2 flips the class -> the two classes are in bijection
    for b in random.sample(all_boards_3, 5000):
        pos = {v: (r, c) for r, row in enumerate(b) for c, v in enumerate(row)}
        assert parity_class(swap(b, pos[1], pos[2])) != parity_class(b)

    # 2x2: the reachable component is exactly 4!/2
    ring = explore(goal(2), neighbors)
    assert len(ring) == factorial(4) // 2 == 12
    assert {parity_class(b) for b in ring} == {parity_class(goal(2))}

    # 3x3: full traversal of the component containing the goal
    component = explore(goal(3), neighbors)
    assert len(component) == factorial(9) // 2 == 181_440
    assert {parity_class(b) for b in component} == {parity_class(goal(3))}

    # the other class is exactly the complement, and is the same size
    everything = set(all_boards_3)
    other = everything - component
    assert len(other) == len(component)
    assert {parity_class(b) for b in other} == {1 - parity_class(goal(3))}

    # handshake lemma on the real 8-puzzle graph
    total_degree = sum(degree(b) for b in component)
    assert total_degree % 2 == 0
    edges = total_degree // 2
    assert edges == 241_920  # сверка с числом из roadmap

    # the classic unsolvable position
    scrambled: Board = board_from([2, 1, 3, 4, 5, 6, 7, 8, 0], 3)
    assert not reachable(scrambled, goal(3))
    assert scrambled in other
