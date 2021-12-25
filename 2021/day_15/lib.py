from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterable
from typing import Optional

from aoclib.search import dijkstra

Point = tuple[int, int]

ADJACENTS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def neighbors(cost: Callable[[Point], Optional[int]]) -> Callable[[Point], Iterable[tuple[int, Point]]]:
    def _helper(coord: Point) -> Generator[tuple[int, Point], None, None]:
        x, y = coord
        for x_n, y_n in ADJACENTS:
            p = x + x_n, y + y_n
            c = cost(p)

            if c is not None:
                yield c, p

    return _helper


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
