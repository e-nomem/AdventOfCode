import asyncio
from os import path

from aoclib.timing import benchmark


def translate(x):
    res = ord(x) - ord("X")
    if res < 0:
        res = ord(x) - ord("A")

    return res


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    sum = 0
    for line in input_lines:
        opponent, me = (translate(x) for x in line.split())
        sum += me + 1
        if opponent == me:
            sum += 3
        elif opponent == (me - 1) % 3:
            sum += 6

    print(sum)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
