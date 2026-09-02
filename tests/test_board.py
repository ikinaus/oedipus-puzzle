from conftest import all_boards, expected_degree

from oedipus.core.board import (
    BLANK,
    board_from,
    degree,
    find_blank,
    goal,
    neighbors,
    swap,
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
