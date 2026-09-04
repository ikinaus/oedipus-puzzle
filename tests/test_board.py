import pytest
from conftest import all_boards, expected_degree

from oedipus.core.board import (
    BLANK,
    Action,
    board_from,
    degree,
    find_blank,
    goal,
    legal_actions,
    neighbors,
    swap,
    transition,
)


def test_degree_depends_only_on_the_blank() -> None:
    for b in all_boards(3):
        r, c = find_blank(b)
        assert degree(b) == expected_degree(r, c, 3)


def test_moves_are_reversible() -> None:
    for b in all_boards(3)[:2000]:
        for nb in neighbors(b):
            assert b in neighbors(nb)


def test_a_move_changes_two_cells_one_of_them_the_blank() -> None:
    for b in all_boards(3)[:2000]:
        blank = find_blank(b)
        for nb in neighbors(b):
            diff = [(i, j) for i in range(3) for j in range(3) if b[i][j] != nb[i][j]]
            assert len(diff) == 2
            assert blank in diff


def test_swap_does_not_mutate_its_input() -> None:
    b = goal(3)
    swap(b, (2, 2), (2, 1))
    assert b == goal(3)


def test_size_independence() -> None:
    for n in (2, 3, 4, 5):
        assert goal(n)[n - 1][n - 1] == BLANK
        assert degree(board_from(list(range(1, n * n)) + [BLANK], n)) == 2


def test_legal_actions_depend_on_the_blank_position() -> None:
    corner = goal(3)
    edge = board_from([1, 2, 3, 4, 5, 6, 7, BLANK, 8], 3)
    centre = board_from([1, 2, 3, 4, BLANK, 5, 6, 7, 8], 3)

    assert legal_actions(corner) == (Action.UP, Action.LEFT)
    assert legal_actions(edge) == (Action.UP, Action.LEFT, Action.RIGHT)
    assert legal_actions(centre) == tuple(Action)


def test_transition_moves_the_blank_in_the_action_direction() -> None:
    board = goal(3)

    assert transition(board, Action.UP) == board_from([1, 2, 3, 4, 5, BLANK, 7, 8, 6], 3)
    assert transition(board, Action.LEFT) == board_from([1, 2, 3, 4, 5, 6, 7, BLANK, 8], 3)


def test_transition_rejects_an_illegal_action() -> None:
    with pytest.raises(ValueError, match="action DOWN is illegal"):
        transition(goal(3), Action.DOWN)


def test_neighbors_are_transitions_for_all_legal_actions() -> None:
    boards = [
        goal(3),
        board_from([1, 2, 3, 4, 5, 6, 7, BLANK, 8], 3),
        board_from([1, 2, 3, 4, BLANK, 5, 6, 7, 8], 3),
    ]

    for board in boards:
        assert neighbors(board) == [transition(board, action) for action in legal_actions(board)]
