import random

from oedipus.core.board import goal
from oedipus.solvers.bfs import distances_from, optimal_path

DIST = distances_from(goal(3))


def test_the_search_reaches_the_whole_component() -> None:
    assert len(DIST) == 181_440


def test_known_shape_of_the_distance_table() -> None:
    assert max(DIST.values()) == 31
    assert abs(sum(DIST.values()) / len(DIST) - 21.9724) < 1e-3
    assert sum(1 for d in DIST.values() if d == 31) == 2


def test_optimal_path_has_exactly_d_star_moves() -> None:
    random.seed(2)
    for s in random.sample(sorted(DIST), 500):
        path = optimal_path(s, DIST)
        assert len(path) - 1 == DIST[s]
        assert path[-1] == goal(3)
