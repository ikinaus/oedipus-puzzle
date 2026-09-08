# %%
ring = {i: [(i - 1) % 12, (i + 1) % 12] for i in range(12)}
print(ring[2])

# %%
path = [3]

while path[-1] != 6:
    path.append(ring[path[-1]][1])

print(f"nods: {path} \nlength(number of edges): {len(path) - 1}")
# %%

import numpy as np

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

def board_from(cells: list[int], size: int) -> Board:
    return tuple(tuple(cells[r * size:(r + 1) * size]) for r in range(size))

def all_boards(size: int) -> list[Board]:
    from itertools import permutations
    return [board_from(list(p), size) for p in permutations(range(size * size))]

def expected_degree(r: int, c: int, size: int) -> int:
    return sum(0 <= r + dr < size and 0 <= c + dc < size for dr, dc in DIRECTIONS)

print(f"{'#'*60}\n{'#'*60}")

# %%
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
    ring_2x2 = explore(board_from([1, 2, 3, 0], 2), neighbors)
    assert len(ring_2x2) == 12
    assert sum(degree(b) for b in ring_2x2) == 2 * 12

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
print(f"{'#'*60}\n{'#'*60}")

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
    ring_2x2 = explore(goal(2), neighbors)
    assert len(ring_2x2) == factorial(4) // 2 == 12
    assert {parity_class(b) for b in ring_2x2} == {parity_class(goal(2))}

    # 3x3: full traversal of the component containing the goal
    component = explore(goal(3), neighbors)
    assert len(component) == factorial(9) // 2 == 181_440
    print(f"vertices              :    {len(component)}   = 9!/2")
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

# ---- tests ----

# %%

import numpy as np
from numpy.linalg import matrix_power
from numpy.typing import NDArray

type Matrix = NDArray[np.float64]
type Vector = NDArray[np.float64]

def state_list(start: Board) -> list[Board]:
    """All vertices of the Graph"""
    return sorted(explore(start, neighbors))

def cycle_order(start: Board) -> list[Board]:
    """Vertices of a cycle-shaped component in walking order. 2x2 only."""

    assert degree(start) == 2, "cycle_order works only where every degree is 2"

    order = [start]
    prev: Board | None = None
    cur = start
    while True:
        nxt = next(t for t in neighbors(cur) if t != prev)
        if nxt == start:
           return order
        order.append(nxt)
        prev, cur = cur, nxt

def index_states[V: Hashable](states: list[V]) -> dict[V, int]:
    """Map each vertex to its row/column number in the matrix."""
    return {s: i for i, s in enumerate(states)}

def transition_matrix[V: Hashable](
    states: list[V], expand: Callable[[V], list[V]]
) -> Matrix:
    """Row-stochastic matrix of the simple random walk on the given vertices."""
    idx = index_states(states)
    n = len(states)
    P = np.zeros((n, n), dtype=np.float64)

    for s in states:
        nbrs = expand(s)
        p = 1 / len(nbrs)
        for t in nbrs:
            P[idx[s], idx[t]] += p

    return P


def step(pi: Vector, P: Matrix) -> Vector:
    """One step of the walk: pi_{t+1} = pi_t P."""
    return pi @ P

def point_mass(n: int, i: int) -> Vector:
    """Distribution concentrated on a single vertex."""
    pi = np.zeros(n, dtype=np.float64)
    pi[i] = 1.0
    return pi

print(f"{'#'*60}\n{'#'*60}")

# %%
# ---- tests: random walk on the 2x2 graph ----

