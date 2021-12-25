import asyncio
from os import path
from typing import cast

from .lib import all_launches
from aoclib.timing import benchmark


@benchmark(100)
def puzzle(input_lines: list[str]) -> None:
    x_range, y_range = (
        cast(tuple[int, int], tuple(map(int, r.split("=")[1].split(".."))))
        for r in input_lines[0].strip().split(": ")[1].split(", ")
    )
    print(sum(1 for _ in all_launches(x_range, y_range)))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
