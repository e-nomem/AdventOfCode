import asyncio
from enum import Enum
from functools import reduce
from os import path
from typing import Tuple


class Direction(Enum):
    FORWARD = "forward"
    UP = "up"
    DOWN = "down"


# Tuple[x, y]
def process(acc: tuple[int, int], line: str) -> tuple[int, int]:
    parts = line.split(" ", 2)
    direction = Direction(parts[0])
    magnitude = int(parts[1])

    if direction is Direction.FORWARD:
        return (acc[0] + magnitude, acc[1])
    elif direction is Direction.DOWN:
        return (acc[0], acc[1] + magnitude)
    elif direction is Direction.UP:
        return (acc[0], acc[1] - magnitude)

    return acc


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        x, y = reduce(process, (line for line in input_file), (0, 0))
        print(x * y)


if __name__ == "__main__":
    asyncio.run(main())
