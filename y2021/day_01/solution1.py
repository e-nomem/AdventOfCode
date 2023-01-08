import asyncio
from collections.abc import Iterable
from os import path

from .lib import window
from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    print(sum(1 for pair in window(int(l) for l in input_lines) if pair[-1] > pair[0]))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
