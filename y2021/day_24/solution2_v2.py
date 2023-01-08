import asyncio
from functools import reduce
from os import path

from .lib2 import make_value_generators
from aoclib.timing import benchmark


# See solution1_v2 to understand what is happening here
@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    program = tuple(tuple(l.split()) for l in input_lines)
    value_generators = make_value_generators(program)

    values: tuple[int, ...] = ()
    values = reduce(lambda vals, gen: vals + (min(gen(vals)),), value_generators, values)
    print(reduce(lambda acc, n: (acc * 10) + n, values))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
