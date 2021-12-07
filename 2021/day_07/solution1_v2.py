import asyncio
from os import path
from statistics import median
from typing import Callable


def distance_from(pos: int) -> Callable[[int], int]:
    def _helper(crab: int) -> int:
        return abs(pos - crab)

    return _helper


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        crabs = [int(p) for p in next(input_file).strip().split(',')]
        median_pos = int(median(crabs))

        print(sum(map(distance_from(median_pos), crabs)))


if __name__ == '__main__':
    asyncio.run(main())
