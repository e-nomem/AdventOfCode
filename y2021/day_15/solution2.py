import asyncio
from collections.abc import Iterable
from os import path

from .lib import neighbors
from .lib import scale_map
from aoclib.search import dijkstra
from aoclib.timing import benchmark


@benchmark(100)
def puzzle(input_file: Iterable[str], scale: int) -> None:
    map = []
    for line in input_file:
        row = [int(c) for c in line.strip()]
        map.append(row)

    neighbor_func = neighbors(scale_map(map, scale))
    start = (0, 0)
    end = ((len(map[0]) * scale) - 1, (len(map) * scale) - 1)

    node_map = dijkstra(start, neighbor_func, lambda n: n == end)
    if node_map is None:
        print("No path found!")
        return

    print(node_map[end][0])


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [line for line in input_file]

    puzzle(input_lines, 5)


if __name__ == "__main__":
    asyncio.run(main())
