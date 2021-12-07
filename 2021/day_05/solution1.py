import asyncio
from collections import Counter
from os import path
from typing import Generator
from typing import Tuple


def direction(c1: int, c2: int) -> int:
    if c1 == c2:
        return 0
    elif c1 < c2:
        return 1
    else:
        return -1


def line_points(c1: str, c2: str) -> Generator[Tuple[int, int], None, None]:
    x, y = map(int, c1.split(','))
    x2, y2 = map(int, c2.split(','))

    x_dir = direction(x, x2)
    y_dir = direction(y, y2)

    if x_dir != 0 and y_dir != 0:
        return

    while x != (x2 + x_dir) or y != (y2 + y_dir):
        yield x, y
        x += x_dir
        y += y_dir


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        c = Counter(
            p
            for line in input_file
            for p in line_points(*line.strip().split(' -> '))
        )
        print(sum(1 for count in c.values() if count > 1))


if __name__ == '__main__':
    asyncio.run(main())
