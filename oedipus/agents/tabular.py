"""Value iteration and tabular Q-learning."""

from oedipus.core.board import Board, neighbors


def value_iteration(
    states: set[Board],
    target: Board,
    gamma: float = 1.0,
) -> dict[Board, float]:
    """Solve the Bellman optimality equation over a complete state set."""
    old_values = {state: 0.0 for state in states}
    delta = float("inf")

    while delta != 0:
        delta = 0.0
        new_values: dict[Board, float] = {}

        for state in states:
            if state == target:
                new_value = 0.0
            else:
                new_value = max(
                    -1.0 + gamma * old_values[next_state]
                    for next_state in neighbors(state)
                )

            new_values[state] = new_value
            delta = max(delta, abs(new_value - old_values[state]))

        old_values = new_values

    return old_values
