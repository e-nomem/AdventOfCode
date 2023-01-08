import asyncio
from functools import cmp_to_key
from functools import reduce
from operator import mul
from os import path

from .lib import is_ordered
from .lib import parse_packet
from aoclib.timing import benchmark


DIVIDERS = [
    [[2]],
    [[6]],
]


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    packets = [parse_packet(line) for line in input_lines if line]
    packets.extend(DIVIDERS)
    packets.sort(key=cmp_to_key(is_ordered))

    print(reduce(mul, (idx + 1 for idx, p in enumerate(packets) if p in DIVIDERS)))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
