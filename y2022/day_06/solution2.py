import asyncio
from os import path
from typing import Optional

from aoclib.itertools import windowed
from aoclib.timing import benchmark


def unique_prefix(n: int, line: str) -> Optional[int]:
    for idx, group in enumerate(windowed(n, line)):
        if len(set(group)) == n:
            return idx + n

    return None


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    line = input_lines[0]

    print(unique_prefix(14, line))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
