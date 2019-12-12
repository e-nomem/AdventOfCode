import asyncio
from itertools import count
from math import gcd
from os import path
from typing import List
from typing import Set
from typing import Tuple

Moon = Tuple[List[int], List[int]]
Moons = List[Moon]


def process_input(i: str) -> List[int]:
    parts = [a for a in i.strip().split(',')]
    return [int(p.strip('<>').split('=')[1]) for p in parts]


def update_vel(moons: Moons) -> Moons:
    for i, moon in enumerate(moons):
        for j, other in enumerate(moons):
            if i == j:
                continue

            for axis in range(3):
                a_m = moon[0][axis]
                a_o = other[0][axis]
                if a_m > a_o:
                    moon[1][axis] -= 1
                elif a_m < a_o:
                    moon[1][axis] += 1

    return moons


def update_pos(moons: Moons) -> Moons:
    for moon in moons:
        for axis in range(3):
            moon[0][axis] += moon[1][axis]

    return moons


def step(moons: Moons, count: int = 1) -> Moons:
    for _ in range(count):
        moons = update_vel(moons)
        moons = update_pos(moons)

    return moons


def find_periods(moons: Moons) -> Tuple[int, int, int]:
    px = 0
    py = 0
    pz = 0
    sx: Set[str] = set()
    sy: Set[str] = set()
    sz: Set[str] = set()
    for i in count(0):
        if px and py and pz:
            break

        moons = step(moons)

        # Stringify the list of [pos[axis], vel[axis]] values for each moon
        # When we see an exact match, we have found the period for that axis
        if not px:
            posx = str([[m[0][0], m[1][0]] for m in moons])
            if posx in sx:
                px = i
            sx.add(posx)
        if not py:
            posy = str([[m[0][1], m[1][1]] for m in moons])
            if posy in sy:
                py = i
            sy.add(posy)
        if not pz:
            posz = str([[m[0][2], m[1][2]] for m in moons])
            if posz in sz:
                pz = i
            sz.add(posz)

    return px, py, pz


def lcm(x: int, y: int) -> int:
    return x // gcd(x, y) * y


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        moon_pos = [process_input(l) for l in input_file]
        moons = [(i, [0, 0, 0]) for i in moon_pos]

        x, y, z = find_periods(moons)

        # Answer is the least common multiple of all the periods
        solution = lcm(lcm(x, y), z)
        print(f'Solution: {solution}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
