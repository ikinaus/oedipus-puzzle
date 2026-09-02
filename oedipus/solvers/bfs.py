
"""Exact distances to the goal by breadth-first search.

Practical for the 8-puzzle only: 181440 states fit in memory, so one pass from
the goal yields d* for every position at once. The 15-puzzle has about 1.05e13
states and no such table exists.

Because every move is reversible the graph is undirected, hence
d(s, goal) = d(goal, s) and a single search from the goal answers for all s.
"""
from collections import deque

from oedipus.core.board import Board, neighbors


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


def optimal_path(start: Board, dist: dict[Board, int]) -> list[Board]:
    """States along one shortest path from `start` to the `goal`, inclusive"""
    path = [start]
    cur = start
    while dist[cur] > 0:
        cur = min(neighbors(cur), key=lambda u: dist[u])
        path.append(cur)
    return path
