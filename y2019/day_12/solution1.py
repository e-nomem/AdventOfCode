import asyncio
from os import path
from typing import List
from typing import Tuple

Moon = tuple[list[int], list[int]]


def process_input(i: str) -> list[int]:
    parts = [a for a in i.strip().split(",")]
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


def potential(moon: Moon) -> int:
    return sum(map(lambda i: abs(i), moon[0]))


def kinetic(moon: Moon) -> int:
    return sum(map(lambda i: abs(i), moon[1]))


def energy(moon: Moon) -> int:
    return potential(moon) * kinetic(moon)


def step(moons: list[Moon], count: int = 1) -> list[Moon]:
    for _ in range(count):
        moons = update_vel(moons)
        moons = update_pos(moons)

    return moons


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        moons = [(i, [0, 0, 0]) for i in (process_input(l) for l in input_file)]

        moons = step(moons, 1000)
        total = sum(energy(m) for m in moons)
        print(f"Total: {total}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
