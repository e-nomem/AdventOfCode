import asyncio
from os import path
from typing import Iterable

from .lib import window


def process(depths: Iterable[int]) -> int:
    return sum(1 for pair in window(depths, 4) if pair[-1] > pair[0])


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        increasing = process(int(line) for line in input_file)
        print(increasing)


def test_process() -> None:
    depths = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    assert process(depths) == 5


if __name__ == '__main__':
    asyncio.run(main())
