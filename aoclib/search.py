from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Sequence
from heapq import heappop
from heapq import heappush
from typing import cast
from typing import Optional
from typing import TypeVar

_NodeT = TypeVar("_NodeT")
_StateT = TypeVar("_StateT")


def dfs(
    start: _NodeT,
    neighbors: Callable[[Sequence[_NodeT], _StateT], Iterable[tuple[_NodeT, _StateT]]],
    goal: Callable[[_NodeT, _StateT], bool],
    *,
    initial_state: _StateT = None,
) -> Sequence[Sequence[_NodeT]]:
    paths: list[tuple[_NodeT, ...]] = []
    query_stack: list[tuple[tuple[_NodeT, ...], _NodeT, _StateT]] = [
        (cast(tuple[_NodeT, ...], ()), start, cast(_StateT, initial_state)),
    ]

    while query_stack:
        path, node, state = query_stack.pop()
        path += (node,)

        if goal(node, state):
            paths.append(path)
            continue

        for neighbor, neighbor_state in neighbors(path, state):
            query_stack.append((path, neighbor, neighbor_state))

    return tuple(paths)


def dijkstra(
    start: _NodeT,
    neighbors: Callable[[_NodeT], Iterable[tuple[int, _NodeT]]],
    goal: Callable[[_NodeT], bool],
    heuristic: Optional[Callable[[_NodeT], int]] = None,
) -> Optional[dict[_NodeT, tuple[int, _NodeT]]]:
    if heuristic is None:
        heuristic = lambda _: 0

    visited: dict[_NodeT, tuple[int, _NodeT]] = {}
    query_stack: list[tuple[int, int, _NodeT, _NodeT]] = [(0, 0, start, start)]

    while query_stack:
        _, cost, node, parent = heappop(query_stack)

        if node in visited:
            continue

        visited[node] = (cost, parent)

        if goal(node):
            return visited

        for n_cost, neighbor in neighbors(node):
            if neighbor not in visited:
                neighbor_cost = cost + n_cost
                neighbor_heuristic = neighbor_cost + heuristic(neighbor)
                heappush(query_stack, (neighbor_heuristic, neighbor_cost, neighbor, node))

    return None
