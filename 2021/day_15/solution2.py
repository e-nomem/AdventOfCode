import asyncio
from heapq import heappop
from heapq import heappush
from os import path
from typing import Iterable


def neighbors(map: list[list[int]], coord: tuple[int, int]) -> Iterable[tuple[tuple[int, int], int]]:
    ret = []
    x, y = coord
    if x > 0:
        ret.append((x-1, y))
    if y > 0:
        ret.append((x, y-1))
    if x < len(map[0]) - 1:
        ret.append((x+1, y))
    if y < len(map) - 1:
        ret.append((x, y+1))

    return ((p, map[p[1]][p[0]]) for p in ret)


def find_shortest_path(map: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> int:
    costs = {}
    query_stack: list[tuple[int, tuple[int, int]]] = []
    heappush(query_stack, (0, start))
    while end not in costs and query_stack:
        base_cost, loc = heappop(query_stack)
        if loc in costs:
            continue

        costs[loc] = base_cost

        for neighbor, neighbor_cost in neighbors(map, loc):
            if neighbor not in costs:
                heappush(query_stack, (base_cost + neighbor_cost, neighbor))

    return costs[end]


def extend_map(map: list[list[int]], scale: int) -> list[list[int]]:
    new_map = []
    for y_scale in range(scale):
        block_row: list[list[int]] = []
        for _ in map:
            block_row.append([])

        for x_scale in range(scale):
            for y, row in enumerate(map):
                block_row[y].extend(((i - 1 + x_scale + y_scale) % 9) + 1 for i in map[y])

        new_map.extend(block_row)

    return new_map


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        map = []
        for line in input_file:
            row = [int(c) for c in line.strip()]
            map.append(row)

    map = extend_map(map, 5)

    start = (0, 0)
    end = (len(map[0]) - 1, len(map) - 1)
    print(find_shortest_path(map, start, end))


if __name__ == '__main__':
    asyncio.run(main())
