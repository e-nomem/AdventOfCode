import asyncio
from math import atan2
from math import pi
from os import path
from typing import List

from ..util import Point


def angle(a: Point, b: Point) -> float:
    return atan2(b.x - a.x, a.y - b.y) % (2 * pi)


def visible(asteroids: list[Point], a: Point) -> int:
    return len({angle(a, b) for b in asteroids if a != b})


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        lines = input_file.read().splitlines()
        asteroids = [Point(x, y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == "#"]

        count = max(visible(asteroids, a) for a in asteroids)
        print(f"Solution: {count}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