if __name__ == "__main__":
    states = cycle_order(goal(2))
    idx = index_states(states)
    n = len(states)
    P = transition_matrix(states, neighbors)

    assert n == 12
    assert P.shape == (n, n)

    # rows are probability distributions
    assert np.allclose(P.sum(axis=1), 1.0)

    # row i has exactly deg(i) nonzeros, each equal to 1/deg(i)
    for s in states:
        row = P[idx[s]]
        d = degree(s)
        assert np.count_nonzero(row) == d
        assert np.allclose(row[row > 0], 1.0 / d)

    # nonzeros == 2|E|
    assert np.count_nonzero(P) == sum(degree(s) for s in states)

    # no self loops
    assert np.allclose(np.diag(P), 0.0)

    # the walk keeps total probability
    pi = point_mass(n, idx[goal(2)])
    for _ in range(20):
        pi = step(pi, P)
        assert np.isclose(pi.sum(), 1.0)

    # stepping one at a time == multiplying by a matrix power
    for t in (1, 2, 5, 13):
        a = point_mass(n, 0)
        for _ in range(t):
            a = step(a, P)
        assert np.allclose(a, point_mass(n, 0) @ matrix_power(P, t))

    # period 2: after t steps the walk sits only on vertices of parity t
    for t in range(8):
        pi = point_mass(n, 0) @ matrix_power(P, t)
        assert all(i % 2 == t % 2 for i in range(n) if pi[i] > 0)

    # the 8-puzzle graph is bipartite: a move flips the colour of the blank cell
    for b in list(explore(goal(3), neighbors))[:20000]:
        r, c = find_blank(b)
        for nb in neighbors(b):
            rr, cc = find_blank(nb)
            assert (r + c) % 2 != (rr + cc) % 2

    print("all checks passed")
    print()
    print("2x2, distribution after t steps (start = goal)")
    print("     " + " ".join(f"{i:>5}" for i in range(n)))
    for t in range(7):
        pi = point_mass(n, idx[goal(2)]) @ matrix_power(P, t)
        print(f"t={t}  " + " ".join(f"{v:5.3f}" for v in pi))
    print()
    print(f"P is {n}x{n}, nonzeros: {np.count_nonzero(P)}")
    print(f"a dense P for the 8-puzzle would hold {181440 ** 2:,} entries")

    print(P)

# --- test ---


# %%
from numpy.linalg import eig


def stationary(states: list[Board]) -> Vector:
    """pi(v) = deg(v)/sum{deg(v)}"""
    deg = np.array([degree(s) for s in states], dtype=np.float64)
    return deg / deg.sum()

# %%
# ---- tests: stationary distribution ----

if __name__ == "__main__":
    # ---- 2x2: the matrix is small enough to check pi P = pi directly ----
    states = cycle_order(goal(2))
    idx = index_states(states)
    P = transition_matrix(states, neighbors)
    pi = stationary(states)

    assert np.isclose(pi.sum(), 1.0)
    assert np.allclose(pi @ P, pi)

    # pi is the unique left eigenvector for eigenvalue 1
    vals, vecs = eig(P.T)
    one = np.argmin(np.abs(vals - 1.0))
    v = np.real(vecs[:, one])
    v = v / v.sum()
    assert np.allclose(v, pi)

    # detailed balance on every edge
    for i, s in enumerate(states):
        for nb in neighbors(s):
            j = idx[nb]
            assert np.isclose(pi[i] * P[i, j], pi[j] * P[j, i])

    # on the ring every degree is 2, so pi is uniform and hides the formula
    assert np.allclose(pi, 1.0 / len(states))

    # ---- 3x3: no matrix at all, balance checked through the neighbour function ----
    component3 = sorted(explore(goal(3), neighbors))
    total_degree = sum(degree(b) for b in component3)
    edges = total_degree // 2

    pi3 = {b: degree(b) / total_degree for b in component3}
    assert np.isclose(sum(pi3.values()), 1.0)

    # (pi P)(j) = sum over neighbours i of pi(i)/deg(i)  must equal pi(j)
    for b in component3:
        inflow = sum(pi3[nb] / degree(nb) for nb in neighbors(b))
        assert np.isclose(inflow, pi3[b])

    corner = min(pi3.values())
    centre = max(pi3.values())

    print("all checks passed")
    print()
    print(f"2x2  pi is uniform: {pi[0]:.6f} for all {len(states)} vertices")
    print()
    print(f"3x3  vertices        : {len(component3):,}")
    print(f"     sum of degrees  : {total_degree:,}  = 2|E|")
    print(f"     edges           : {edges:,}")
    print()
    print(f"     pi(blank in corner) = 2/{total_degree:,} = {corner:.3e}  = 1/{1/corner:,.0f}")
    print(f"     pi(blank at edge)   = 3/{total_degree:,} = {3/total_degree:.3e}")
    print(f"     pi(blank in centre) = 4/{total_degree:,} = {centre:.3e}  = 1/{1/centre:,.0f}")
    print(f"     ratio centre/corner : {centre/corner:.1f}")
    print()
    print(f"     the goal has its blank in a corner, so pi(goal) = 1/{1/pi3[goal(3)]:,.0f}")

