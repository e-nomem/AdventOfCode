import asyncio
from enum import Enum
from functools import reduce
from os import path
from typing import Tuple


class Direction(Enum):
    FORWARD = 'forward'
    UP = 'up'
    DOWN = 'down'


# Tuple[x, y, aim]
def process(acc: Tuple[int, int, int], line: str) -> Tuple[int, int, int]:
    parts = line.split(' ', 2)
    direction = Direction(parts[0])
    magnitude = int(parts[1])

    if direction is Direction.FORWARD:
        x = acc[0] + magnitude
        y = acc[1] + (acc[2] * magnitude)
        return (x, y, acc[2])
    elif direction is Direction.DOWN:
        return (acc[0], acc[1], acc[2] + magnitude)
    elif direction is Direction.UP:
        return (acc[0], acc[1], acc[2] - magnitude)

    return acc


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        r = reduce(process, (line for line in input_file), (0, 0, 0))
        print(f'{r[0] * r[1]}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
