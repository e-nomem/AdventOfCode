import asyncio
from itertools import combinations
from os import path

from .lib import diff_position
from .lib import map_scanners
from .lib import Position
from .lib import Scanner
from aoclib.timing import benchmark


def manhattan(pos_a: Position, pos_b: Position) -> int:
    return sum(abs(x) for x in diff_position(pos_a, pos_b))


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    scanners: list[Scanner] = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("--- scanner"):
            scanners.append(Scanner(len(scanners)))
        else:
            scanners[-1].add_beacon(tuple(map(int, line.strip().split(","))))

    map_scanners(scanners)

    print(
        max(
            manhattan(sa.position, sb.position)
            for sa, sb in combinations(scanners, 2)
            if sa.position is not None and sb.position is not None  # Only ever false if map_scanners failed
        ),
    )


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
