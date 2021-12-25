import asyncio
from os import path

from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    pass


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
