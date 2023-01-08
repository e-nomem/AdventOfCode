import asyncio
from os import path

from aoclib.timing import benchmark

CHR_a = ord("a")
CHR_A = ord("A")


def priority(c):
    val = ord(c)
    if (ret := val - CHR_a) >= 0:
        return ret

    return val - CHR_A + 27


@benchmark(10)
def puzzle(input_lines: tuple[str, ...]) -> None:
    sum = 0
    for line in input_lines:
        items = len(line) // 2
        (common,) = set(line[:items]) & set(line[items:])
        sum += priority(common)

    print(sum)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = tuple(l.strip() for l in input_file)

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
