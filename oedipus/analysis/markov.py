
"""The simple random walk on the puzzle graph, studied as a Markov chain.

Study code, not runtime: no agent ever calls this. It exists because the
numbers it produces justify design decisions taken elsewhere, in particular
that a random policy reaches the goal about once per 5000 episodes and that
learning therefore cannot start without curriculum, HER or reward shaping.
"""
from collections.abc import Callable, Hashable

import numpy as np
from numpy.typing import NDArray

from oedipus.core.board import Board, degree, neighbors
from oedipus.core.graph import explore

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


def stationary(states: list[Board]) -> Vector:
    """pi(v) = deg(v)/sum{deg(v)}"""
    deg = np.array([degree(s) for s in states], dtype=np.float64)
    return deg / deg.sum()
