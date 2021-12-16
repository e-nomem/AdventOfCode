from heapq import heappop
from heapq import heappush
from typing import Callable
from typing import Generator
from typing import Optional

Point = tuple[int, int]

ADJACENTS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def neighbors(cost: Callable[[Point], Optional[int]], coord: Point) -> Generator[tuple[Point, int], None, None]:
    x, y = coord
    for x_n, y_n in ADJACENTS:
        x_p = x + x_n
        y_p = y + y_n

        p = (x_p, y_p)
        c = cost(p)

        if c is not None:
            yield p, c


def find_shortest_path(cost: Callable[[Point], Optional[int]], start: Point, end: Point) -> Optional[int]:
    visited: set[Point] = set()
    query_stack: list[tuple[int, Point]] = []
    heappush(query_stack, (0, start))
    while query_stack:
        base_cost, loc = heappop(query_stack)

        if loc in visited:
            continue

        if loc == end:
            return base_cost

        visited.add(loc)

        for neighbor, neighbor_cost in neighbors(cost, loc):
            if neighbor not in visited:
                heappush(query_stack, (base_cost + neighbor_cost, neighbor))

    return None


def scale_map(map: list[list[int]], scale: int) -> Callable[[Point], Optional[int]]:
    x_len = len(map[0])
    y_len = len(map)
    max_x = x_len * scale
    max_y = y_len * scale

    def _helper(p: Point) -> Optional[int]:
        x, y = p
        if 0 <= x < max_x and 0 <= y < max_y:
            x_b = x // x_len
            y_b = y // y_len
            x = x % x_len
            y = y % y_len

            val = map[y][x]
            return ((val + x_b + y_b - 1) % 9) + 1

        return None

    return _helper
