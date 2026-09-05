import pytest

from oedipus.agents.tabular import value_iteration
from oedipus.core.board import goal, neighbors
from oedipus.core.graph import explore
from oedipus.solvers.bfs import distances_from

TARGET = goal(2)
STATES = explore(TARGET, neighbors)
DISTANCES = distances_from(TARGET)


@pytest.mark.parametrize("gamma", [1.0, 0.9])
def test_value_iteration_matches_the_exact_discounted_return(gamma: float) -> None:
    values = value_iteration(STATES, TARGET, gamma)

    for state, distance in DISTANCES.items():
        expected = (
            -float(distance)
            if gamma == 1.0
            else -(1.0 - gamma**distance) / (1.0 - gamma)
        )
        assert values[state] == pytest.approx(expected)
