import asyncio
from enum import Enum
from functools import reduce
from os import path

from aoclib.timing import benchmark


class Direction(Enum):
    FORWARD = "forward"
    UP = "up"
    DOWN = "down"


def process(acc: tuple[int, int, int], line: str) -> tuple[int, int, int]:
    parts = line.split(" ", 2)
    direction = Direction(parts[0])
    magnitude = int(parts[1])
    x, y, aim = acc

    if direction is Direction.FORWARD:
        return x + magnitude, y + (aim * magnitude), aim
    elif direction is Direction.DOWN:
        return x, y, aim + magnitude
    elif direction is Direction.UP:
        return x, y, aim - magnitude

    return acc


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    x, y, _ = reduce(process, input_lines, (0, 0, 0))
    print(x * y)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
