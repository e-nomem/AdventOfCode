import asyncio
from itertools import permutations
from os import path

from .lib import add_numbers
from .lib import magnitude
from .lib import parse
from lib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    numbers = [parse(l.strip())[0] for l in input_lines]

    print(max(magnitude(add_numbers(a, b)) for a, b in permutations(numbers, 2)))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())