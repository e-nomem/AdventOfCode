import asyncio
from collections.abc import Iterable
from os import path

from .lib import find_shortest_path
from .lib import scale_map
from aoclib.timing import benchmark


@benchmark(20)
def puzzle(input_file: Iterable[str], scale: int) -> None:
    map = []
    for line in input_file:
        row = [int(c) for c in line.strip()]
        map.append(row)

    cost_func = scale_map(map, scale)

    start = (0, 0)
    end = ((len(map[0]) * scale) - 1, (len(map) * scale) - 1)
    print(find_shortest_path(cost_func, start, end))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [line for line in input_file]

    puzzle(input_lines, 5)


if __name__ == "__main__":
    asyncio.run(main())
