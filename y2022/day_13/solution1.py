import asyncio
from os import path

from .lib import is_ordered
from .lib import parse_packet
from .lib import Result
from aoclib.itertools import chunked
from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    packets = [parse_packet(line) for line in input_lines if line]
    total = sum(idx + 1 for idx, chunk in enumerate(chunked(2, packets)) if is_ordered(*chunk) is Result.Ordered)
    print(total)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
