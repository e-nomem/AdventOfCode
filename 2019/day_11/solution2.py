import asyncio
from collections import defaultdict
from itertools import cycle
from os import path
from typing import AsyncGenerator
from typing import Dict
from typing import Set

from ..intcode.executor import run
from ..intcode.utils import load
from ..intcode.utils import Program


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f'({self.x}, {self.y})'


def generate_plane() -> Dict[int, Dict[int, int]]:
    return defaultdict(lambda: defaultdict(int))


async def paint(plane: Dict[int, Dict[int, int]], prog: Program) -> Set[Point]:
    x = 0
    y = 0
    direction = cycle('RDLU')
    ocount = 0
    visited = set()

    moved = asyncio.Event()
    read = asyncio.Event()

    async def reader() -> AsyncGenerator[int, None]:
        while True:
            read.set()
            yield plane[x][y]
            await moved.wait()

    async def writer(val: int) -> None:
        nonlocal ocount
        nonlocal x
        nonlocal y

        if ocount % 2 == 0:
            plane[x][y] = val
            visited.add(Point(x, y))
        else:
            await read.wait()
            if val:
                face = next(direction)
            else:
                for _ in range(3):
                    # Three rights make a left
                    face = next(direction)

            if face == 'U':
                y += 1
            elif face == 'R':
                x += 1
            elif face == 'D':
                y -= 1
            else:
                x -= 1

            # Done moving now
            moved.set()

        ocount += 1

    await run(prog, reader=reader, writer=writer)
    return visited


def print_plane(plane: Dict[int, Dict[int, int]], visited: Set[Point]) -> None:
    min_x = min(p.x for p in visited)
    max_x = max(p.x for p in visited)
    min_y = min(p.y for p in visited)
    max_y = max(p.y for p in visited)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            print('#' if plane[x][y] else ' ', end='')
        print()


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        prog = load(input_file.read())
        plane = generate_plane()
        plane[0][0] = 1

        visited = await paint(plane, prog)
        print_plane(plane, visited)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
