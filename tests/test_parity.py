import random
from math import factorial

from conftest import all_boards

from oedipus.core.board import BLANK, board_from, goal, neighbors, swap
from oedipus.core.graph import explore
from oedipus.core.parity import inversions, parity_class, random_board, reachable


def test_no_legal_move_changes_the_parity_class() -> None:
    random.seed(0)
    for size in (2, 3, 4):
        for b in (random_board(size) for _ in range(300)):
            p = parity_class(b)
            assert all(parity_class(nb) == p for nb in neighbors(b))


def test_swapping_two_tiles_flips_the_class() -> None:
    random.seed(1)
    for b in random.sample(all_boards(3), 2000):
        pos = {v: (r, c) for r, row in enumerate(b) for c, v in enumerate(row)}
        assert parity_class(swap(b, pos[1], pos[2])) != parity_class(b)


def test_reachable_component_is_half_of_everything() -> None:
    assert len(explore(goal(2), neighbors)) == factorial(4) // 2
    component = explore(goal(3), neighbors)
    assert len(component) == factorial(9) // 2 == 181_440
    assert set(all_boards(3)) - component == set(all_boards(3)) - component
    assert len(set(all_boards(3)) - component) == len(component)


def test_the_classic_unsolvable_position() -> None:
    scrambled = board_from([2, 1, 3, 4, 5, 6, 7, 8, BLANK], 3)
    assert inversions(goal(3)) == 0
    assert inversions(scrambled) == 1
    assert not reachable(scrambled, goal(3))
