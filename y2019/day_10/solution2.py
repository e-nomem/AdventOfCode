import asyncio
from math import atan2
from math import hypot
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

        base = max(asteroids, key=lambda a: visible(asteroids, a))
        asteroids.remove(base)

        # First sort the asteroids by distance from the laser
        asteroids.sort(key=lambda o: hypot(o.x - base.x, o.y - base.y))

        # Make a dict of asteroid -> count of asteroids directly in front of it
        ranks = {a: sum(angle(base, a) == angle(base, b) for b in asteroids[:i]) for i, a in enumerate(asteroids)}

        # Sort asteroids by:
        # 1) The rank (same rank == vaporized in the same cycle of the laser)
        # 2) The angle (laser starts pointing up and circles around clockwise)
        winner = sorted(asteroids, key=lambda o: (ranks[o], angle(base, o)))[199]

        print(f"Solution: {(winner.x * 100) + winner.y}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
