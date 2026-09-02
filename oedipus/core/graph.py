
"""Graph traversal that works on any implicit graph.

Nothing here mentions the puzzle. A graph reaches this module as one function
that maps a vertex to its neighbours, so the same code walks the 12-vertex ring
of the 2x2 puzzle and the 181440-vertex graph of the 3x3 one.
"""
from collections.abc import Callable, Hashable


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
