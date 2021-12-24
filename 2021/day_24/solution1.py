import asyncio
from os import path

from .lib import find_model
from lib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    program = tuple(tuple(l.split()) for l in input_lines)
    guess_generator = lambda: range(9, 0, -1)

    print(find_model(program, guess_generator))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