# --- test ---

# %%
from collections import deque


def distances_from(target: Board) -> dict[Board, int]:
    """Shortest distance from every reachable state to target"""
    dist = {target: 0}
    queue = deque([target])

    while queue:
        s = queue.popleft()
        for t in neighbors(s):
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    return dist
# %%
print(f"{'#'*60}\n{'#'*60}")
# %%
import polars as pl


dist = distances_from(goal(3))
flat = []

for board in dist.keys():
    cells = [v for row in board for v in row]
    flat.append(cells)

df = pl.DataFrame({
    "board": flat,
    "distance": list(dist.values()),
})

print(df.head())
print(df.describe())
# %%
with pl.Config(tbl_rows=-1):
    print(df["distance"].value_counts().sort(by="distance"))
# %%
import seaborn as sns

hist = df["distance"].value_counts().sort(by="distance")
sns.barplot(x=hist["distance"], y=hist["count"])
# %%

def optimal_path(start: Board, dist: dict[Board, int]) -> list[Board]:
    """States along one shortest path from `start` to the `goal`, inclusive"""
    path = [start]
    cur = start
    while dist[cur] > 0:
        cur = min(neighbors(cur), key=lambda u: dist[u])
        path.append(cur)
    return path
# %%
print(f"{'#'*60}\n{'#'*60}")
# %%
b = next(x for x in iter(lambda: random_board(3), None) if parity_class(x) == parity_class(goal(3)))
print(b)
print(parity_class(b) == parity_class(goal(3)))   # False для упавшей доски
path = optimal_path(b, dist)
print(len(path))
np.array(path)
# %%
with pl.Config(fmt_table_cell_list_len=9):
    print(df.filter(pl.col("distance") == 31))
# %%
ddf = [b for b, d in dist.items() if d == 31]
np.array(ddf)
# %%
b = board_from([6, 1, 3, 8, 4, 2, 0, 7, 5], 3)
optimal_path(b, dist)

# %%
target = goal(3)
vi_states = explore(target, neighbors)


def value_iteration(
    states: set[Board],
    target: Board,
    gamma: float = 1.0,
) -> dict[Board, float]:
    old_V: dict[Board, float] = {
        state: 0.0
        for state in states
    }
    delta = float("inf")
    while delta != 0:
        delta = 0
        new_V: dict[Board, float] = {}

        for state in states:
            if state == target:
                new_val = 0.0
            else:
                new_val = max(
                    -1.0 + gamma * old_V[next_state]
                    for next_state in neighbors(state)
                )

            new_V[state] = new_val

            change = abs(new_val - old_V[state])
            delta = max(change, delta)

        old_V = new_V

    return old_V


# %%
values = value_iteration(vi_states, target)
print(len(values))
print(min(values.values()), max(values.values()))

# %%
error = max(
    abs(values[state] + dist[state])
    for state in vi_states
)
print(error)

# %%

from oedipus.core.board import Action, legal_actions, transition


def greedy_action(board: Board, values: dict[Board, float]) -> Action:
    return max(
        legal_actions(board),
        key=lambda action: values[transition(board, action)]
    )

print(f"{'#'*60}\n{'#'*60}")

# %%
temp_board = random_board(3)
while parity_class(temp_board)!=parity_class(goal(3)):
    temp_board = random_board(3)
print(temp_board)
# %%
print(values[temp_board])
# %%


b: Board = temp_board
steps: int = 0

while b != goal(3):
    action: Action = greedy_action(b, values)
    b = transition(b, action)
    steps += 1

print(steps)
print(b)

# %%
def greedy_path(
    start: Board,
    target: Board,
    values: dict[Board, float]) -> list[Board]:

    trajectory = [start]
    current = start

    while current != target:
        action = greedy_action(current, values)
        current = transition(current, action)
        trajectory.append(current)

    return trajectory

print(f"{'#'*60}\n{'#'*60}")
# %%
greedy_start = next(
    state for state, distance in dist.items()
    if distance == 31
)
greedy_trajectory = greedy_path(greedy_start, target, values)

assert greedy_trajectory[-1] == target
assert len(greedy_trajectory) - 1 == dist[greedy_start]

print(len(greedy_trajectory) - 1)
