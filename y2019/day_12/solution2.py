import asyncio
from functools import reduce
from itertools import count
from math import gcd
from os import path
from typing import List
from typing import Set
from typing import Tuple

Moon = tuple[list[int], list[int]]


def process_input(i: str) -> list[int]:
    parts = (a for a in i.strip().split(","))
    return [int(p.strip("<>").split("=")[1]) for p in parts]


def update_vel(moons: list[Moon]) -> list[Moon]:
    for i, moon in enumerate(moons):
        for other in moons[i + 1 :]:
            for axis in range(3):
                a_m = moon[0][axis]
                a_o = other[0][axis]
                if a_m > a_o:
                    moon[1][axis] -= 1
                    other[1][axis] += 1
                elif a_m < a_o:
                    moon[1][axis] += 1
                    other[1][axis] -= 1
    return moons


def update_pos(moons: list[Moon]) -> list[Moon]:
    for moon in moons:
        for axis in range(3):
            moon[0][axis] += moon[1][axis]

    return moons


def step(moons: list[Moon], count: int = 1) -> list[Moon]:
    for _ in range(count):
        moons = update_vel(moons)
        moons = update_pos(moons)

    return moons


def strify(moons: list[Moon], axis: int) -> str:
    return str([[m[0][axis], m[1][axis]] for m in moons])


def find_periods(moons: list[Moon]) -> list[int]:
    period = [0, 0, 0]
    positions: list[set[str]] = [set(), set(), set()]
    for i in count():
        if all(period):
            break

        moons = step(moons)

        # Stringify the list of [pos[axis], vel[axis]] values for each moon
        # When we see an exact match, we have found the period for that axis
        for axis in range(3):
            if not period[axis]:
                pos = strify(moons, axis)
                if pos in positions[axis]:
                    period[axis] = i
                positions[axis].add(pos)

    return period


def lcm(x: int, y: int) -> int:
    return x // gcd(x, y) * y


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        moons = [(i, [0, 0, 0]) for i in (process_input(l) for l in input_file)]

        # Answer is the least common multiple of all the periods
        solution = reduce(lcm, find_periods(moons), 1)
        print(f"Solution: {solution}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
