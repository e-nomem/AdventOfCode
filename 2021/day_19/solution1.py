import asyncio
from operator import add
from os import path

from .lib import map_scanners
from .lib import Position
from .lib import Scanner
from lib.timing import benchmark


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

    beacons: set[Position] = {
        tuple(map(add, b, s.position))  # Move beacon position from relative to the scanner to absolute
        for s in scanners
        for b in s.beacons.keys()
        if s.position is not None  # Only ever false if map_scanners failed
    }
    print(len(beacons))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
