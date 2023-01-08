from collections import deque
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
    query_stack: list[tuple[_StateT, tuple[_NodeT, ...], _NodeT]] = [
        (initial_state, (), start),
    ]

    while query_stack:
        state, path, node = query_stack.pop()
        path += (node,)

        if goal(node, state):
            paths.append(path)
            continue

        for neighbor, neighbor_state in neighbors(path, state):
            query_stack.append((path, neighbor, neighbor_state))

    return tuple(paths)


def bfs(
    start: _NodeT,
    neighbors: Callable[[Sequence[_NodeT], _StateT], Iterable[tuple[_NodeT, _StateT]]],
    goal: Callable[[_NodeT, _StateT], bool],
    *,
    initial_state: _StateT = None,
) -> Sequence[Sequence[_NodeT]]:
    paths: list[tuple[_NodeT, ...]] = []
    query_queue: deque[tuple[tuple[_NodeT, ...], _NodeT, _StateT]] = deque(
        [
            ((), start, initial_state),
        ],
    )

    while query_queue:
        path, node, state = query_queue.popleft()
        path += (node,)

        if goal(node, state):
            paths.append(path)
            continue

        for neighbor, neighbor_state in neighbors(path, state):
            query_queue.append((path, neighbor, neighbor_state))

    return tuple(paths)


def dijkstra(
    start: _NodeT,
    neighbors: Callable[[Sequence[_NodeT], int], Iterable[tuple[_NodeT, int]]],
    goal: Callable[[_NodeT], bool],
) -> Sequence[_NodeT]:
    query_heap: list[int, tuple[_NodeT, ...], _NodeT] = [
        (0, (), start),
    ]

    while query_heap:
        path, node, cost = heappop(query_heap)
        path += (node,)

        if goal(node, cost):
            return path

        for neighbor, neighbor_cost in neighbors(path, cost):
            heappush(query_heap, (neighbor_cost, path, neighbor))

    return None
